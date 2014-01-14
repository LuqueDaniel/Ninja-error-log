# -*- coding: UTF-8 -*-
#
# This file is part of Ninja-error-log
# Ninja-error-log is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Ninja-error-log is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ninja-error-log. If not, see <http://www.gnu.org/licenses/>.
#
# Source url (https://github.com/LuqueDaniel/Ninja-error-log)

import zipfile
import os
import re

VERSION = "0.2"

FOLDERS = ['ninja_error_log']
PATH_LIST = ['ninja_error_log.plugin']


def get_file_list(path):
    for item in os.listdir(path):
        item_src = os.path.join(path, item)
        if os.path.isdir(item_src):
            get_file_list(item_src)
        elif os.path.isfile(item_src) and not re.search('.+\.pyc$', item):
            PATH_LIST.append(item_src)


with zipfile.ZipFile('ninja-eror-log_{}.zip'.format(VERSION), 'w') as zip_file:
    for folder in FOLDERS:
        get_file_list(os.path.join(folder))
    for item in PATH_LIST:
        zip_file.write(item)

    zip_file.close()
