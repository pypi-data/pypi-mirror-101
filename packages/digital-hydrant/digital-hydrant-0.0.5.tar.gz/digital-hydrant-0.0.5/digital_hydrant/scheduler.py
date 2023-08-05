#!/usr/bin/env python3
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

import importlib
import pkgutil

import digital_hydrant.collectors
from digital_hydrant import logging
from digital_hydrant.process_manager import ProcessManager


class Scheduler:
    def __init__(self, package=digital_hydrant.collectors):
        self.logger = logging.getLogger(__name__)
        self.package = package
        self.manager = ProcessManager("Scheduler")

        self.collectors = []
        for importer, modname, ispkg in pkgutil.iter_modules(self.package.__path__):
            if ispkg:
                self.collectors.append(modname)

    def __schedule__(self):
        for name in self.collectors:
            self.manager.add_process(name, self.__exec__, (name,))
        self.manager.manage()

    def __exec__(self, name):
        __module__ = importlib.import_module(f".{name}", package=self.package.__name__)
        __class__ = getattr(__module__, name.capitalize())
        collector = __class__(name)
        collector.run_collection()
