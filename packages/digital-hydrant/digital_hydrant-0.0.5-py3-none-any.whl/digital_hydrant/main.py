# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import sqlite3
import shutil
import sys

from digital_hydrant import logging
from digital_hydrant.scheduler import Scheduler
from digital_hydrant.uploader import Uploader
from digital_hydrant.collector_queue import CollectorQueue
from digital_hydrant.ping import Ping
from digital_hydrant.args import args
from digital_hydrant.process_manager import ProcessManager
from digital_hydrant.config import db_path, update_config, check_default_config


def create_tables(logger):
    tables = {
        "unique_ips": "id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT UNIQUE, last_tested TIMESTAMP, last_nmap_scan TIMESTAMP, open_ports TEXT",
        "collectors": "id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, payload TEXT, timestamp TIMESTAMP, uploaded INTEGER DEFAULT 0",
    }

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for table_name, columns in tables.items():
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    except Exception as e:
        logger.critical(f"Failed to initialize databases: {err}")


def check_required_ubuntu_packages():
    missing = False
    packages = {
        "arp-scan": "https://github.com/royhills/arp-scan",
        "dhcpcd": "https://wiki.archlinux.org/index.php/Dhcpcd",
        "iw": "https://wireless.wiki.kernel.org/en/users/documentation/iw",
        "lldpd": "https://lldpd.github.io/lldpd/installation.html",
        "ifconfig": "(https://wiki.linuxfoundation.org/networking/net-tools",
        "nmap": "https://nmap.org",
        "hydra": "https://github.com/vanhauser-thc/thc-hydra",
        "tshark": "https://www.wireshark.org/docs/man-pages/tshark.html",
        "wpa_supplicant": "https://wiki.archlinux.org/index.php/wpa_supplicant",
        "yersinia": "https://github.com/tomac/yersinia",
    }

    for package, link in packages.items():
        which = shutil.which(package)

        if which is None:
            print(f"Digital Hydrant requires your system to have {package} installed")
            print(f"    Package details can be found at {link}")
            missing = True

    return missing


def run():
    check_default_config()
    missing = False if args.force else check_required_ubuntu_packages()

    if args.init is not None:
        if len(args.init) > 0:
            update_config({"api": {"token": args.init}})

        print("\ninit complete!")
        return

    if missing:
        sys.exit(
            "\nPlease install all required dependencies or use -f/--force to run without dependencies"
        )

    logger = logging.getLogger(__name__)
    manager = ProcessManager("Main")
    create_tables(logger)

    if args.clear_queue:
        queue = CollectorQueue()
        queue.remove_all()

    # ping the server
    ping = Ping()
    manager.add_process("ping", ping.__exec__)

    collect = args.collect
    upload = args.upload

    if not (collect or upload):
        collect = upload = True

    if collect:
        scheduler = Scheduler()
        manager.add_process("scheduler", scheduler.__schedule__)

    if upload:
        logger.info("Launching Uploader")
        # upload data to the api
        uploader = Uploader()
        manager.add_process("uploader", uploader.__upload__)

    manager.manage()
