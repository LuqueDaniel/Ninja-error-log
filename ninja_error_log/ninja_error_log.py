#Ninja_ide imports
from ninja_ide.core import plugin

#PyQt4.QtGui imports
from PyQt4.QtGui import (QMessageBox, QDialog, QAction, QVBoxLayout,
                         QPushButton, QTextEdit)

#PyQt4.QtCore imports
from PyQt4.QtCore import SIGNAL

#OS imports
import os

#sys imports
import sys


class msgNinjaErrorLog(QMessageBox):

    def __init__(self, path=None):
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
        super(ninjaErrorLogDialog, self).__init__()
        #Set log path
        self._path = path

        self.setWindowTitle('Ninja Error Log')
        self.setFixedSize(600, 400)

        #Create text area and load file
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        with open(self._path, 'r') as f:
            self.editor.setPlainText(f.read())
            f.close()

        #Create delete button
        self.delete_button = QPushButton('Delete log file')
        self.delete_button.setToolTip('Requires admin permissions.')

        #Create central layout and add widgets
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.editor)
        vlayout.addWidget(self.delete_button)

        #SIGNALS
        self.connect(self.delete_button, SIGNAL('clicked()'), self._delete_log)

    def _delete_log(self):
        """This method delete Ninja.exe.log"""

        if os.path.exists(self._path):
            msg = QMessageBox.question(self, 'Ninja Error log',
                        'Delete Ninja.exe.log file?',
                        QMessageBox.Yes, QMessageBox.No)

            if msg == QMessageBox.Yes:
                try:
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
    def initialize(self):
        if sys.platform == 'win32':
            #Get executable path
            self.executable_path = os.path.abspath(os.path.dirname(sys.executable))

            #Get Ninja-IDE service and create action in menu
            menu_service = self.locator.get_service('menuApp')
            menu_service.add_action(QAction('Ninja Error Log', self,
                                        triggered=self.check_error_log))
        else:
            msgNinjaErrorLog()

    def check_error_log(self):
        if os.path.exists(os.path.join(self.executable_path, 'Ninja.exe.log')):
            self.dialog = ninjaErrorLogDialog(os.path.join(self.executable_path,
                                         'Ninja.exe.log'))
            self.dialog.show()
        else:
            msgNinjaErrorLog(os.path.join(self.executable_path,
                             'Ninja.exe.log'))
