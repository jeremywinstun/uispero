# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:49:27 2021

@author: Rio Alfandy
"""


from PyQt5 import QtWidgets,QtCore,QtGui
from ._robot import Ui_MainWindow
from ._status import Ui_status

import paho.mqtt.client as mqtt
    

class spero(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(spero, self).__init__(parent)
        self.setupUi(self)
        self.preparation()
        self.show()
        self.pb_auto.clicked.connect(self.pb_autoClicked)
        self.pb_manual.clicked.connect(self.pb_manualClicked)
        self.pb_shutdown.clicked.connect(self.pb_shutdownClicked)
        self.pb_roboton.clicked.connect(self.pb_robotonClicked)
        self.pb_robotoff.clicked.connect(self.pb_robotoffClicked)
        self.pb_uvon.clicked.connect(self.pb_uvonClicked)
        self.pb_uvoff.clicked.connect(self.pb_uvoffClicked)
        self.client=None
        self.konfig()

    def konfig(self):
        self.pub = "operator_status"
        self.sub = "status_robot"
        self.nickname = "Operator Robot"
        self.username = "operatorspero"
        self.password = "spero2"
        self.broker = "localhost"
        self.port = "1883"
        self.run()

    #def hideEvent(self, event):
        #self.done.emit()
    def pb_shutdownClicked(self):
        msgshut = "SHUTDOWN"
        self.client.publish(self.pub, msgshut)
    def pb_autoClicked(self):
        msgauto = "AUTO"
        self.client.publish(self.pub, msgauto)

    def pb_manualClicked(self):
        msgmanual = "MANUAL"
        self.client.publish(self.pub, msgmanual)

    def pb_robotonClicked(self):
        msgroboton = "GO"
        self.client.publish(self.pub, msgroboton)

    def pb_robotoffClicked(self):
        msgrobotoff = "STOP"
        self.client.publish(self.pub, msgrobotoff) 

    def pb_uvonClicked(self):
        msguvon = "ON"
        self.client.publish(self.pub, msguvon)

    def pb_uvoffClicked(self):
        msguvoff = "OFF"
        self.client.publish(self.pub, msguvoff)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("operator_status")

    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.username,self.password) 
        self.client.connect(self.broker, int(self.port), 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()  

    def preparation(self):
        self.initCallbacks()
        self.statusrobotShown = False

    def initCallbacks(self):
        self.actionRobot_Status.triggered.connect(self.statusrobot)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F5:
            self.statusrobot()
        event.accept()

    def donestatusrobot(self):
        self.statusrobotShown = False
        self.substatusrobot.close()
    def statusrobot(self):
        if self.statusrobotShown is False:
            self.wxstatusrobot = statusrobot(self)
            self.substatusrobot = QtWidgets.QMdiSubWindow(self.mdiArea)
            self.substatusrobot.setWidget(self.wxstatusrobot)
            self.substatusrobot.setMinimumSize(self.wxstatusrobot.width(), self.wxstatusrobot.height())
            self.substatusrobot.setMaximumSize(self.wxstatusrobot.width(), 65535)
            self.mdiArea.addSubWindow(self.substatusrobot)
            self.statusrobotShown = True
            self.wxstatusrobot.done.connect(self.donestatusrobot)
            self.substatusrobot.show()

class statusrobot(QtWidgets.QWidget, Ui_status):
    done = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(statusrobot, self).__init__(parent)
        self.setupUi(self)
        self.client = None
        self.konfigurasi()
        self.lcd = QtWidgets.QLCDNumber(self)
    def konfigurasi(self):
        self.nickname = "Operator Robot 2"
        self.username = "operatorspero"
        self.password = "spero2"
        self.broker = "192.168.1.197"
        self.port = "1883"
        self.run()
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe([("status_tegangan",0),("status_uv",0)])
    def on_message_uv(self, client, userdata, message):
        self.verticalLayout_3.addWidget(self.label_uv)
        msguv = str(message.payload.decode("utf-8"))
        self.label_uv.setText(msguv)
        print (msguv)
    def on_message_tegangan(self, client, userdata, message):
        msgv = str(message.payload.decode("utf-8"))
        self.lcd.setStyleSheet('background:red')
        self.verticalLayout_2.addWidget(self.lcd)
        self.lcd.display(msgv)
        print (msgv)
        self.a = float(msgv)
        self.b = 11.3
        if self.a<=self.b:
            self.label_baterai.setText("Baterai lemah mohon charge baterai")
        else:
            self.label_baterai.setText("Baterai Aman!")
        
    def run (self):
        self.client = mqtt.Client()
        self.client.message_callback_add("status_tegangan", self.on_message_tegangan)
        self.client.message_callback_add("status_uv", self.on_message_uv)
       # self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.username,self.password) 
        self.client.connect(self.broker, int(self.port), 60)
        self.client.loop_start()
    
    #def on_message(self, client, userdata, flags, message):

    #def hideEvent(self, event):
        #self.done.emit()       
