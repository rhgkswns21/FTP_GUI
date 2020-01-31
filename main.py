import sys
import ftplib
import csv
import datetime
import os
import json

import ftp_func

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout,QLabel,
QPushButton, QTextEdit,  QGridLayout, QRadioButton, QSlider,  QMessageBox, QTabWidget, QProgressBar, QAction, qApp, QApplication, QComboBox, QLineEdit)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

mainStatusBar = None

ftp = ftp_func


class mainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initmainWidgetUI()

    def initmainWidgetUI(self):
        print('initmainWidgetUI')

        ## Make Button
        self.ConnectBT = QtWidgets.QPushButton('Connect')
        self.ConnectBT.clicked.connect(self.ConnectBT_Push)

        self.MakeCsvBT = QtWidgets.QPushButton('Make CSV')
        self.MakeCsvBT.clicked.connect(self.MakeCsvBT_Push)

        self.DisconnectBT = QtWidgets.QPushButton('Disconnect')
        self.DisconnectBT.clicked.connect(self.DisconnectBT_Push)

        self.UploadFileBT = QtWidgets.QPushButton('Upload')
        self.UploadFileBT.clicked.connect(self.UploadFileBT_Push)

        self.makeremotecommandBT = QtWidgets.QPushButton('Make Command.txt')
        self.makeremotecommandBT.clicked.connect(self.makeremotecommandBT_Push)

        self.SaveBT = QtWidgets.QPushButton('Save')
        self.SaveBT.clicked.connect(self.SaveBT_Push)

        ## Make Label
        self.FtpUrlLabel = QLabel('Host')
        self.FtpIdLabel = QLabel('ID')
        self.FtpPasswordLabel = QLabel('PW')
        self.FtpPortLabel = QLabel('Port')

        self.PanIDLabel = QLabel('PanID')
        self.dateTimeLabel = QLabel('Date')

        self.timeoutLabel = QLabel('TimeOut(s)')

        self.makeremotecommandLabel = QLabel('Remote Command')

        ## Make Line Edit
        self.FtpUrLineEdit = QLineEdit()
        self.FtpIdLineEdit = QLineEdit()
        self.FtpPasswordLineEdit = QLineEdit()
        self.FtpPortLineEdit = QLineEdit()
        self.FtpPortLineEdit.setText('21')

        self.PanIDLineEdit = QLineEdit()

        self.timeoutLineEdit = QLineEdit('60')

        self.makeremotecommandLineEdit = QLineEdit()

        ## Make Date Bar
        self.dateTimeVar = QtWidgets.QDateEdit()
        self.dateTimeVar.setDate(QDate.currentDate())

        ## Make Check Box
        self.timeoutCheckBox = QtWidgets.QCheckBox('TimeOut')
        self.timeoutCheckBox.setLayoutDirection(Qt.RightToLeft)

        self.device_checkbox_list = []
        self.device_checkbox_list.append(QtWidgets.QCheckBox('M'))
        for i in range(10):
            self.device_checkbox_list.append(QtWidgets.QCheckBox('S' + str(i+1)))
        self.deviceallCheckBox = QtWidgets.QCheckBox('All')
        self.deviceallCheckBox.clicked.connect(self.deviceallCheckBox_Push)

        ## Make List View
        self.uploadListView = QtWidgets.QListView()
        upload_model = QStandardItemModel()
        # file_list = os.listdir('./command')
        # file_list.sort()
        # for i in file_list:
        #     upload_model.appendRow(QStandardItem(i))
        self.uploadListView.setModel(upload_model)
        self.uploadListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        self.uploadfilelistListView = QtWidgets.QListView()

        self.makeremotecommandlistview = QtWidgets.QListView()
        log_list_model = QStandardItemModel()
        # f = open('remote_command.txt', 'r')
        # log_list = f.readlines()
        # f.close()
        # for i in log_list:
        #     log_list_model.appendRow(QStandardItem(i.rstrip()))
        # self.makeremotecommandlistview.setModel(log_list_model)
        # self.makeremotecommandlistview.clicked.connect(self.makeremotecommandlistview_Push)

        ## Make HorizontalLayout
        self.HorizontalLayout = QtWidgets.QHBoxLayout()

        for i in self.device_checkbox_list:
            self.HorizontalLayout.addWidget(i)
        self.HorizontalLayout.addWidget(self.deviceallCheckBox)


        ## Make Combo Box
        self.LoadComboBox = QtWidgets.QComboBox()

        try:
            if os.path.isdir('login'):
                pass
            else:
                os.mkdir('login')

            if os.path.isfile('login/info.txt'):
                f = open('login/info.txt', 'r')
                load_list = f.readlines()
                f.close()
                save_list = json.loads(load_list[0])
                self.LoadComboBox.addItems(save_list.keys())
                select_key = self.LoadComboBox.currentText()
                self.FtpUrLineEdit.setText(save_list[select_key]['host'])
                self.FtpIdLineEdit.setText(save_list[select_key]['id'])
                self.FtpPasswordLineEdit.setText(save_list[select_key]['pw'])
                self.FtpPortLineEdit.setText(save_list[select_key]['port'])

            self.LoadComboBox.currentIndexChanged.connect(self.LoadComboBox_Push)
        except:
            pass

        ## Make GridLayout
        mainlayout = QGridLayout()

        ## FTP Connect Info
        mainlayout.addWidget(self.FtpUrlLabel, 0, 0, 1, 1)
        mainlayout.addWidget(self.FtpUrLineEdit, 0, 1, 1, 1)

        mainlayout.addWidget(self.FtpIdLabel, 0, 2, 1, 1)
        mainlayout.addWidget(self.FtpIdLineEdit, 0, 3, 1, 1)

        mainlayout.addWidget(self.FtpPasswordLabel, 0, 4, 1, 1)
        mainlayout.addWidget(self.FtpPasswordLineEdit, 0, 5, 1, 1)

        mainlayout.addWidget(self.FtpPortLabel, 0, 6, 1, 1)
        mainlayout.addWidget(self.FtpPortLineEdit, 0, 7, 1, 1)

        # mainlayout.addWidget(self.ConnectBT, 2, 4, 1, 1)
        mainlayout.addWidget(self.SaveBT, 0, 8, 1, 1)
        mainlayout.addWidget(self.LoadComboBox, 0, 9, 1, 1)

        ## Data File Info
        mainlayout.addWidget(self.PanIDLabel, 1, 0, 1, 1)
        mainlayout.addWidget(self.PanIDLineEdit, 1, 1, 1, 1)

        mainlayout.addWidget(self.dateTimeLabel, 1, 2, 1, 1)
        mainlayout.addWidget(self.dateTimeVar, 1, 3, 1, 2)

        mainlayout.addWidget(self.MakeCsvBT, 2, 0, 1, 0)

        # ## Upload File List View
        # mainlayout.addWidget(self.uploadListView, 13, 0, 3, 2)
        #
        # mainlayout.addWidget(self.uploadfilelistListView, 13, 2, 3, 2)
        #
        # mainlayout.addWidget(self.timeoutCheckBox, 13, 4, 1, 1)
        # mainlayout.addWidget(self.timeoutLabel, 14, 4, 1, 1)
        # mainlayout.addWidget(self.timeoutLineEdit, 15, 4, 1, 1)
        #
        # mainlayout.addWidget(self.UploadFileBT, 16, 0, 1, 5)
        #
        # ## Make Rrmote Command
        # mainlayout.addWidget(self.makeremotecommandLabel, 8, 0, 1, 1)
        # mainlayout.addWidget(self.makeremotecommandLineEdit, 9, 0, 1, 5)
        # mainlayout.addWidget(self.makeremotecommandlistview, 10, 0, 1, 5)
        # mainlayout.addLayout(self.HorizontalLayout, 11, 0, 1, 5)
        # mainlayout.addWidget(self.makeremotecommandBT, 12, 0, 1, 5)
        #
        #
        # ## Disconnect BT
        # mainlayout.addWidget(self.DisconnectBT, 17, 0, 1, 5)

        self.setLayout(mainlayout)

    def remove_file_cheker(self, remove_list):
        print('remove_file_cheker')
        uploaddoneList = QStandardItemModel()
        for i in remove_list:
            uploaddoneList.appendRow(QStandardItem(i))
        self.uploadfilelistListView.setModel(uploaddoneList)

    def ConnectBT_Push(self):
        print('ConnectBT_Push')
        try:
            if ftp_func.ftp_connect(self.FtpUrLineEdit.text(), int(self.FtpPortLineEdit.text()), self.FtpIdLineEdit.text(), self.FtpPasswordLineEdit.text()):
                print('connect Ok')
                mainStatusBar.showMessage('FTP Connected')
            else:
                print('connect Fail')
                mainStatusBar.showMessage('FTP Connect failed')
        except:
            print('Invalid Connect Info')
            mainStatusBar.showMessage('Invalid Connect Info')

    def MakeCsvBT_Push(self):
        print('MakeCsvBT_Push')
        # if ftp.make_csv_file(self.PanIDLineEdit.text(), self.dateTimeVar.date().toString('yyyyMMdd')):
        #     print('Make Done')
        #     mainStatusBar.showMessage('CSV Make Done')
        # else:
        #     print('Make Fail')
        #     mainStatusBar.showMessage('CSV Make Failed')
        try:
            ## connect FTP
            if ftp_func.ftp_connect(self.FtpUrLineEdit.text(), int(self.FtpPortLineEdit.text()), self.FtpIdLineEdit.text(), self.FtpPasswordLineEdit.text()):
                print('connect Ok')
                mainStatusBar.showMessage('FTP Connected')

            else:
                print('connect Fail')
                mainStatusBar.showMessage('FTP Connect failed')
                return 0

            ## Make csv File
            if ftp.make_csv_file(self.PanIDLineEdit.text(), self.dateTimeVar.date().toString('yyyyMMdd')):
                print('Make Done')
                mainStatusBar.showMessage('CSV Make Done')
            else:
                print('Make Fail')
                mainStatusBar.showMessage('CSV Make Failed')
                return 0

            ## Disconnect
            if ftp.ftp_disconnect():
                mainStatusBar.showMessage('FTP Disconnected')
            else:
                mainStatusBar.showMessage('FTP Disconnect Failed')
                return 0
        except:
            print('Invalid Connect Info')
            mainStatusBar.showMessage('Invalid Connect Info')



    def DisconnectBT_Push(self):
        print('DisconnectBT_Push')
        if ftp.ftp_disconnect():
            mainStatusBar.showMessage('FTP Disconnected')
        else:
            mainStatusBar.showMessage('FTP Disconnect Failed')

    def UploadFileBT_Push(self):
        print('UploadFileBT_Push')
        file_list = []
        get_file_list = self.uploadListView.selectedIndexes()
        get_file_list.sort()

        print(get_file_list)

        for i in get_file_list:
            file_list.append(i.data())
        if ftp.ftp_file_upload('command', '/local/inspection/' + self.PanIDLineEdit.text() + '/command', file_list, time_out_state=self.timeoutCheckBox.isChecked(), time_out_time=self.timeoutLineEdit.text(), evenc_func=self.remove_file_cheker):
            mainStatusBar.showMessage('FTP File Upload Done')
            uploaddoneList = QStandardItemModel()
            for i in file_list:
                uploaddoneList.appendRow(QStandardItem(i))
            self.uploadfilelistListView.setModel(uploaddoneList)
        else:
            mainStatusBar.showMessage('FTP File Upload Failed')

    def makeremotecommandlistview_Push(self):
        print('makeremotecommandlistview_Push')
        select_text = self.makeremotecommandlistview.selectedIndexes()
        print(type(select_text[0].data()))
        self.makeremotecommandLineEdit.setText(select_text[0].data())

    def makeremotecommandBT_Push(self):
        print('makeremotecommandBT_Push')
        rm_file = os.listdir('command')
        for i in rm_file:
            os.remove('command/' + i)
        for index, i in enumerate(self.device_checkbox_list):
            if i.isChecked() == True:
                command_file_name = 'command' + str(index+1) + '.txt'
                f = open('command/' + command_file_name, 'w')
                f.write(self.makeremotecommandLineEdit.text())
                f.write('\n')
                f.close()
        upload_model = QStandardItemModel()
        file_list = os.listdir('./command')
        file_list.sort()
        for i in file_list:
            upload_model.appendRow(QStandardItem(i))
        self.uploadListView.setModel(upload_model)

    def deviceallCheckBox_Push(self):
        print('deviceallCheckBox_Push')
        for i in self.device_checkbox_list:
            i.setChecked(self.deviceallCheckBox.isChecked())

    def SaveBT_Push(self):
        print('SaveBT_Push')
        try:
            info_json = None
            save_name = self.FtpUrLineEdit.text()
            name_count = 1

            if os.path.isfile('login/info.txt'):
                f = open('login/info.txt', 'r')
                load_list = f.readlines()
                f.close()
                info_json = json.loads(load_list[0])
                if save_name in info_json.keys():
                    next_name = save_name + str(name_count)
                    name_count = name_count + 1
                    while next_name in info_json.keys():
                        next_name = save_name + str(name_count)
                        name_count = name_count + 1
                    save_name = next_name

                info_json[save_name] = {'host' : self.FtpUrLineEdit.text(), 'id' : self.FtpIdLineEdit.text(), 'pw' : self.FtpPasswordLineEdit.text(), 'port' : self.FtpPortLineEdit.text()}
            else:
                info_json = {save_name : {'host' : self.FtpUrLineEdit.text(), 'id' : self.FtpIdLineEdit.text(), 'pw' : self.FtpPasswordLineEdit.text(), 'port' : self.FtpPortLineEdit.text()}}

            json_data = json.dumps(info_json)

            f = open('login/info.txt', 'w')
            f.writelines(json_data)
            f.close()

            self.LoadComboBox.addItem(save_name)

        except:
            print('Save Error')

    def LoadComboBox_Push(self):
        print('LoadComboBox_Push')
        try:
            f = open('login/info.txt', 'r')
            json_data = f.readlines()
            f.close()
            info_json = json.loads(json_data[0])
            select_key = self.LoadComboBox.currentText()
            self.FtpUrLineEdit.setText(info_json[select_key]['host'])
            self.FtpIdLineEdit.setText(info_json[select_key]['id'])
            self.FtpPasswordLineEdit.setText(info_json[select_key]['pw'])
            self.FtpPortLineEdit.setText(info_json[select_key]['port'])
        except:
            print('Load Error')

class MainWindow(QMainWindow):
    # Global variables for the Program

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global mainStatusBar
        print('initUI')
        self.setGeometry(100, 100, 100, 100)
        self.statusBar()
        mainStatusBar = self.statusBar()
        mainStatusBar.showMessage('Ready...')

        self.mainWidgetUI = mainWidget()
        self.setCentralWidget(self.mainWidgetUI)

    def closeEvent(self, QCloseEvent):
        global thread_list
        print('Close')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("LoRa Recv Program")
    window.show()
    sys.exit(app.exec_())