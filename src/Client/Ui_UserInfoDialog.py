# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserInfoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserInfoDialog(object):
    def setupUi(self, UserInfoDialog):
        UserInfoDialog.setObjectName("UserInfoDialog")
        UserInfoDialog.resize(600, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/IconaFrontEnd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UserInfoDialog.setWindowIcon(icon)
        self.UserInfoDIalog = QtWidgets.QLabel(UserInfoDialog)
        self.UserInfoDIalog.setGeometry(QtCore.QRect(10, 0, 571, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.UserInfoDIalog.setFont(font)
        self.UserInfoDIalog.setObjectName("UserInfoDIalog")
        self.horizontalLayoutWidget = QtWidgets.QWidget(UserInfoDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 581, 441))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DialogInfoUser_lbl = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DialogInfoUser_lbl.setFont(font)
        self.DialogInfoUser_lbl.setScaledContents(True)
        self.DialogInfoUser_lbl.setObjectName("DialogInfoUser_lbl")
        self.horizontalLayout.addWidget(self.DialogInfoUser_lbl)

        self.retranslateUi(UserInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(UserInfoDialog)

    def retranslateUi(self, UserInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        UserInfoDialog.setWindowTitle(_translate("UserInfoDialog", "Informazioni Utente"))
        self.UserInfoDIalog.setText(_translate("UserInfoDialog", "Finanze Utente"))
        self.DialogInfoUser_lbl.setText(_translate("UserInfoDialog", "Grafico Non Disponibile"))
