#!/usr/bin/env python3
# encoding: utf-8
import os
import re
import cv2
import sys
import math
import time
import sqlite3
import threading
import resource_rc
from socket import * 
from ServoCmd import *
from ArmUi import Ui_Form
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)                               
        self.setWindowIcon(QIcon(':/images/Arm.png'))
        self.tabWidget.setCurrentIndex(0)  # 设置默认标签为第一个标签
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置选中整行，若不设置默认选中单元格
        self.message = QMessageBox()
        self.resetServos_ = False
        self.path = '/home/ubuntu/ArmPi_PC_Software/'
        self.actdir = self.path + "ActionGroups/"
        self.button_controlaction_clicked('reflash')
        ########################主界面###############################
        self.validator1 = QIntValidator(0, 1000)
        self.lineEdit_1.setValidator(self.validator1)
        self.lineEdit_2.setValidator(self.validator1)
        self.lineEdit_3.setValidator(self.validator1)
        self.lineEdit_4.setValidator(self.validator1)
        self.lineEdit_5.setValidator(self.validator1)
        self.lineEdit_6.setValidator(self.validator1)

        # 滑竿同步对应文本框的数值,及滑竿控制相应舵机转动与valuechange函数绑定
        self.horizontalSlider_1.valueChanged.connect(lambda: self.valuechange1('id1'))
        self.horizontalSlider_2.valueChanged.connect(lambda: self.valuechange1('id2'))
        self.horizontalSlider_3.valueChanged.connect(lambda: self.valuechange1('id3'))
        self.horizontalSlider_4.valueChanged.connect(lambda: self.valuechange1('id4'))
        self.horizontalSlider_5.valueChanged.connect(lambda: self.valuechange1('id5'))
        self.horizontalSlider_6.valueChanged.connect(lambda: self.valuechange1('id6'))

        self.horizontalSlider_11.valueChanged.connect(lambda: self.valuechange2('d1'))
        self.horizontalSlider_12.valueChanged.connect(lambda: self.valuechange2('d2'))
        self.horizontalSlider_13.valueChanged.connect(lambda: self.valuechange2('d3'))
        self.horizontalSlider_14.valueChanged.connect(lambda: self.valuechange2('d4'))
        self.horizontalSlider_15.valueChanged.connect(lambda: self.valuechange2('d5'))
        self.horizontalSlider_16.valueChanged.connect(lambda: self.valuechange2('d6'))
        
        self.radioButton_zn.toggled.connect(lambda: self.language(self.radioButton_zn))
        self.radioButton_en.toggled.connect(lambda: self.language(self.radioButton_en))        
        self.radioButton_zn.setChecked(True)
        self.chinese = True
        
        # tableWidget点击获取定位的信号与icon_position函数（添加运行图标）绑定
        self.tableWidget.pressed.connect(self.icon_position)

        self.validator3 = QIntValidator(20, 30000)
        self.lineEdit_time.setValidator(self.validator3)

        # 将编辑动作组的按钮点击时的信号与button_editaction_clicked函数绑定
        self.Button_ServoPowerDown.pressed.connect(lambda: self.button_editaction_clicked('servoPowerDown'))
        self.Button_AngularReadback.pressed.connect(lambda: self.button_editaction_clicked('angularReadback'))
        self.Button_AddAction.pressed.connect(lambda: self.button_editaction_clicked('addAction'))
        self.Button_DelectAction.pressed.connect(lambda: self.button_editaction_clicked('delectAction'))
        self.Button_DelectAllAction.pressed.connect(lambda: self.button_editaction_clicked('delectAllAction'))                                                 
        self.Button_UpdateAction.pressed.connect(lambda: self.button_editaction_clicked('updateAction'))
        self.Button_InsertAction.pressed.connect(lambda: self.button_editaction_clicked('insertAction'))
        self.Button_MoveUpAction.pressed.connect(lambda: self.button_editaction_clicked('moveUpAction'))
        self.Button_MoveDownAction.pressed.connect(lambda: self.button_editaction_clicked('moveDownAction'))        

        # 将运行及停止运行按钮点击的信号与button_runonline函数绑定
        self.Button_Run.clicked.connect(lambda: self.button_run('run'))

        self.Button_OpenActionGroup.pressed.connect(lambda: self.button_flie_operate('openActionGroup'))
        self.Button_SaveActionGroup.pressed.connect(lambda: self.button_flie_operate('saveActionGroup'))
        self.Button_ReadDeviation.pressed.connect(lambda: self.button_flie_operate('readDeviation'))
        self.Button_DownloadDeviation.pressed.connect(lambda: self.button_flie_operate('downloadDeviation'))
        self.Button_TandemActionGroup.pressed.connect(lambda: self.button_flie_operate('tandemActionGroup'))
        self.Button_ReSetServos.pressed.connect(lambda: self.button_re_clicked('reSetServos'))
        
        # 将控制动作的按钮点击的信号与action_control_clicked函数绑定
        self.Button_DelectSingle.pressed.connect(lambda: self.button_controlaction_clicked('delectSingle'))
        self.Button_AllDelect.pressed.connect(lambda: self.button_controlaction_clicked('allDelect'))
        self.Button_RunAction.pressed.connect(lambda: self.button_controlaction_clicked('runAction'))
        self.Button_StopAction.pressed.connect(lambda: self.button_controlaction_clicked('stopAction'))
        self.Button_Reflash.pressed.connect(lambda: self.button_controlaction_clicked('reflash'))
        self.Button_Quit.pressed.connect(lambda: self.button_controlaction_clicked('quit'))

        self.devNew = [0, 0, 0, 0, 0, 0]
        self.dev_change = False 
        self.readDevOk = False
        self.totalTime = 0
        self.row = 0
        #################################副界面1#######################################
        self.id = 0
        self.dev = 0
        self.servoTemp = 0
        self.servoMin = 0
        self.servoMax = 0
        self.servoMinV = 0
        self.servoMaxV = 0
        self.servoMove = 0
        self.horizontalSlider_servoTemp.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoTemp'))
        self.horizontalSlider_servoMin.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoMin'))
        self.horizontalSlider_servoMax.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoMax'))
        self.horizontalSlider_servoMinV.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoMinV'))
        self.horizontalSlider_servoMaxV.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoMaxV'))
        self.horizontalSlider_servoMove.valueChanged.connect(lambda: self.horizontalSlider_valuechange('servoMove'))

        self.pushButton_read.pressed.connect(lambda: self.button_clicked('read'))
        self.pushButton_set.pressed.connect(lambda: self.button_clicked('set'))
        self.pushButton_default.pressed.connect(lambda: self.button_clicked('default'))
        self.pushButton_quit2.pressed.connect(lambda: self.button_clicked('quit2'))
        self.pushButton_resetPos.pressed.connect(lambda: self.button_clicked('resetPos'))
        
        self.validator2 = QIntValidator(-125, 125)
        self.lineEdit_servoDev.setValidator(self.validator2)
        
        self.tabWidget.currentChanged['int'].connect(self.tabchange)
        self.readOrNot = False
        
    # 弹窗提示函数
    def message_from(self, str):
        try:
            QMessageBox.about(self, '', str)
            time.sleep(0.01)
        except:
            pass
    
    def message_From(self, str):
        self.message_from(str)
#     
    # 弹窗提示函数
    def message_delect(self, str):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(' ')
        messageBox.setText(str)
        messageBox.addButton(QPushButton('OK'), QMessageBox.YesRole)
        messageBox.addButton(QPushButton('Cancel'), QMessageBox.NoRole)
        return messageBox.exec_()

    # 窗口退出
    def closeEvent(self, e):        
        result = QMessageBox.question(self,
                                    "关闭窗口提醒",
                                    "exit?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if result == QMessageBox.Yes:
            self.camera_ui = True
            self.camera_ui_break = True
            QWidget.closeEvent(self, e)
        else:
            e.ignore()
    
    def language(self, name):
        if name.text() == '中文':
            self.chinese = True
            Ui_Form.retranslateUi(self, self)
        else:
            self.chinese = False
            Ui_Form.englishUi(self)
            
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.resetServos_ = True
            servo1_pulse = int(self.lineEdit_1.text())
            servo2_pulse = int(self.lineEdit_2.text())
            servo3_pulse = int(self.lineEdit_3.text())
            servo4_pulse = int(self.lineEdit_4.text())
            servo5_pulse = int(self.lineEdit_5.text())
            servo6_pulse = int(self.lineEdit_6.text())
            self.horizontalSlider_1.setValue(servo1_pulse)
            self.horizontalSlider_2.setValue(servo2_pulse)
            self.horizontalSlider_3.setValue(servo3_pulse)
            self.horizontalSlider_4.setValue(servo4_pulse)
            self.horizontalSlider_5.setValue(servo5_pulse)
            self.horizontalSlider_6.setValue(servo6_pulse)
            
            setServoPulse(1, servo1_pulse, 500)
            setServoPulse(2, servo2_pulse, 500)
            setServoPulse(3, servo3_pulse, 500)
            setServoPulse(4, servo4_pulse, 500)
            setServoPulse(5, servo5_pulse, 500)
            setServoPulse(6, servo6_pulse, 500)
            self.resetServos_ = False
    
    def tabchange(self):
        if self.tabWidget.currentIndex() == 1:
            if self.chinese:
                self.message_From('使用此面板时，请确保只连接了一个舵机，否则会引起冲突！')
            else:
                self.message_From('Before debugging servo,make sure that the servo controller is connected with ONE servo.Otherwise it may cause a conflict!')
        
    
    # 滑竿同步对应文本框的数值,及滑竿控制相应舵机转动
    def valuechange1(self, name):
        if not self.resetServos_:
            if name == 'id1':
                servoAngle = str(self.horizontalSlider_1.value())
                self.lineEdit_1.setText(servoAngle)
                setServoPulse(1, int(servoAngle), 20)
            if name == 'id2':
                servoAngle = str(self.horizontalSlider_2.value())
                self.lineEdit_2.setText(servoAngle)
                setServoPulse(2, int(servoAngle), 20)
            if name == 'id3':
                servoAngle = str(self.horizontalSlider_3.value())
                self.lineEdit_3.setText(servoAngle)
                setServoPulse(3, int(servoAngle), 20)
            if name == 'id4':
                servoAngle = str(self.horizontalSlider_4.value())
                self.lineEdit_4.setText(servoAngle)
                setServoPulse(4, int(servoAngle), 20)
            if name == 'id5':
                servoAngle = str(self.horizontalSlider_5.value())
                self.lineEdit_5.setText(servoAngle)
                setServoPulse(5, int(servoAngle), 20)
            if name == 'id6':
                servoAngle = str(self.horizontalSlider_6.value())
                self.lineEdit_6.setText(servoAngle)
                setServoPulse(6, int(servoAngle), 20)

    def valuechange2(self, name):
        if name == 'd1':
            self.devNew[0] = self.horizontalSlider_11.value()
            self.label_d1.setText(str(self.devNew[0]))
            setServoDeviation(1, self.devNew[0])
            if self.devNew[0] < 0:
                self.devNew[0] = 0xff + self.devNew[0] + 1            
        if name == 'd2':
            self.devNew[1] = self.horizontalSlider_12.value()
            self.label_d2.setText(str(self.devNew[1]))
            setServoDeviation(2, self.devNew[1])
            if self.devNew[1] < 0:
                self.devNew[1] = 0xff + self.devNew[1] + 1                  
        if name == 'd3':
            self.devNew[2] = self.horizontalSlider_13.value()
            self.label_d3.setText(str(self.devNew[2]))
            setServoDeviation(3, self.devNew[2])
            if self.devNew[2] < 0:
                self.devNew[2] = 0xff + self.devNew[2] + 1            
        if name == 'd4':
            self.devNew[3] = self.horizontalSlider_14.value()
            self.label_d4.setText(str(self.devNew[3]))
            setServoDeviation(4, self.devNew[3])
            if self.devNew[3] < 0:
                self.devNew[3] = 0xff + self.devNew[3] + 1           
        if name == 'd5':
            self.devNew[4] = self.horizontalSlider_15.value()
            self.label_d5.setText(str(self.devNew[4]))
            setServoDeviation(5, self.devNew[4])
            if self.devNew[4] < 0:
                self.devNew[4] = 0xff + self.devNew[4] + 1                  
        if name == 'd6':
            self.devNew[5] = self.horizontalSlider_16.value()
            self.label_d6.setText(str(self.devNew[5]))
            setServoDeviation(6, self.devNew[5])
            if self.devNew[5] < 0:
                self.devNew[5] = 0xff + self.devNew[5] + 1
                     
    # 复位按钮点击事件
    def button_re_clicked(self, name):
        self.resetServos_ = True
        if name == 'reSetServos':
            setServoPulse(1, 500, 1000)
            setServoPulse(2, 500, 1000)
            setServoPulse(3, 500, 1000)
            setServoPulse(4, 500, 1000)
            setServoPulse(5, 500, 1000)
            setServoPulse(6, 500, 1000)
            self.lineEdit_1.setText('500')
            self.lineEdit_2.setText('500')
            self.lineEdit_3.setText('500')
            self.lineEdit_4.setText('500')
            self.lineEdit_5.setText('500')
            self.lineEdit_6.setText('500')                    

            self.horizontalSlider_1.setValue(500)
            self.horizontalSlider_2.setValue(500)
            self.horizontalSlider_3.setValue(500)
            self.horizontalSlider_4.setValue(500)
            self.horizontalSlider_5.setValue(500)
            self.horizontalSlider_6.setValue(500)    
            self.resetServos_ = False

    # 选项卡选择标签状态，获取对应舵机数值
    def tabindex(self, index):       
        return  [str(self.horizontalSlider_1.value()), str(self.horizontalSlider_2.value()),
                 str(self.horizontalSlider_3.value()), str(self.horizontalSlider_4.value()),
                 str(self.horizontalSlider_5.value()), str(self.horizontalSlider_6.value())]
    
    def getIndexData(self, index):
        data = []
        for j in range(2, self.tableWidget.columnCount()):
            data.append(str(self.tableWidget.item(index, j).text()))
        return data
    
    # 往tableWidget表格添加一行数据的函数
    def add_line(self, item, timer, id1, id2, id3, id4, id5, id6):
        self.tableWidget.setItem(item, 1, QtWidgets.QTableWidgetItem(str(item + 1)))
        self.tableWidget.setItem(item, 2, QtWidgets.QTableWidgetItem(timer))
        self.tableWidget.setItem(item, 3, QtWidgets.QTableWidgetItem(id1))
        self.tableWidget.setItem(item, 4, QtWidgets.QTableWidgetItem(id2))
        self.tableWidget.setItem(item, 5, QtWidgets.QTableWidgetItem(id3))
        self.tableWidget.setItem(item, 6, QtWidgets.QTableWidgetItem(id4))
        self.tableWidget.setItem(item, 7, QtWidgets.QTableWidgetItem(id5))
        self.tableWidget.setItem(item, 8, QtWidgets.QTableWidgetItem(id6))

    # 在定位行添加运行图标按钮
    def icon_position(self):
        toolButton_run = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/index.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        toolButton_run.setIcon(icon)
        toolButton_run.setObjectName("toolButton_run")
        item = self.tableWidget.currentRow()
        self.tableWidget.setCellWidget(item, 0, toolButton_run)
        for i in range(self.tableWidget.rowCount()):
            if i != item:
                self.tableWidget.removeCellWidget(i, 0)
        toolButton_run.clicked.connect(self.action_one)

    def action_one(self):
        self.resetServos_ = True
        item = self.tableWidget.currentRow()
        alist = []
        try:
            timer = int(self.tableWidget.item(self.tableWidget.currentRow(), 2).text())

            for j in range(3, 9):
                alist.append(int(self.tableWidget.item(item, j).text()))
            setServoPulse(1, alist[0], timer)
            setServoPulse(2, alist[1], timer)
            setServoPulse(3, alist[2], timer)
            setServoPulse(4, alist[3], timer)
            setServoPulse(5, alist[4], timer)
            setServoPulse(6, alist[5], timer)
            self.horizontalSlider_1.setValue(alist[0])
            self.horizontalSlider_2.setValue(alist[1])
            self.horizontalSlider_3.setValue(alist[2])
            self.horizontalSlider_4.setValue(alist[3])
            self.horizontalSlider_5.setValue(alist[4])
            self.horizontalSlider_6.setValue(alist[5])
            self.lineEdit_1.setText(str(alist[0]))
            self.lineEdit_2.setText(str(alist[1]))
            self.lineEdit_3.setText(str(alist[2]))
            self.lineEdit_4.setText(str(alist[3]))
            self.lineEdit_5.setText(str(alist[4]))
            self.lineEdit_6.setText(str(alist[5]))             
        except BaseException as e:
            print(e)
            if self.chinese:
                self.message_From('运行出错')
            else:
                self.message_From('Running error')
        self.resetServos_ = False

    # 编辑动作组按钮点击事件
    def button_editaction_clicked(self, name):
        list = self.tabindex(self.tabWidget.currentIndex())
        RowCont = self.tableWidget.rowCount()
        item = self.tableWidget.currentRow()
        if name == 'servoPowerDown':
            for id in range(1, 7):
                unloadServo(id)
            if self.chinese:
                self.message_From('掉电成功')
            else:
                self.message_From('success')
        if name == 'angularReadback':
            self.tableWidget.insertRow(RowCont)    # 增加一行
            self.tableWidget.selectRow(RowCont)    # 定位最后一行为选中行
            use_time = int(self.lineEdit_time.text())
            data = [RowCont, str(use_time)]
            for i in range(1, 7):
                pulse = getServoPulse(i)
                if pulse is None:
                    return
                else:
                    data.append(str(pulse))                                       
            if use_time < 20:
                if self.chinese:
                    self.message_From('运行时间必须大于20ms')
                else:
                    self.message_From('Run time must be greater than 20ms')
                return         
            self.add_line(data[0], date[1], data[2], data[3], data[4], data[5], data[6], data[7])
            self.totalTime += use_time
            self.label_TotalTime.setText(str((self.totalTime)/1000.0))            
        if name == 'addAction':    # 添加动作
            if int(self.lineEdit_time.text()) < 20:
                if self.chinese:
                    self.message_From('运行时间必须大于20')
                else:
                    self.message_From('Run time must greater than 20')
                return
            self.tableWidget.insertRow(RowCont)    # 增加一行
            self.tableWidget.selectRow(RowCont)    # 定位最后一行为选中行
            self.add_line(RowCont, str(self.lineEdit_time.text()), list[0], list[1], list[2], list[3], list[4], list[5])
            self.totalTime += int(self.lineEdit_time.text())
            self.label_TotalTime.setText(str((self.totalTime)/1000.0))
        if name == 'delectAction':    # 删除动作
            if RowCont != 0:
                self.totalTime -= int(self.tableWidget.item(item, 2).text())
                self.tableWidget.removeRow(item)  # 删除选定行                
                self.label_TotalTime.setText(str((self.totalTime)/1000.0))
        if name == 'delectAllAction':
            result = self.message_delect('此操作会删除列表中的所有动作，是否继续？')
            if result == 0:                              
                for i in range(RowCont):
                    self.tableWidget.removeRow(0)
                self.totalTime = 0
                self.label_TotalTime.setText(str(self.totalTime))
            else:
                pass          
        if name == 'updateAction':    # 更新动作
            if int(self.lineEdit_time.text()) < 20:
                if self.chinese:
                    self.message_From('运行时间必须大于20')
                else:
                    self.message_From('Run time must greater than 20')
                return

            self.add_line(item, str(self.lineEdit_time.text()), list[0], list[1], list[2], list[3], list[4], list[5])
            self.totalTime = 0
            for i in range(RowCont):
                self.totalTime += int(self.tableWidget.item(i,2).text())
            self.label_TotalTime.setText(str((self.totalTime)/1000.0))            
        if name == 'insertAction':    # 插入动作
            if item == -1:
                return
            if int(self.lineEdit_time.text()) < 20:
                if self.chinese:
                    self.message_From('运行时间必须大于20')
                else:
                    self.message_From('Run time must greater than 20')
                return

            self.tableWidget.insertRow(item)       # 插入一行
            self.tableWidget.selectRow(item)
            self.add_line(item, str(self.lineEdit_time.text()), list[0], list[1], list[2], list[3], list[4], list[5])
            self.totalTime += int(self.lineEdit_time.text())
            self.label_TotalTime.setText(str((self.totalTime)/1000.0))
        if name == 'moveUpAction':
            if item == 0 or item == -1:
                return
            current_data = self.getIndexData(item)
            uplist_data = self.getIndexData(item - 1)
            self.add_line(item - 1, current_data[0], current_data[1], current_data[2], current_data[3], current_data[4], current_data[5], current_data[6])
            self.add_line(item, uplist_data[0], uplist_data[1], uplist_data[2], uplist_data[3], uplist_data[4], uplist_data[5], uplist_data[6])
            self.tableWidget.selectRow(item - 1) 
        if name == 'moveDownAction':
            if item == RowCont - 1:
                return
            current_data = self.getIndexData(item)
            downlist_data = self.getIndexData(item + 1)           
            self.add_line(item + 1, current_data[0], current_data[1], current_data[2], current_data[3], current_data[4], current_data[5], current_data[6])
            self.add_line(item, downlist_data[0], downlist_data[1], downlist_data[2], downlist_data[3], downlist_data[4], downlist_data[5], downlist_data[6])
            self.tableWidget.selectRow(item + 1)
                             
        for i in range(self.tableWidget.rowCount()):    #刷新编号值
            self.tableWidget.item(i , 2).setFlags(self.tableWidget.item(i , 2).flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(i + 1)))
        self.icon_position()

    # 在线运行按钮点击事件
    def button_run(self, name):
        if self.tableWidget.rowCount() == 0:
            if self.chinese:
                self.message_From('请先添加动作!')
            else:
                self.message_From('Add action first!')
        else:
            if name == 'run':
                 if self.Button_Run.text() == '运行' or self.Button_Run.text() == 'Run':
                    if self.chinese:
                        self.Button_Run.setText('停止')
                    else:
                        self.Button_Run.setText('Stop')
                    self.row = self.tableWidget.currentRow()
                    self.tableWidget.selectRow(self.row)
                    self.icon_position()
                    self.timer = QTimer()
                    self.action_online(self.row)
                    if self.checkBox.isChecked():
                        for i in range(self.tableWidget.rowCount() - self.row):
                            s = self.tableWidget.item(i,2).text()
                            self.timer.start(int(s))       # 设置计时间隔并启动
                        self.timer.timeout.connect(self.operate1)
                    else:
                        for i in range(self.tableWidget.rowCount() - self.row):
                            s = self.tableWidget.item(i,2).text()
                            self.timer.start(int(s))       # 设置计时间隔并启动
                        self.timer.timeout.connect(self.operate2)
                 elif self.Button_Run.text() == '停止' or self.Button_Run.text() == 'Stop':
                    self.timer.stop()
                    if self.chinese:
                        self.Button_Run.setText('运行')
                        self.message_From('运行结束!')
                    else:
                        self.Button_Run.setText('Run')
                        self.message_From('Run over!')  
            
    def operate1(self):
        item = self.tableWidget.currentRow()
        if item == self.tableWidget.rowCount() - 1:
            self.tableWidget.selectRow(self.row)
            self.action_online(self.row)
        else:
            self.tableWidget.selectRow(item + 1)
            self.action_online(item + 1)
        self.icon_position()

    def operate2(self):
        item = self.tableWidget.currentRow()
        if item == self.tableWidget.rowCount() - 1:
            self.timer.stop()
            if self.chinese:
                self.Button_Run.setText('运行')
                self.message_From('运行结束!')
            else:
                self.Button_Run.setText('Run')
                self.message_From('Run over!') 
        else:
            self.tableWidget.selectRow(item + 1)
            self.action_online(item + 1)
        self.icon_position()

    def action_online(self, item):
        try:
            timer = int(self.tableWidget.item(item, 2).text())
            data = [timer, 6]
            for j in range(1, 7):
                data.extend([j, int(self.tableWidget.item(item, j+2).text())])
                setServoPulse(j, int(self.tableWidget.item(item, j+2).text()), timer)     
        except Exception:
            self.timer.stop()
            if self.chinese:
                self.Button_Run.setText('运行')
                self.message_From('运行出错!')
            else:
                self.Button_Run.setText('Run')
                self.message_From('Run error!')              

    # 文件打开及保存按钮点击事件
    def button_flie_operate(self, name):
        try:            
            if name == 'openActionGroup':
                dig_o = QFileDialog()
                dig_o.setFileMode(QFileDialog.ExistingFile)
                dig_o.setNameFilter('d6a Flies(*.d6a)')
                openfile = dig_o.getOpenFileName(self, 'OpenFile', '', 'd6a Flies(*.d6a)')
                # 打开单个文件
                # 参数一：设置父组件；参数二：QFileDialog的标题
                # 参数三：默认打开的目录，“.”点表示程序运行目录，/表示当前盘符根目录
                # 参数四：对话框的文件扩展名过滤器Filter，比如使用 Image files(*.jpg *.gif) 表示只能显示扩展名为.jpg或者.gif文件
                # 设置多个文件扩展名过滤，使用双引号隔开；“All Files(*);;PDF Files(*.pdf);;Text Files(*.txt)”
                path = openfile[0]
                try:
                    if path != '':
                        rbt = QSqlDatabase.addDatabase("QSQLITE")
                        rbt.setDatabaseName(path)
                        if rbt.open():
                            actgrp = QSqlQuery()
                            if (actgrp.exec("select * from ActionGroup ")):
                                self.tableWidget.setRowCount(0)
                                self.tableWidget.clearContents()
                                self.totalTime = 0
                                while (actgrp.next()):
                                    count = self.tableWidget.rowCount()
                                    self.tableWidget.setRowCount(count + 1)
                                    for i in range(8):
                                        self.tableWidget.setItem(count, i + 1, QtWidgets.QTableWidgetItem(str(actgrp.value(i))))
                                        if i == 1:
                                            self.totalTime += actgrp.value(i)
                                        self.tableWidget.update()
                                        self.tableWidget.selectRow(count)
                                    self.tableWidget.item(count , 2).setFlags(self.tableWidget.item(count , 2).flags() & ~Qt.ItemIsEditable)                                        
                        self.icon_position()
                        rbt.close()
                        self.label_TotalTime.setText(str(self.totalTime/1000.0))
                except:
                    if self.chinese:
                        self.message_From('动作组错误')
                    else:
                        self.message_From('Wrong action format')
                    
            if name == 'saveActionGroup':
                dig_s = QFileDialog()
                if self.tableWidget.rowCount() == 0:
                    if self.chinese:
                        self.message_From('动作列表是空的哦，没啥要保存的')
                    else:
                        self.message_From('The action list is empty，nothing to save')
                    return
                savefile = dig_s.getSaveFileName(self, 'Savefile', '', 'd6a Flies(*.d6a)')
                path = savefile[0]
                if os.path.isfile(path):
                    os.system('sudo rm ' + path)
                if path != '':                    
                    if path[-4:] == '.d6a':
                        conn = sqlite3.connect(path)
                    else:
                        conn = sqlite3.connect(path + '.d6a')
                    
                    c = conn.cursor()                    
                    c.execute('''CREATE TABLE ActionGroup([Index] INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL ON CONFLICT FAIL
                    UNIQUE ON CONFLICT ABORT,
                    Time INT,
                    Servo1 INT,
                    Servo2 INT,
                    Servo3 INT,
                    Servo4 INT,
                    Servo5 INT,
                    Servo6 INT);''')                      
                    for i in range(self.tableWidget.rowCount()):
                        insert_sql = "INSERT INTO ActionGroup(Time, Servo1, Servo2, Servo3, Servo4, Servo5, Servo6) VALUES("
                        for j in range(2, self.tableWidget.columnCount()):
                            if j == self.tableWidget.columnCount() - 1:
                                insert_sql += str(self.tableWidget.item(i, j).text())
                            else:
                                insert_sql += str(self.tableWidget.item(i, j).text()) + ','
                        
                        insert_sql += ");"
                        c.execute(insert_sql)
                    
                    conn.commit()
                    conn.close()
                    self.button_controlaction_clicked('reflash')
            if name == 'readDeviation':
                id = ''
                self.readDevOk = True
                dev_data = []
                for i in range(1, 7):
                    dev = getServoDeviation(i)
                    if dev == 999:
                        dev_data.append(0)
                        id += (' id' + str(i))
                    elif dev > 125:  # 负数
                        dev_data.append(-(0xff - (dev - 1)))                        
                    else:
                        dev_data.append(dev)
                self.horizontalSlider_11.setValue(dev_data[0])
                self.horizontalSlider_12.setValue(dev_data[1])
                self.horizontalSlider_13.setValue(dev_data[2])
                self.horizontalSlider_14.setValue(dev_data[3])
                self.horizontalSlider_15.setValue(dev_data[4])
                self.horizontalSlider_16.setValue(dev_data[5])
                    
                if id == '':
                    if self.chinese:
                        self.message_From('读取偏差成功!')
                    else:
                        self.message_From('success!')
                else:
                    if self.chinese:
                        self.message_From(id + '号舵机偏差读取失败!')
                    else:
                        self.message_From('Failed to read the deviation of' + id)
            if name == 'downloadDeviation':
                if self.readDevOk:                    
                    for id in range(1, 7):
                        saveServoDeviation(id)
                    if self.chinese:
                        self.message_From('下载偏差成功!')
                    else:
                        self.message_From('success!')
                else:
                    if self.chinese:
                        self.message_From('请先读取偏差！')
                    else:
                        self.message_From('Please read the deviation first！')
            if name == 'tandemActionGroup':
                dig_t = QFileDialog()
                dig_t.setFileMode(QFileDialog.ExistingFile)
                dig_t.setNameFilter('d6a Flies(*.d6a)')
                openfile = dig_t.getOpenFileName(self, 'OpenFile', '', 'd6a Flies(*.d6a)')
                # 打开单个文件
                # 参数一：设置父组件；参数二：QFileDialog的标题
                # 参数三：默认打开的目录，“.”点表示程序运行目录，/表示当前盘符根目录
                # 参数四：对话框的文件扩展名过滤器Filter，比如使用 Image files(*.jpg *.gif) 表示只能显示扩展名为.jpg或者.gif文件
                # 设置多个文件扩展名过滤，使用双引号隔开；“All Files(*);;PDF Files(*.pdf);;Text Files(*.txt)”
                path = openfile[0]
                try:
                    if path != '':
                        tbt = QSqlDatabase.addDatabase("QSQLITE")
                        tbt.setDatabaseName(path)
                        if tbt.open():
                            actgrp = QSqlQuery()
                            if (actgrp.exec("select * from ActionGroup ")):
                                while (actgrp.next()):
                                    count = self.tableWidget.rowCount()
                                    self.tableWidget.setRowCount(count + 1)
                                    for i in range(8):
                                        if i == 0:
                                            self.tableWidget.setItem(count, i + 1, QtWidgets.QTableWidgetItem(str(count + 1)))
                                        else:                      
                                            self.tableWidget.setItem(count, i + 1, QtWidgets.QTableWidgetItem(str(actgrp.value(i))))
                                        if i == 1:
                                            self.totalTime += actgrp.value(i)
                                        self.tableWidget.update()
                                        self.tableWidget.selectRow(count)
                                    self.tableWidget.item(count , 2).setFlags(self.tableWidget.item(count , 2).flags() & ~Qt.ItemIsEditable)
                        self.icon_position()
                        tbt.close()
                        self.label_TotalTime.setText(str(self.totalTime/1000.0))
                except:
                    if self.chinese:
                        self.message_From('动作组错误')
                    else:
                        self.message_From('Wrong action format')
        except BaseException as e:
            print(e)

    def listActions(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        pathlist = os.listdir(path)
        actList = []
        
        for f in pathlist:
            if f[0] == '.':
                pass
            else:
                if f[-4:] == '.d6a':
                    f.replace('-', '')
                    if f:
                        actList.append(f[0:-4])
                else:
                    pass
        return actList
    
    def reflash_action(self):
        actList = self.listActions(self.actdir)
        actList.sort()
        
        if len(actList) != 0:        
            self.comboBox_action.clear()
            for i in range(0, len(actList)):
                self.comboBox_action.addItem(actList[i])
        else:
            self.comboBox_action.clear()
    
    # 控制动作组按钮点击事件
    def button_controlaction_clicked(self, name):
        if name == 'delectSingle':
            if str(self.comboBox_action.currentText()) != "":
                os.remove(self.actdir + str(self.comboBox_action.currentText()) + ".d6a")            
                self.reflash_action()
        if name == 'allDelect':
            result = self.message_delect('此操作会删除所有动作组，是否继续？')
            if result == 0:                              
                actList = self.listActions(self.actdir)
                for d in actList:
                    os.remove(self.actdir + d + '.d6a')
            else:
                pass
            self.reflash_action()
        if name == 'runAction':   # 动作组运行
            runActionGroup(self.comboBox_action.currentText())            
        if name == 'stopAction':   # 停止运行
            stopActionGroup()
        if name == 'reflash':
            self.reflash_action()
        if name == 'quit':
            self.camera_ui = True
            self.camera_ui_break = True
            try:
                self.cap.release()
            except:
                pass
            sys.exit()

    ################################################################################################
    def horizontalSlider_valuechange(self, name):
        if name == 'servoTemp':
            self.temp = str(self.horizontalSlider_servoTemp.value())
            self.label_servoTemp.setText(self.temp + '℃')
        if name == 'servoMin':
            self.servoMin = str(self.horizontalSlider_servoMin.value())
            self.label_servoMin.setText(self.servoMin)
        if name == 'servoMax':
            self.servoMax = str(self.horizontalSlider_servoMax.value())
            self.label_servoMax.setText(self.servoMax)
        if name == 'servoMinV':
            self.servoMinV = str(self.horizontalSlider_servoMinV.value()/10)
            self.label_servoMinV.setText(self.servoMinV + 'V')
        if name == 'servoMaxV':
            self.servoMaxV = str(self.horizontalSlider_servoMaxV.value()/10)
            self.label_servoMaxV.setText(self.servoMaxV + 'V')
        if name == 'servoMove':
            self.servoMove = str(self.horizontalSlider_servoMove.value())            
            self.label_servoMove.setText(self.servoMove)
            setServoPulse(self.id, int(self.servoMove), 0)
    
    def button_clicked(self, name):
        if name == 'read':
            try:
                self.id = getBusServoID()
                if self.id is None:
                    if self.chinese:
                        self.message_From('读取id失败')
                    else:
                        self.message_From('Failed to read ID')
                    return
                self.readOrNot = True
                self.dev = getServoDeviation(self.id)
                if self.dev > 125:
                    self.dev = -(0xff-(self.dev - 1))
                self.servoTemp = getBusServoTempLimit(self.id)
                (self.servoMin, self.servoMax) = getBusServoAngleLimit(self.id)
                (self.servoMinV, self.servoMaxV) = getBusServoVinLimit(self.id)
                self.servoMove = getServoPulse(self.id)
                
                currentVin = getBusServoVin(self.id)

                currentTemp = getBusServoTemp(self.id)

                self.lineEdit_servoID.setText(str(self.id))
                self.lineEdit_servoDev.setText(str(self.dev))
                
                self.horizontalSlider_servoTemp.setValue(self.servoTemp)
                self.horizontalSlider_servoMin.setValue(self.servoMin)
                self.horizontalSlider_servoMax.setValue(self.servoMax)
                MinV = self.servoMinV
                MaxV = self.servoMaxV            
                self.horizontalSlider_servoMinV.setValue(int(MinV/100))
                self.horizontalSlider_servoMaxV.setValue(int(MaxV/100))

                self.label_servoCurrentP.setText(str(self.servoMove))
                self.label_servoCurrentV.setText(str(round(currentVin/1000.0, 2)) + 'V')
                self.label_servoCurrentTemp.setText(str(currentTemp) + '℃')

                self.horizontalSlider_servoMove.setValue(self.servoMove)
            except:
                if self.chinese:
                    self.message_From('读取超时')
                else:
                    self.message_From('Read timeout')
                return
            if self.chinese:
                self.message_From('读取成功')
            else:
                self.message_From('success')
            
        if name == 'set':
            if self.readOrNot is False:
                if self.chinese:
                    self.message_From('请先读取，否则无法获取舵机信息，从而进行设置！')
                else:
                    self.message_From('Read first！')
                return
            id = self.lineEdit_servoID.text()
            if id == '':
                if self.chinese:
                    self.message_From('舵机id参数为空，无法设置')
                else:
                    self.message_From('Please input id')
                return           
            dev = self.lineEdit_servoDev.text()
            if dev is '':
                dev = 0
            dev = int(dev)
            if dev > 125 or dev < -125:
                if self.chinese:
                    self.message_From('偏差参数超出可调节范围-125～125，无法设置')
                else:
                    self.message_From('Deviation out of range -125~125')
                return          
            temp = self.horizontalSlider_servoTemp.value()
            pos_min = self.horizontalSlider_servoMin.value()
            pos_max = self.horizontalSlider_servoMax.value()
            if pos_min > pos_max:
                if self.chinese:
                    self.message_From('舵机范围参数错误，无法设置')
                else:
                    self.message_From('Wrong angle range')
                return
            vin_min = self.horizontalSlider_servoMinV.value()
            vin_max = self.horizontalSlider_servoMaxV.value()
            if vin_min > vin_max:
                if self.chinese:
                    self.message_From('舵机电压范围参数错误，无法设置')
                else:
                    self.message_From('Wrong voltage range')
                return
            pos = self.horizontalSlider_servoMove.value()
            
            id = int(id)
            
            try:
                setBusServoID(self.id, id)
                time.sleep(0.01)
                if getBusServoID() != id:
                    if self.chinese:
                        self.message_From('id设置失败！')
                    else:
                        self.message_From('failed！')
                    return
                setBusServoDeviation(id, dev)
                time.sleep(0.01)
                saveServoDeviation(id)
                time.sleep(0.01)
                d = getServoDeviation(id)
                if d > 125:
                    d = -(0xff-(d - 1))               
                if d != dev:
                    if self.chinese:
                        self.message_From('偏差设置失败！')
                    else:
                        self.message_From('failed！')
                    return            
                setBusServoMaxTemp(id, temp)
                time.sleep(0.01)
                if getBusServoTempLimit(id) != temp:
                    if self.chinese:
                        self.message_From('温度设置失败！')
                    else:
                        self.message_From('failed！')

                    return 
                setBusServoAngleLimit(id, pos_min, pos_max)
                time.sleep(0.01)
                if getBusServoAngleLimit(id) != (pos_min, pos_max):
                    if self.chinese:
                        self.message_From('角度范围设置失败！')
                    else:
                        self.message_From('failed！')
                    return 
                setBusServoVinLimit(id, vin_min*100, vin_max*100)
                time.sleep(0.01)
                if getBusServoVinLimit(id) != (vin_min*100, vin_max*100):
                    if self.chinese:
                        self.message_From('电压范围设置失败！')
                    else:
                        self.message_From('failed！')
                    return 
                setServoPulse(id, pos, 0)
            except:
                if self.chinese:
                    self.message_From('设置超时!')
                else:
                    self.message_From('Timeout!')
                return                
            if self.chinese: 
                self.message_From('设置成功')
            else:
                self.message_From('success')

        if name == 'default':
            if self.readOrNot is False:
                if self.chinese:
                    self.message_From('请先读取，否则无法获取舵机信息，从而进行设置！')
                else:
                    self.message_From('Read first！')
                return
            try:
                setBusServoID(self.id, 1)
                time.sleep(0.01)
                if getBusServoID() != 1:
                    if self.chinese:
                        self.message_From('id设置失败！')
                    else:
                        self.message_From('failed！')
                    return
                setBusServoDeviation(1, 0)
                time.sleep(0.01)
                saveServoDeviation(1)
                time.sleep(0.01)
                if getServoDeviation(1) != 0:
                    if self.chinese:
                        self.message_From('偏差设置失败！')
                    else:
                        self.message_From('failed！')
                    return
                setBusServoMaxTemp(1, 85)
                time.sleep(0.01)
                if getBusServoTempLimit(1) != 85:
                    if self.chinese:
                        self.message_From('温度设置失败！')
                    else:
                        self.message_From('failed！')
                    return
                setBusServoAngleLimit(1, 0, 1000)
                time.sleep(0.01)
                if getBusServoAngleLimit(1) != (0, 1000):
                    if self.chinese:
                        self.message_From('角度范围设置失败！')
                    else:
                        self.message_From('failed！')
                    return          
                setBusServoVinLimit(1, 4500, 12000)
                time.sleep(0.01)
                if getBusServoVinLimit(1) != (4500, 12000):
                    if self.chinese:
                        self.message_From('电压范围设置失败！')
                    else:
                        self.message_From('failed！')
                    return             
                setServoPulse(1, 500, 0)
            except:
                if self.chinese:
                    self.message_From('设置超时!')
                else:
                    self.message_From('Timeout!')
                return
            if self.chinese:
                self.message_From('设置成功')
            else:
                self.message_From('success')
        if name == 'quit2':
            self.camera_ui = True
            self.camera_ui_break = True
            try:
                self.cap.release()
            except:
                pass          
            sys.exit()
        if name == 'resetPos':
            self.horizontalSlider_servoMove.setValue(500)
            setServoPulse(self.id, 500, 0)

if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
