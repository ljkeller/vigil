# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'splash.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class SplashUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 400)
        Form.setFixedSize(640, 400)
        self.progress_bar = QtWidgets.QProgressBar(Form)
        self.progress_bar.setGeometry(QtCore.QRect(70, 270, 501, 31))
        self.progress_bar.setStyleSheet("QProgressBar{\n"
"    border-radius: 10px;\n"
"    background-color: #ffffff;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    background-color: #41C363\n"
"}")
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(300, 130, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 90, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600; color:#41C363;\">Vigil</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600; color:#000000;\">Avnet</span></p></body></html>"))
