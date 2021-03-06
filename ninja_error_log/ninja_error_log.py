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

# Ninja_ide imports
from ninja_ide.core import plugin

# PyQt4.QtGui imports
from PyQt4.QtGui import (QMessageBox, QDialog, QAction, QVBoxLayout,
                         QPushButton, QTextEdit)

# PyQt4.QtCore imports
from PyQt4.QtCore import SIGNAL

# OS imports
import os

# sys imports
import sys


class msgNinjaErrorLog(QMessageBox):
    """This class is a son of QMessageBox, is used for show messages in ninjaErrorLog"""

    def __init__(self, path=None):
        """This class is used for show messages in ninjaErrorLog

        'path'
            Path of the Ninja.exe.log
        """

        super(msgNinjaErrorLog, self).__init__()

        if path is not None:
            msg = QMessageBox.information(self, 'Ninja Error Log',
                                    'No such file: {}'.format(path))
        else:
            msg = QMessageBox.information(self, 'Ninja Error log',
                                    'This plugin is only for Windows.')


class ninjaErrorLogDialog(QDialog):
    """Plugin dialog"""

    def __init__(self, path):
        """Plugin dialog

        'path'
            Path of the ninja.exe.log
        """

        super(ninjaErrorLogDialog, self).__init__()

        # Set log path
        self._path = path

        self.setWindowTitle('Ninja Error Log')
        self.setFixedSize(600, 400)

        # Create text area and load file
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        with open(self._path, 'r') as f:
            self.editor.setPlainText(f.read())
            f.close()

        # Create delete button
        self.delete_button = QPushButton('Delete log file')
        self.delete_button.setToolTip('Requires admin permissions.')

        # Create central layout and add widgets
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.editor)
        vlayout.addWidget(self.delete_button)

        # SIGNALS
        self.connect(self.delete_button, SIGNAL('clicked()'), self._delete_log)

    def _delete_log(self):
        """
        This method delete Ninja.exe.log
        """

        # Check if Ninja.exe.lgo currently exists
        if os.path.exists(self._path):
            msg = QMessageBox.question(self, 'Ninja Error log',
                        'Delete Ninja.exe.log file?',
                        QMessageBox.Yes, QMessageBox.No)

            if msg == QMessageBox.Yes:
                try:
                    # Delete Ninja.exe.log
                    os.remove(self._path)
                    done_msg = QMessageBox.information(self, 'Ninja Error Log',
                                'The file has been deleted: Ninja.exe.log')
                    self.close()
                except:
                    err_msg = QMessageBox.warning(self, 'Ninja Error Log',
                        'You need permissions of administrator to delete Ninja.exe.log.')

        else:
            msg = QMessageBox.information(self, 'Ninja Error Log',
                                'No such file: {}'.format(self._path))


class ninjaErrorLog(plugin.Plugin):
    """This is the main class of the plugin, this class run the plugin."""

    def initialize(self):
        if sys.platform == 'win32':
            # Get executable path
            self.executable_path = os.path.abspath(os.path.dirname(sys.executable))

            # Get Ninja-IDE service and create action in menu
            menu_service = self.locator.get_service('menuApp')
            menu_service.add_action(QAction('Ninja Error Log', self,
                                        triggered=self.check_error_log))
        else:
            msgNinjaErrorLog()

    def check_error_log(self):
        """This method check if Ninja.exe.log is currently exists"""

        if os.path.exists(os.path.join(self.executable_path, 'Ninja.exe.log')):
            self.dialog = ninjaErrorLogDialog(os.path.join(self.executable_path,
                                         'Ninja.exe.log'))
            self.dialog.show()
        else:
            msgNinjaErrorLog(os.path.join(self.executable_path,
                             'Ninja.exe.log'))
