from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_EditEventDialog import Ui_EditEventDialog
from Ui_EventBetDialog import Ui_BetInfoDialog
from Ui_UserInfoDialog import Ui_UserInfoDialog

class EditEventDialog(Ui_EditEventDialog,QtWidgets.QDialog):
    def __init__(self,pos):
        super(Ui_EditEventDialog, self).__init__()
        self.setupUi(self)
        self.move(pos)

class BetInfoDialog(Ui_BetInfoDialog,QtWidgets.QDialog):
    def __init__(self,pos):
        super(Ui_BetInfoDialog, self).__init__()
        self.setupUi(self)
        self.move(pos)

class UserInfoDialog(Ui_UserInfoDialog,QtWidgets.QDialog):
    def __init__(self,pos):
        super(Ui_UserInfoDialog, self).__init__()
        self.setupUi(self)
        self.move(pos)

class CustomDialog(QtWidgets.QDialog):
    def __init__(self,titolo,testo,pos):
        super(QtWidgets.QDialog, self).__init__()

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/IconaFrontEnd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle(titolo)
        self.setGeometry(QtCore.QRect(30, 30, 360, 80))
        self.move(pos)

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(20, 20, 300, 80))
        self.label.setObjectName("label")
        self.label.setText(testo)
        

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MessageBox(QtWidgets.QMessageBox):
    def __init__(self, title, text, pos):
        super(QtWidgets.QMessageBox, self).__init__()
        self.title = title
        self.text = text
        self.pos = pos
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/IconaFrontEnd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def showMessageInfo(self):
            self.move(self.pos)
            self.setIcon(QtWidgets.QMessageBox.Information)
            self.setText(self.text)
            self.setWindowTitle(self.title)
            self.exec_()

    def showMessageError(self):
            self.move(self.pos)
            self.setIcon(QtWidgets.QMessageBox.Critical)
            self.setText(self.text)
            self.setWindowTitle(self.title)
            self.exec_()