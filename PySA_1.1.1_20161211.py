# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtCore, QtGui
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as tick
tick.MultipleLocator(base=25.0)
from PIL import Image

#Tab_1###############################
path_data = ""#record loading calibrated data path
box = np.array([0,0],dtype=int)
times_box = 0 # count the times of plot 
stdlight = ""
times_cali_plot = 0 # count the times of line_plot
neon_data = np.array([671.70, 667.83, 659.90, 653.29, 650.65, 640.22, 638.30, 633.44,
                      630.48, 626.65, 621.73, 616.36, 614.31, 609.62, 607.43, 603.00,
                      597.55, 594.48, 588.19, 585.25, 540.06, 534.11,533.08],dtype=float)
sun_data_show = np.array(['Ha(C) 656.281', 'Na(D1) 589.592', 'Na(D2) 588.995','Hg(e) 546.073','Fe(E) 527.039',
                          'Mg(b1) 518.362','Mg(b2) 517.270','Mg(b4) 516.733','Fe(c) 495.761','Hb(F) 486.134',
                          'Fe(d) 466.814','Fe(e) 438.355','Hr(G") 434.047','Ca(g) 422.673','FeCa(G) 430.8',
                          'Hd(h) 410.175','Ca+(K) 393.368'],dtype=str)
sun_data = np.array([656.281, 589.592, 588.995, 546.073, 527.039, 518.362, 517.270, 516.733, 495.761,
                     486.134, 466.814, 438.355, 434.047, 422.673, 430.8, 410.175, 393.368],dtype=float)
x_p = np.array([],dtype=float)
y_nm = np.array([],dtype=float)
coef = np.array([],dtype=float)
cov = np.array([],dtype=float)
sigma = np.array([],dtype=float) 
#Tab_2###############################
abs_blank = np.array([],dtype=float)
abs_analyte = np.array([],dtype=float)
abs_analyte_number = 0
abs_input_name = np.array([],dtype=str)
abs_plot_number = 1

std_blank = np.array([],dtype=float)
std_std = np.array([],dtype=float)
std_std_number = 0
std_input_name = np.array([],dtype=str)
std_input_conc = np.array([],dtype=str)
std_plot_number = 1
std_max_wavelength = np.array([],dtype=float)#for auto select
std_select_wavelength = 0.0 #for manual select
std_max_abs = np.array([],dtype=float)#for abs. at select w_l
std_linregress = np.zeros(5)#slope,intercept,rvalue,pvalue,std_err 
std_analyte_result = np.array([],dtype=float)#store 2 item: abs unknown
#Tab_3###################################
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 710)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")        
################################################################
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)#let screen can be rolled
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1000, 740))       
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)#AlwaysOn        
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded) 
        self.scrollArea.setObjectName("scrollArea")              
        self.tabWidget = QtGui.QTabWidget(self.scrollArea)# (self.centralwidget)  
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 960, 700))
        font = QtGui.QFont() #set for tabwidget label
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setItalic(True)                
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")    
        self.scrollArea.setWidget(self.tabWidget)
        self.scrollArea.ensureWidgetVisible(self.tabWidget)        
###########################################################            
        self.tab_1 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_1, "Wavelength Calibration")            
        self.tab_1.setObjectName("tab_1")        
        self.groupBox_t1select = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1select.setGeometry(QtCore.QRect(17, 54, 340, 102))
        self.groupBox_t1select.setObjectName("groupBox_t1select")        
        self.label_4 = QtGui.QLabel(self.groupBox_t1select)#first label
        self.label_4.setGeometry(QtCore.QRect(15, 15, 340, 31))
        self.label_4.setObjectName("label_4")                
        self.pushButton = QtGui.QPushButton(self.tab_1)#load image
        self.pushButton.setGeometry(QtCore.QRect(14, 13, 110, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")        
        self.label = QtGui.QLabel(self.tab_1) #y2 pixel
        self.label.setGeometry(QtCore.QRect(31, 128, 112, 21))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.label_3 = QtGui.QLabel(self.tab_1) #y1 pixel
        self.label_3.setGeometry(QtCore.QRect(31, 101, 89, 21))
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setObjectName("label_3")         
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_1)# y1
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 100, 76, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtGui.QLineEdit(self.tab_1)#y2
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 127, 76, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_2.setFont(font)                
        self.label_7 = QtGui.QLabel(self.tab_1)#Image
        self.label_7.setGeometry(QtCore.QRect(133, 7, 63, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtGui.QLabel(self.tab_1) #size
        self.label_8.setGeometry(QtCore.QRect(133, 29, 61, 21))
        self.label_8.setObjectName("label_8")       
        self.label_9 = QtGui.QLabel(self.tab_1) #image path
        self.label_9.setGeometry(QtCore.QRect(182, 8, 870, 21))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtGui.QLabel(self.tab_1) #image size
        self.label_10.setGeometry(QtCore.QRect(172, 29, 138, 21))        
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)        
        self.label_9.setFont(font)        
        self.label_10.setFont(font)        
        self.pushButton_2 = QtGui.QPushButton(self.tab_1) #show profile without cali
        self.pushButton_2.setGeometry(QtCore.QRect(19, 166, 266, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtGui.QPushButton(self.tab_1)#ok groupBox_t1select
        self.pushButton_4.setGeometry(QtCore.QRect(267, 106, 61, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_2.setFont(font)        
        self.pushButton_4.setFont(font)

        self.groupBox_t1wc = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1wc.setGeometry(QtCore.QRect(17, 207, 400, 430))
        self.groupBox_t1wc.setObjectName("groupBox_t1wc")   
        self.stdLight = QtGui.QComboBox(self.groupBox_t1wc)
        self.stdLight.setGeometry(QtCore.QRect(15, 28, 192, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.stdLight.setFont(font)
        self.stdLight.setEditable(False)
        self.stdLight.setMaxVisibleItems(5)
        self.stdLight.setObjectName("stdLight")
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox_t1wc) #auto
        self.checkBox_4.setGeometry(QtCore.QRect(215, 27, 150, 31))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtGui.QCheckBox(self.groupBox_t1wc)# manual
        self.checkBox_5.setGeometry(QtCore.QRect(16, 57, 330, 31))
        self.checkBox_5.setObjectName("checkBox_5") 
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)     
        self.checkBox_4.setFont(font)   
        self.checkBox_5.setFont(font)     
        self.tableWidget = QtGui.QTableWidget(self.groupBox_t1wc)
        self.tableWidget.setGeometry(QtCore.QRect(14, 93, 375, 139))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(30)        
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)        
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(22, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(23, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(24, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(25, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(26, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(27, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(28, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(29, item)         
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)         
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(111)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(23)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(23)
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_t1wc) # calibrate
        self.pushButton_5.setGeometry(QtCore.QRect(17, 271, 103, 32))
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")        
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_t1wc)# save cali
        self.pushButton_6.setGeometry(QtCore.QRect(155, 271, 171, 32))
        self.pushButton_6.setObjectName("pushButton_6")  
        self.label_13 = QtGui.QLabel(self.groupBox_t1wc) #result
        self.label_13.setGeometry(QtCore.QRect(17, 308, 118, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setTextFormat(QtCore.Qt.PlainText)
        self.label_13.setObjectName("label_13")            
        self.label_14 = QtGui.QLabel(self.groupBox_t1wc) #result formula
        self.label_14.setGeometry(QtCore.QRect(18, 330, 380, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")

        self.groupBox_t1plot = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1plot.setGeometry(QtCore.QRect(440, 54, 480, 235))
        self.groupBox_t1plot.setObjectName("groupBox_t1plot")  
        self.pushButton_11 = QtGui.QPushButton(self.groupBox_t1plot)#current
        self.pushButton_11.setGeometry(QtCore.QRect(20, 28, 185, 32))        
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_10 = QtGui.QPushButton(self.groupBox_t1plot)#load cali
        self.pushButton_10.setGeometry(QtCore.QRect(276, 28, 185, 32))
        self.pushButton_10.setObjectName("pushButton_10")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_10.setFont(font)
        self.pushButton_11.setFont(font)
        self.label_16 = QtGui.QLabel(self.groupBox_t1plot)#show formula
        self.label_16.setGeometry(QtCore.QRect(95, 66, 460, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.pushButton_7 = QtGui.QPushButton(self.groupBox_t1plot) #plot long
        self.pushButton_7.setGeometry(QtCore.QRect(80, 140, 335, 32))        
        self.pushButton_7.setObjectName("pushButton_7")        
        self.pushButton_8 = QtGui.QPushButton(self.groupBox_t1plot) #save value
        self.pushButton_8.setGeometry(QtCore.QRect(36, 184, 155, 32))
        self.pushButton_8.setObjectName("pushButton_8") 
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_8.setFont(font)
        self.pushButton_7.setFont(font)        
        self.pushButton_9 = QtGui.QPushButton(self.groupBox_t1plot)#load and plot
        self.pushButton_9.setGeometry(QtCore.QRect(240, 184, 210, 32))
        self.pushButton_9.setObjectName("pushButton_9")       
        
        self.groupBox2 = QtGui.QGroupBox(self.tab_1) #plot pro with img
        self.groupBox2.setGeometry(QtCore.QRect(440, 301, 480, 150))#(x, y, l,w )
        font = QtGui.QFont()  
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox2.setFont(font)
        self.groupBox2.setObjectName("groupBox2")         
        self.checkBox_11 = QtGui.QCheckBox(self.groupBox2)#typ1
        self.checkBox_11.setGeometry(QtCore.QRect(10, 15, 400, 43))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.checkBox_11.setFont(font)
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_12 = QtGui.QCheckBox(self.groupBox2)#typ2
        self.checkBox_12.setGeometry(QtCore.QRect(10, 40, 400, 43))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.checkBox_12.setFont(font)
        self.checkBox_12.setObjectName("checkBox_12")         
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox2)#show peak label
        self.checkBox_3.setGeometry(QtCore.QRect(10, 105, 400, 43))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")        
        self.pushButton_20 = QtGui.QPushButton(self.groupBox2)#plot button
        self.pushButton_20.setGeometry(QtCore.QRect(245, 110, 130, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_20.setFont(font)
        self.pushButton_20.setObjectName("pushButton_20")          
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox2)
        self.lineEdit_4.setGeometry(QtCore.QRect(127, 78, 260, 23))###
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")       
        self.label_2 = QtGui.QLabel(self.groupBox2)
        self.label_2.setGeometry(QtCore.QRect(10, 78, 120, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")
   
        self.groupBox = QtGui.QGroupBox(self.tab_1)#readme
        self.groupBox.setGeometry(QtCore.QRect(440, 464, 480, 175))#(x, y, l,w )
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.README = QtGui.QTextEdit(self.groupBox)
        self.README.setGeometry(QtCore.QRect(8, 20, 464, 143))#(9, 20, 389, 286)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.README.setFont(font)
        self.README.setObjectName("README")
        self.README.setReadOnly(True)

###################################################################
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.plotProfile)
        self.pushButton_4.clicked.connect(self.plot_region)#plot region ok button
        self.stdLight.activated[str].connect(self.load_stdlight)
        self.checkBox_5.stateChanged.connect(self.show_ref_profile)
        self.pushButton_5.clicked.connect(self.calibrate)#calibrate button
        self.pushButton_11.clicked.connect(self.current_fomula)#current formula button
        self.pushButton_7.clicked.connect(self.plot_cali_profile)#plot cali.button
        self.pushButton_6.clicked.connect(self.Save_calibration_data) 
        self.pushButton_10.clicked.connect(self.Load_calibration_data) 
        self.pushButton_8.clicked.connect(self.Save_profile_value)
        self.pushButton_9.clicked.connect(self.Load_profile_value_plot)
        self.pushButton_20.clicked.connect(self.plot_profile_and_spectrum)
        readme(self)
######################################################################
######################################################################
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox_t2re = QtGui.QGroupBox(self.tab_2)#read me
        self.groupBox_t2re.setGeometry(QtCore.QRect(5, 556, 940, 111))
        self.groupBox_t2re.setObjectName("groupBox_t2re")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_t2re1 = QtGui.QTextEdit(self.groupBox_t2re)
        self.textEdit_t2re1.setGeometry(QtCore.QRect(9, 20, 338, 84))
        self.textEdit_t2re1.setFont(font)
        self.textEdit_t2re1.setObjectName("textEdit21_t2re1")
        self.textEdit_t2re1.setReadOnly(True)
        self.textEdit_t2re2 = QtGui.QTextEdit(self.groupBox_t2re)
        self.textEdit_t2re2.setGeometry(QtCore.QRect(388, 20, 540, 84))
        self.textEdit_t2re2.setFont(font)
        self.textEdit_t2re2.setObjectName("textEdit21_t2re2")  
        self.textEdit_t2re2.setReadOnly(True)
        ###############################################################
        self.groupBox_abs = QtGui.QGroupBox(self.tab_2)
        self.groupBox_abs.setGeometry(QtCore.QRect(4, 7, 340, 545))
        self.groupBox_abs.setObjectName("groupBox_abs")
        self.pushButton_abs1 = QtGui.QPushButton(self.groupBox_abs)
        self.pushButton_abs1.setGeometry(QtCore.QRect(13, 26, 140, 23))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_abs1.setFont(font)
        self.pushButton_abs1.setObjectName("pushButton_abs1")
        self.pushButton_abs2 = QtGui.QPushButton(self.groupBox_abs)
        self.pushButton_abs2.setGeometry(QtCore.QRect(182, 26, 140, 23))
        self.pushButton_abs2.setObjectName("pushButton_abs2")
        self.pushButton_abs3 = QtGui.QPushButton(self.groupBox_abs)
        self.pushButton_abs3.setGeometry(QtCore.QRect(63, 305, 222, 28))#59
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_abs3.setFont(font)
        self.pushButton_abs3.setObjectName("pushButton_abs3")        
        self.pushButton_abs4 = QtGui.QPushButton(self.groupBox_abs)#reset
        self.pushButton_abs4.setGeometry(QtCore.QRect(13, 506, 76, 28))#245
        self.pushButton_abs4.setObjectName("pushButton_abs4")  
        self.label_abs1 = QtGui.QLabel(self.groupBox_abs)
        self.label_abs1.setGeometry(QtCore.QRect(40, 277, 400, 31))
        self.label_abs1.setText("Highligh(select) items you want to show")
        self.label_abs1.setObjectName("label_abs1")                 
        self.tableWidget_abs = QtGui.QTableWidget(self.groupBox_abs)
        self.tableWidget_abs.setGeometry(QtCore.QRect(14, 56, 317, 222))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.tableWidget_abs.setFont(font)
        self.tableWidget_abs.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tableWidget_abs.setShowGrid(True)
        self.tableWidget_abs.setObjectName("tableWidget_abs")
        self.tableWidget_abs.setColumnCount(2)
        self.tableWidget_abs.setRowCount(10)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(0, item)
        self.tableWidget_abs.verticalHeaderItem(0).setText("blank")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(1, item)
        self.tableWidget_abs.verticalHeaderItem(1).setText("2")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(2, item)
        self.tableWidget_abs.verticalHeaderItem(2).setText("3")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(3, item)
        self.tableWidget_abs.verticalHeaderItem(3).setText("4")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(4, item)
        self.tableWidget_abs.verticalHeaderItem(4).setText("5")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(5, item)
        self.tableWidget_abs.verticalHeaderItem(5).setText("6")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(6, item)
        self.tableWidget_abs.verticalHeaderItem(6).setText("7")       
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(7, item)
        self.tableWidget_abs.verticalHeaderItem(7).setText("8") 
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(8, item)
        self.tableWidget_abs.verticalHeaderItem(8).setText("9")         
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setVerticalHeaderItem(9, item)
        self.tableWidget_abs.verticalHeaderItem(9).setText("10")         
        item = QtGui.QTableWidgetItem()        
        self.tableWidget_abs.setHorizontalHeaderItem(0, item)        
        self.tableWidget_abs.horizontalHeaderItem(0).setText("InputFile")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_abs.setHorizontalHeaderItem(1, item)
        self.tableWidget_abs.horizontalHeaderItem(1).setText("Name")
        self.tableWidget_abs.horizontalHeader().setDefaultSectionSize(124)
        self.tableWidget_abs.verticalHeader().setDefaultSectionSize(30)        
        self.label_abs2 = QtGui.QLabel(self.groupBox_abs)
        self.label_abs2.setGeometry(QtCore.QRect(16, 406, 400, 31))
        self.label_abs2.setText("~~Show Transmittance spectra~~")
        self.label_abs2.setObjectName("label_abs2")          
        self.label_abs3 = QtGui.QLabel(self.groupBox_abs)
        self.label_abs3.setGeometry(QtCore.QRect(16, 340, 400, 31))
        self.label_abs3.setText("Save Absorbance Value for selected item")
        self.label_abs3.setObjectName("label_abs3") 
        self.comboBox_abs = QtGui.QComboBox(self.groupBox_abs)
        self.comboBox_abs.setGeometry(QtCore.QRect(16, 370, 310, 24))
        self.comboBox_abs.setObjectName("comboBox_abs")
        self.comboBox_abs.addItem("")            
        self.comboBox_abs2 = QtGui.QComboBox(self.groupBox_abs)
        self.comboBox_abs2.setGeometry(QtCore.QRect(16, 436, 310, 24))
        self.comboBox_abs2.setObjectName("comboBox_abs2")
        self.comboBox_abs2.addItem("")  
        ################################################################        
        self.groupBox_s = QtGui.QGroupBox(self.tab_2)
        self.groupBox_s.setGeometry(QtCore.QRect(392, 7, 550, 545))
        self.groupBox_s.setObjectName("groupBox_s")
        self.pushButton_s4 = QtGui.QPushButton(self.groupBox_s)
        self.pushButton_s4.setGeometry(QtCore.QRect(188, 26, 140, 23))
        self.pushButton_s4.setObjectName("pushButton_s4")
        self.tableWidget_s = QtGui.QTableWidget(self.groupBox_s)
        self.tableWidget_s.setGeometry(QtCore.QRect(16, 56, 517, 222))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.tableWidget_s.setFont(font)
        self.tableWidget_s.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tableWidget_s.setShowGrid(True)
        self.tableWidget_s.setObjectName("tableWidget_s")
        self.tableWidget_s.setColumnCount(5)
        self.tableWidget_s.setRowCount(10)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(0, item)
        self.tableWidget_s.verticalHeaderItem(0).setText("blank")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(1, item)
        self.tableWidget_s.verticalHeaderItem(1).setText("2")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(2, item)
        self.tableWidget_s.verticalHeaderItem(2).setText("3")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(3, item)
        self.tableWidget_s.verticalHeaderItem(3).setText("4")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(4, item)
        self.tableWidget_s.verticalHeaderItem(4).setText("5")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(5, item)
        self.tableWidget_s.verticalHeaderItem(5).setText("6")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(6, item)
        self.tableWidget_s.verticalHeaderItem(6).setText("7")       
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(7, item)
        self.tableWidget_s.verticalHeaderItem(7).setText("8") 
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(8, item)
        self.tableWidget_s.verticalHeaderItem(8).setText("9")         
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setVerticalHeaderItem(9, item)
        self.tableWidget_s.verticalHeaderItem(9).setText("10")         
        item = QtGui.QTableWidgetItem()        
        self.tableWidget_s.setHorizontalHeaderItem(0, item)        
        self.tableWidget_s.horizontalHeaderItem(0).setText("InputFile")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setHorizontalHeaderItem(1, item)
        self.tableWidget_s.horizontalHeaderItem(1).setText("Name")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setHorizontalHeaderItem(2, item)
        self.tableWidget_s.horizontalHeaderItem(2).setText("Std.Conc.(M)")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setHorizontalHeaderItem(3, item)
        self.tableWidget_s.horizontalHeaderItem(3).setText("Max Abs.")
        item = QtGui.QTableWidgetItem()
        self.tableWidget_s.setHorizontalHeaderItem(4, item)
        self.tableWidget_s.horizontalHeaderItem(4).setText("Wavelength(nm)")        
        self.tableWidget_s.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_s.verticalHeader().setDefaultSectionSize(30)
        self.label_s1 = QtGui.QLabel(self.groupBox_s)
        self.label_s1.setGeometry(QtCore.QRect(17, 318, 250, 23))
        self.label_s1.setObjectName("label_s1")
        self.lineEdit_s1 = QtGui.QLineEdit(self.groupBox_s)
        self.lineEdit_s1.setGeometry(QtCore.QRect(271, 320, 76, 20))
        self.lineEdit_s1.setObjectName("lineEdit_s1")
        self.comboBox_s = QtGui.QComboBox(self.groupBox_s)
        self.comboBox_s.setGeometry(QtCore.QRect(15, 289, 231, 23))
        self.comboBox_s.setObjectName("comboBox_s")
        self.comboBox_s.addItem("")
        self.pushButton_s5 = QtGui.QPushButton(self.groupBox_s)
        self.pushButton_s5.setGeometry(QtCore.QRect(15, 342, 105, 30))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_s5.setFont(font)
        self.pushButton_s5.setObjectName("pushButton_s5")
        self.pushButton_s6 = QtGui.QPushButton(self.groupBox_s)#add_blank
        self.pushButton_s6.setGeometry(QtCore.QRect(15, 24, 159, 26))
        font = QtGui.QFont() 
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_s6.setFont(font)
        self.pushButton_s6.setObjectName("pushButton_s6")
        self.pushButton_s7 = QtGui.QPushButton(self.groupBox_s)#reset
        self.pushButton_s7.setGeometry(QtCore.QRect(463, 471, 76, 25))
        self.pushButton_s7.setObjectName("pushButton_s7")
        self.pushButton_s8 = QtGui.QPushButton(self.groupBox_s)
        self.pushButton_s8.setGeometry(QtCore.QRect(129, 342, 173, 30))
        self.pushButton_8.setObjectName("pushButton_s8")
        self.label_s2 = QtGui.QLabel(self.groupBox_s) #lebal result
        self.label_s2.setGeometry(QtCore.QRect(19, 373, 52, 27))
        self.label_s2.setObjectName("label_s2")
        self.pushButton_s9 = QtGui.QPushButton(self.groupBox_s) #load analyte
        self.pushButton_s9.setGeometry(QtCore.QRect(15, 426, 346, 30))
        font = QtGui.QFont() 
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_s9.setFont(font)
        self.pushButton_s9.setObjectName("pushButton_s9")
        self.label_s3 = QtGui.QLabel(self.groupBox_s)
        self.label_s3.setGeometry(QtCore.QRect(20, 483, 108, 30))
        self.label_s3.setObjectName("label_s3")
        self.pushButton_s10 = QtGui.QPushButton(self.groupBox_s)
        self.pushButton_s10.setGeometry(QtCore.QRect(307, 342, 173, 30))
        self.pushButton_s10.setObjectName("pushButton_s10")
        self.label_s4 = QtGui.QLabel(self.groupBox_s)#input 'result'
        self.label_s4.setGeometry(QtCore.QRect(74, 371, 445, 31))
        self.label_s4.setText("")
        self.label_s4.setObjectName("label_s4")
        self.label_s5 = QtGui.QLabel(self.groupBox_s)
        self.label_s5.setGeometry(QtCore.QRect(20, 456, 148, 30))
        self.label_s5.setObjectName("label_s5")
        self.label_s6 = QtGui.QLabel(self.groupBox_s)#input 'at wavelength' 
        self.label_s6.setGeometry(QtCore.QRect(162, 456, 108, 30))
        self.label_s6.setText("")
        self.label_s6.setObjectName("label_s6")
        self.label_s7 = QtGui.QLabel(self.groupBox_s)
        self.label_s7.setGeometry(QtCore.QRect(357, 314, 178, 30))
        self.label_s7.setObjectName("label_s7")
        self.label_s8 = QtGui.QLabel(self.groupBox_s)#input 'absorbance'
        self.label_s8.setGeometry(QtCore.QRect(123, 483, 108, 30))
        self.label_s8.setText("")
        self.label_s8.setObjectName("label_s8")
        self.label_s9 = QtGui.QLabel(self.groupBox_s)
        self.label_s9.setGeometry(QtCore.QRect(18, 511, 216, 30))
        self.label_s9.setObjectName("label_s9")
        self.label_s10 = QtGui.QLabel(self.groupBox_s)#input conc.
        self.label_s10.setGeometry(QtCore.QRect(214, 511, 108, 30))
        self.label_s10.setText("")
        self.label_s10.setObjectName("label_s10")
        self.pushButton_s11 = QtGui.QPushButton(self.groupBox_s)
        self.pushButton_s11.setGeometry(QtCore.QRect(367, 503, 173, 33))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_s11.setFont(font)
        self.pushButton_s11.setObjectName("pushButton_s11")
        self.label_s11 = QtGui.QLabel(self.groupBox_s)
        self.label_s11.setGeometry(QtCore.QRect(18, 398, 295, 24))
        self.label_s11.setObjectName("label_s11")
        self.lineEdit_s2 = QtGui.QLineEdit(self.groupBox_s)#input unknown name
        self.lineEdit_s2.setGeometry(QtCore.QRect(162, 400, 200, 23))
        self.lineEdit_s2.setObjectName("lineEdit_s2")                 
        self.tabWidget.addTab(self.tab_2, "Calculate absorbance and concentration")
###################################################################
        #initinalize for tableWidget_abs
        self.tableWidget_abs.clearContents()     
        for i in range(10):#each row
            item1 = QtGui.QTableWidgetItem()                              
            self.tableWidget_abs.setItem(i, 0,item1)#column1 
            item2 = QtGui.QTableWidgetItem()
            self.tableWidget_abs.setItem(i, 1,item2)#column2
        #initinalize for tableWidget_s    
        self.tableWidget_s.clearContents()     
        for i in range(10):
            items1 = QtGui.QTableWidgetItem()                              
            self.tableWidget_s.setItem(i, 0,items1) 
            items2 = QtGui.QTableWidgetItem()
            self.tableWidget_s.setItem(i, 1,items2) 
            items3 = QtGui.QTableWidgetItem()                              
            self.tableWidget_s.setItem(i, 2,items3) 
            items4 = QtGui.QTableWidgetItem()
            self.tableWidget_s.setItem(i, 3,items4) 
            items5 = QtGui.QTableWidgetItem()                              
            self.tableWidget_s.setItem(i, 4,items5) 
###################################################################
        self.pushButton_abs1.clicked.connect(self.add_blank)#l
        self.pushButton_abs2.clicked.connect(self.add_analyte)#l
        self.tableWidget_abs.cellChanged.connect(self.handleCellChanged)        
        self.comboBox_abs2.activated[str].connect(self.show_Transmittance)
        self.comboBox_abs.activated[str].connect(self.save_spectra_value)         
        self.pushButton_abs3.clicked.connect(self.plot_abs)#plot
        self.pushButton_abs4.clicked.connect(self.reset)#reset        
        self.pushButton_s4.clicked.connect(self.std_add_std)       
        self.pushButton_s6.clicked.connect(self.std_add_blank)       
        self.tableWidget_s.cellChanged.connect(self.std_handleCellChanged)        
        self.comboBox_s.activated[str].connect(self.std_show_abs) 
        self.pushButton_s5.clicked.connect(self.std_calibrate)       
        self.pushButton_s7.clicked.connect(self.std_reset)#
        self.pushButton_s8.clicked.connect(self.std_save_calibrate)              
        self.pushButton_s9.clicked.connect(self.std_load_analyte)#Load Analyte solution and Show Abs. spectra"       
        self.pushButton_s10.clicked.connect(self.std_load_calibrate)       
        self.pushButton_s11.clicked.connect(self.std_save_report)       
        tab2_readme1(self) #textEdit_t2re1
        tab2_readme2(self) #textEdit_t2re2        
##################################################################################        
#        self.tab_3 = QtGui.QWidget()
#        self.tab_3.setObjectName("tab_3")
#        self.label_t3_1 = QtGui.QLabel(self.tab_3)#input conc.
#        self.label_t3_1.setGeometry(QtCore.QRect(38, 24, 300, 30))
#        self.label_t3_1.setText("Coming soon!")
#        self.label_t3_1.setObjectName("label_t3_1")        
#        self.label_t3_1.setStyleSheet('color: red')#'color: rgb(255, 0, 0)' or 'blue'
#        self.tabWidget.addTab(self.tab_3, "Stellar spectra process")
##################################################################################                              
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")        
        self.groupBox_t4_about = QtGui.QGroupBox(self.tab_4)
        self.groupBox_t4_about.setGeometry(QtCore.QRect(225, 24, 510, 305))
        self.groupBox_t4_about.setObjectName("groupBox_t4_about")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_t4re1 = QtGui.QTextEdit(self.groupBox_t4_about)
        self.textEdit_t4re1.setGeometry(QtCore.QRect(13, 22, 485, 269))
        self.textEdit_t4re1.setFont(font)
        self.textEdit_t4re1.setObjectName("textEdit_t4re1")
        self.textEdit_t4re1.setReadOnly(True)
        self.label_qr = QtGui.QLabel(self.tab_4)
        self.label_qr.setGeometry(QtCore.QRect(750, 500, 148, 148))
        pixmap = QtGui.QPixmap('etc//lcycblog.png')#148*148
        self.label_qr.setPixmap(pixmap)
        self.label_qr.show()
        self.label_qr.setObjectName("label_qr")        
        self.tabWidget.addTab(self.tab_4, "About")
        tab4_about1(self) #textEdit_t4re1
##################################################################################            
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setItalic(False)        
        self.tab_1.setFont(font)
        self.tab_2.setFont(font)
#        self.tab_3.setFont(font)
        self.tab_4.setFont(font)
##################################################################################            
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.stdLight.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
##################################################################################        
# Tab_2 start ##########################################################################        
##################################################################################        
    def add_blank(self):
        global abs_blank #nm=[:,0] int=[:,1]
        global abs_input_name  
        blank_path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        data = np.genfromtxt(blank_path,dtype=str,delimiter=',')          
        abs_blank = np.array(data[0:data.shape[0]],dtype=float) 
        filename1 = blank_path.split('/')[len(blank_path.split('/'))-1]
        filename = '%s'%(filename1)        
        item = QtGui.QTableWidgetItem(filename)        
        self.tableWidget_abs.setItem(0, 0,item)
        abs_input_name = np.append(abs_input_name,'1')#init abs_input_name            
    def add_analyte(self):
        global abs_analyte
        global abs_analyte_number
        global abs_input_name        
        analyte_path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        data = np.genfromtxt(analyte_path,dtype=str,delimiter=',')          
        analyte = np.array(data[0:data.shape[0],1],dtype=float)
        if abs_analyte_number == 0:            
           abs_analyte = np.array([analyte],dtype=float)
        else:
           abs_analyte = np.vstack((abs_analyte,analyte))                 
        abs_analyte_number +=1
        filename1 = analyte_path.split('/')[len(analyte_path.split('/'))-1]
        filename = '%s'%(filename1)
        item = QtGui.QTableWidgetItem(filename)        
        self.tableWidget_abs.setItem(abs_analyte_number, 0,item)         
        abs_input_name = np.append(abs_input_name,str(abs_analyte_number+1))#init abs_input_name
        self.comboBox_abs.addItem("")
        self.comboBox_abs.setItemText(abs_analyte_number, abs_input_name[abs_analyte_number])
        self.comboBox_abs2.addItem("")#for show specra
        self.comboBox_abs2.setItemText(abs_analyte_number, abs_input_name[abs_analyte_number])        
    def handleCellChanged(self,row,column):
        global abs_input_name    #[1234]
        if column == 0:
           pass
        elif column == 1:
          item = self.tableWidget_abs.item(row, column) #get input_x memory site        
          if row > 0:          
             self.comboBox_abs.setItemText(row, item.text())
             self.comboBox_abs2.setItemText(row, item.text())
          abs_input_name = np.append(abs_input_name,item.text())#translate to unicode                             
          abs_input_name[row] = abs_input_name[abs_input_name.size-1]#switch                           
          abs_input_name = np.delete(abs_input_name, abs_input_name.size-1)#delete   
    def show_Transmittance(self,name): #comboBox_abs2
        global abs_input_name
        global abs_blank #nm=[:,0] int=[:,1]        
        global abs_analyte
        global abs_plot_number
        if name == "Select and Show":
           print "Show Transmittance spectra for the selected item."
        else:
           x_nm = abs_blank[:,0]          
           aidx = np.arange(abs_input_name.size)#0 is blamk 
           idx = aidx[np.where(abs_input_name == name)][0] #decide which item be selected (start from 1 eq analyte 0) 

           blank = abs_blank[:,1]
           rule = np.where(blank>(blank.min()+6.4)/2.)#min to 0.012
           x_nm = x_nm[rule]                                 
           analyte = abs_analyte[idx-1]  
           analyte = analyte[rule]       
           blank = blank[rule]#must be last 
           transmittance = analyte/blank 
           abs_plot_number +=1
           plt.figure(808+abs_plot_number)
           plt.gcf().canvas.set_window_title('%s_Transmittance_spectra'%(abs_input_name[idx]))             
           plt.xlim(x_nm.min(),x_nm.max())
           plt.ylim(0,1)           
           plt.title('%s'%(abs_input_name[idx]))
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('Transmittance')
           plt.minorticks_on()
           plt.grid(True)
           plt.tight_layout()    
           plt.plot(x_nm,transmittance,'k-',label=abs_input_name[idx])
           plt.legend(loc='best')
           plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
           plt.show()                        
    def save_spectra_value(self,name):#comboBox_abs
        global abs_input_name
        global abs_blank #nm=[:,0] int=[:,1]        
        global abs_analyte
        if name == "Select and Save":
           print "The selected item will be autosave in 'Save' folder."
        else:
           nm = abs_blank[:,0]
           aidx = np.arange(abs_input_name.size)
           idx = aidx[np.where(abs_input_name == name)][0] #1~n, already get[0] to get value
           blank = abs_blank[:,1]
           rule = np.where(blank>(blank.min()+6.4)/2.)
           nm = nm[rule]
           analyte = abs_analyte[idx-1]  
           analyte = analyte[rule]       
           blank = blank[rule]#must be last 
           absorbance = np.log10(blank/analyte)
           save_data = np.concatenate((nm.reshape(nm.size,1), absorbance.reshape(nm.size,1)), axis=1)
           savepath = 'Save//Absorbance_value' #r'C:\Program Files\arbitrary'
           if not os.path.exists(savepath):
              os.makedirs(savepath)
           filename = 'Save//Absorbance_value//%s_absorbance_value.csv'%(abs_input_name[idx])
           np.savetxt(filename,save_data,delimiter=',',fmt='%.3f')
           print "%s_absorbance_value.csv has been saved to folder: Save\\Absorbance_value"%(abs_input_name[idx])   
    def plot_abs(self): #comboBox_abs2
        global abs_input_name
        global abs_blank #nm=[:,0] int=[:,1]        
        global abs_analyte
        global abs_analyte_number #number of analyte
        global abs_plot_number        
        select_idx = np.array([],dtype=int)
        for item in self.tableWidget_abs.selectedIndexes():
            select_idx = np.append(select_idx,item.row())
        idx = select_idx[np.argsort(select_idx)]
        if idx[0] == 0:
           print "Do not select No.1 item(Blank)"
        elif idx.max() > abs_analyte_number:
           print "Your selection has been out of range."
        else:
           x_nm = abs_blank[:,0]           

           blank = abs_blank[:,1]
           rule = np.where(blank == blank)
           x_nm = x_nm[rule]
           analyte = np.zeros((abs_analyte_number,x_nm.size))#rebuild selected            
           for n in range(abs_analyte_number):           
              analyte[n] = abs_analyte[n,rule]                     
           blank = blank[rule]#must be last                     
           absorbance = np.log10((blank)/(analyte))#caculate all       
           abs_plot_number +=1
           colors = ['b-','r-','k-','g-','c-','m-','y-','b--','r--'] 
           plt.figure(3478+abs_plot_number)
           plt.gcf().canvas.set_window_title('Absorbance_spectra')             
           plt.xlim(x_nm.min(),x_nm.max())
           plt.ylim(0,2)
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('Absorbance')
           plt.minorticks_on()
           plt.grid(True)
           plt.tight_layout()    
           plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range                             
           for i in idx: #if idx =1,3 abs = 0,2
              plt.plot(x_nm,absorbance[i-1],colors[i-1],label=abs_input_name[i])
           plt.legend(loc='best')          
           plt.show()        
    def reset(self):#abs        
        global abs_blank 
        abs_blank = np.array([],dtype=float)
        global abs_analyte
        abs_analyte = np.array([],dtype=float)
        global abs_input_name
        abs_input_name = np.array([],dtype=str)
        global abs_plot_number
        abs_plot_number = 1
        self.tableWidget_abs.clearContents()     
        global abs_analyte_number
        for idx in range(abs_analyte_number): #This will update the current index if the index is removed.
           self.comboBox_abs.removeItem(1)
           self.comboBox_abs2.removeItem(1)        
        abs_analyte_number = 0
    ##############################################################################
    ##############################################################################  
    def std_add_blank(self):
        global std_blank #nm=[:,0] int=[:,1]
        global std_input_name
        global std_input_conc
        blank_path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        data = np.genfromtxt(blank_path,dtype=str,delimiter=',')          
        std_blank = np.array(data[0:data.shape[0]],dtype=float) 
        filename1 = blank_path.split('/')[len(blank_path.split('/'))-1]
        filename = '%s'%(filename1)  
        std_input_name = np.append(std_input_name,'1')
        std_input_conc = np.append(std_input_conc,'1')
        item = QtGui.QTableWidgetItem(filename)        
        self.tableWidget_s.setItem(0, 0,item)                
        item2 = QtGui.QTableWidgetItem('blank')        
        self.tableWidget_s.setItem(0, 2,item2)
        item3 = QtGui.QTableWidgetItem('blank')        
        self.tableWidget_s.setItem(0, 3,item3)   
        item4 = QtGui.QTableWidgetItem('blank')        
        self.tableWidget_s.setItem(0, 4,item4)             
    def std_add_std(self):
        global std_blank
        global std_std
        global std_std_number
        global std_input_name
        global std_input_conc
        global std_max_wavelength
        global std_max_abs
        std_std_path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        data = np.genfromtxt(std_std_path,dtype=str,delimiter=',')          
        std = np.array(data[0:data.shape[0],1],dtype=float)
        if std_std_number == 0:            
           std_std = np.array([std],dtype=float)
        else:
           std_std = np.vstack((std_std,std))                 
        std_std_number +=1
        filename1 = std_std_path.split('/')[len(std_std_path.split('/'))-1]
        filename = '%s'%(filename1)
        item = QtGui.QTableWidgetItem(filename)        
        self.tableWidget_s.setItem(std_std_number, 0,item)         
        std_input_name = np.append(std_input_name,str(std_std_number+1))
        std_input_conc = np.append(std_input_conc,str(std_std_number+1))                
        self.comboBox_s.addItem("")
        self.comboBox_s.setItemText(std_std_number, std_input_name[std_std_number])#first item is 2
        #now calculate max.abs. and wave
        x_nm = std_blank[:,0]           
        blank = std_blank[:,1]
        rule = np.where(blank>(blank.min()+6.4)/2.)#max to 1.9
        x_nm = x_nm[rule]
        std = std[rule]                      
        blank = blank[rule]#must be last                     
        absorbance = np.log10((blank)/(std))#caculate all           
        max_abs = max(absorbance)
        max_wavelength = x_nm[np.where(absorbance == max_abs)]
        item3 = QtGui.QTableWidgetItem(str(max_abs))        
        self.tableWidget_s.setItem(std_std_number, 3,item3)   
        item4 = QtGui.QTableWidgetItem(str(max_wavelength[0]))        
        self.tableWidget_s.setItem(std_std_number, 4,item4)        
        std_max_wavelength = np.append(std_max_wavelength,max_wavelength)
        std_avg_max_wavelength = np.average(std_max_wavelength)        
        self.lineEdit_s1.setText(str(std_avg_max_wavelength))
        std_max_abs = np.append(std_max_abs,max_abs)        
    def std_handleCellChanged(self,row,column):
        global std_std_number
        global std_input_name
        global std_input_conc        
        if column == 0 or column == 3 or column == 4:
           pass
        elif column == 1:
          item = self.tableWidget_s.item(row, column) #get input_x memory site        
          if row > 0:  #no blank        
             self.comboBox_s.setItemText(row, item.text())
          std_input_name = np.append(std_input_name,item.text())#translate to unicode                             
          std_input_name[row] = std_input_name[std_input_name.size-1]# last switch to right place                           
          std_input_name = np.delete(std_input_name, std_input_name.size-1)#delete last  
        elif column == 2:
          item = self.tableWidget_s.item(row, column) #get input_x memory site        
          if row > 0:  #skip blank        
             std_input_conc = np.append(std_input_conc,item.text())#translate to unicode                             
             std_input_conc[row] = std_input_conc[std_input_conc.size-1]# last switch to right place                           
             std_input_conc = np.delete(std_input_conc, std_input_conc.size-1)#delete last  
    def std_show_abs(self,name): #comboBox_abs2
        global std_blank
        global std_std
        global std_std_number
        global std_input_name
        global std_plot_number
        if name == "Show Abs. spectra(all in one)":
           if std_std_number < 1:
              print "Please add std.solution first."
           else:   
              x_nm = std_blank[:,0]           
              blank = std_blank[:,1]
              rule = np.where(blank>(blank.min()+6.4)/2.)#max to 1.9
              x_nm = x_nm[rule]
              std = np.zeros((std_std_number,x_nm.size))           
              for n in range(std_std_number):           
                 std[n] = std_std[n,rule]          
              blank = blank[rule]#must be last                     
              absorbance = np.log10((blank)/(std)) #caculate all            
              std_plot_number +=1
              colors = ['b-','r-','k-','g-','c-','m-','y-','b--','r--'] 
              plt.figure(5678+std_plot_number)
              plt.gcf().canvas.set_window_title('Absorbance_spectra_all_Std.')             
              plt.xlim(x_nm.min(),x_nm.max())
              plt.ylim(0,2)
              plt.xlabel('Wavelength (nm)')
              plt.ylabel('Absorbance')
              plt.minorticks_on()
              plt.grid(True)
              plt.tight_layout()    
              plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range                             
              for i in range(std_std_number): 
                 plt.plot(x_nm,absorbance[i],colors[i],label=std_input_name[i+1])
              plt.legend(loc='best')          
              plt.show()                   
        else:        
           aidx = np.arange(std_input_name.size)#0 is blank 
           idx = aidx[np.where(std_input_name == name)][0] #decide which item be selected (start from 1 eq analyte 0) 
           x_nm = std_blank[:,0]           
           blank = std_blank[:,1]
           rule = np.where(blank>(blank.min()+6.4)/2.)#max to 1.9
           x_nm = x_nm[rule]
           std = std_std[idx-1] 
           std = std[rule]          
           blank = blank[rule]#must be last                     
           absorbance = np.log10((blank)/(std))                      
           std_plot_number +=1
           plt.figure(8210+std_plot_number)
           plt.gcf().canvas.set_window_title('%s_Absorbance_spectra'%(std_input_name[idx]))             
           plt.xlim(x_nm.min(),x_nm.max())
           plt.ylim(0,2)           
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('Absorbance')
           plt.minorticks_on()
#           plt.grid(True)
           plt.tight_layout()    
           plt.plot(x_nm,absorbance,'b-',label=std_input_name[idx])
           plt.legend(loc='best')
           plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
           plt.show()   
    def std_calibrate(self):
        global std_blank
        global std_std
        global std_input_conc #x axis
        global std_max_abs #y axis
        global std_select_wavelength
        global std_linregress #slope,intercept,rvalue,pvalue,std_err 
        global std_plot_number      
        x_nm = std_blank[:,0]           
        blank = std_blank[:,1]
        rule = np.where(blank>(blank.min()+6.4)/2.)#max to 1.9
        x_nm = x_nm[rule]
        std = np.zeros((std_std_number,x_nm.size))           
        for n in range(std_std_number):           
            std[n] = std_std[n,rule]          
        blank = blank[rule]#must be last                     
        absorbance = np.log10((blank)/(std)) #caculate all 
        std_select_wavelength= float(self.lineEdit_s1.text()) 
        std_input_conc = np.array(std_input_conc,dtype=float)#x axis      
        #find w_l point that closet the std_select_wavelength
        delta_nm = np.abs(x_nm-std_select_wavelength)
        std_select_wavelength = x_nm[np.where(delta_nm == delta_nm.min())][0]          
        rule2 = np.where(x_nm == std_select_wavelength)
        std_max_abs = np.zeros(std_std_number)           
        for n in range(std_std_number):           
           std_max_abs[n] = absorbance[n,rule2] #y axis
        std_conc = std_input_conc[1:std_input_conc.size]
        self.lineEdit_s1.setText(str(std_select_wavelength))               
        from scipy.stats import linregress
        std_linregress= np.array(linregress(std_conc, std_max_abs),dtype=float)
        r2 = u'\u00B2' #2 up scripts
        self.label_s4.setText('Y(abs.)=%.5f*X(conc.)+%.5f   R%s=%.5f'%(std_linregress[0],std_linregress[1],r2,std_linregress[2]**2))
        std_plot_number +=1
        plt.figure(9000+std_plot_number)
        plt.gcf().canvas.set_window_title('Standard_Calibration_Curve(%s nm)'%std_select_wavelength)             
        plt.xlim(0,std_conc.max()+std_conc.max()/10.)
        plt.xlabel('Conc.')
        plt.ylabel('Absorbance')
        plt.minorticks_on()
        plt.tight_layout()        
        plt.plot(std_conc,std_max_abs,'r^')
        x = std_conc
        y = std_linregress[0]*std_conc+std_linregress[1]
        plt.plot(x,y,'k-',label=r'y=%.5fx+%.5f  R$^2$=%.5f'%(std_linregress[0],std_linregress[1],std_linregress[2]**2))
        plt.legend(loc='best')
        plt.show()    
    def std_save_calibrate(self):                
        global std_input_conc #idx0 = 1 is blank
        global std_input_name #idx0 is blank      
        global std_select_wavelength        
        global std_max_abs #y axis
        global std_linregress #slope,intercept,rvalue,pvalue,std_err 
        from time import localtime, strftime 
        time_now = strftime("%Y-%m-%d_%H-%M-%S", localtime())
        savepath = 'Save//Standard_calibration' #r'C:\Program Files\arbitrary'
        if not os.path.exists(savepath):
           os.makedirs(savepath)
        filename = 'Save//Standard_calibration//Standard_Calibration_data_(%s).csv'%(time_now)
        file = open(filename , "w")
        file.write('# Standard Calibration data  %s \n'%(time_now))
        file.write('# Selected Wavelength(nm)  \n')
        file.write('  %s,None,None,None,None\n'%(str(std_select_wavelength)))
        file.write('# Name   Conc.(M)   Abs.  \n')#str float float
        for i in range(std_input_conc.size):
           if i == 0: #blank
             line = '  %s,%s,%s,None,None\n'%(std_input_name[i],'blank','blank')
           else:                
             line = '  %s,%f,%.5f,None,None\n'%(std_input_name[i],std_input_conc[i],std_max_abs[i-1])
           file.write(line)
        file.write('# Calibration result\n')
        file.write('# slope intercept r_value p_value std_err\n')
        file.write('  %.5f,%.5f,%.5f,%.5f,%.5f\n'%(std_linregress[0],std_linregress[1],std_linregress[2],std_linregress[3],std_linregress[4]))
        file.close()
        print "Standard_Calibration_data_(%s).csv has been saved to folder: Save\\Standard_calibration"%(time_now)  
    def std_load_calibrate(self):                
        global std_input_conc #idx0 = 1 is blank
        global std_input_name #idx0 is blank      
        global std_select_wavelength        
        global std_max_abs #y axis
        global std_linregress #slope,intercept,rvalue,pvalue,std_err    
        std_cali_path, _ = QtGui.QFileDialog.getOpenFileName()
        data = np.genfromtxt(std_cali_path,dtype=str,delimiter=',')
        data_size = int(data.shape[0])
        std_select_wavelength = float(data[0,0])        
        std_input_name = data[1:data_size-1,0]#need str  
        std_input_conc = data[1:data_size-1,1]
        std_input_conc[0]='1'
        std_input_conc = np.array(std_input_conc,dtype=float)#need float
        std_max_abs = np.array(data[2:data_size-1,2],dtype=float)#need float
        std_linregress = np.array(data[data_size-1,:],dtype=float)#last
        r2 = u'\u00B2'
        self.label_s4.setText('Y(abs.)=%.5f*X(conc.)+%.5f   R%s=%.5f'%(std_linregress[0],std_linregress[1],r2,std_linregress[2]**2))
        self.lineEdit_s1.setText(str(std_select_wavelength))  
        for i in range(std_input_name.size):
            if i == 0:#blank             
               name = QtGui.QTableWidgetItem(std_input_name[i])        
               self.tableWidget_s.setItem(i, 1,name)
               conc = QtGui.QTableWidgetItem('blank')        
               self.tableWidget_s.setItem(i, 2,conc)
               absorb = QtGui.QTableWidgetItem('blank')        
               self.tableWidget_s.setItem(i, 3,absorb)
            else:
               name = QtGui.QTableWidgetItem(std_input_name[i])        
               self.tableWidget_s.setItem(i, 1,name)
               conc = QtGui.QTableWidgetItem(str(std_input_conc[i]))        
               self.tableWidget_s.setItem(i, 2,conc)
               absorb = QtGui.QTableWidgetItem(str(std_max_abs[i-1]))        
               self.tableWidget_s.setItem(i, 3,absorb)               
        std_input_conc = np.array(std_input_conc,dtype=float)#need float
    def std_load_analyte(self):
        global std_blank
        global std_select_wavelength        
        global std_linregress #slope,intercept,rvalue,pvalue,std_err 
        global std_plot_number
        global std_analyte_result          
        std_analyte_path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        data = np.genfromtxt(std_analyte_path,dtype=str,delimiter=',')          
        std_analyte = np.array(data[:,1],dtype=float)
        analyte_name= self.lineEdit_s2.text()
        if std_blank.size == 0:
           print 'If you have loaded calibration data file and want to load'
           print 'analyte solution file, Please add blank solution file first.'
        elif len(analyte_name) == 0:
           print 'You need to enter the analyte name.'
        else:
           x_nm = std_blank[:,0]           
           blank = std_blank[:,1]
           rule = np.where(blank>(blank.min()+6.4)/2.)#max to 1.9
           x_nm = x_nm[rule]      
           std_analyte = std_analyte[rule]          
           blank = blank[rule]#must be last                     
           absorbance = np.log10(blank/std_analyte)                       
           std_analyte_abs = absorbance[np.where(x_nm == std_select_wavelength)]      
           std_analyte_result = np.append(std_analyte_result,std_analyte_abs)
           # abs = a*conc+b >> conc = (abs-b)/a
           unknown = (std_analyte_abs-std_linregress[1])/std_linregress[0]
           std_analyte_result = np.append(std_analyte_result,unknown)
           self.label_s6.setText(str(std_select_wavelength))#at wavelength
           self.label_s8.setText('%.6f'%(std_analyte_abs[0]))#abs. for unknown
           self.label_s10.setText('%.6f'%(unknown[0]))#unknown conc.

           std_plot_number +=1
           plt.figure(6822+std_plot_number)
           plt.gcf().canvas.set_window_title('Absorbance_spectra_for_analyte')             
           plt.xlim(x_nm.min(),x_nm.max())
           plt.ylim(0,2)
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('Absorbance')
           plt.minorticks_on()
           plt.grid(True)
           plt.tight_layout()    
           plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range                             
           plt.plot(x_nm,absorbance,'r-',label='%s'%(analyte_name))
           plt.legend(loc='best')          
           plt.show()          

    def std_save_report(self):
        #need save to txt file and png file
        global std_plot_number
        global std_input_conc #idx0 = 1 is blank
        global std_input_name #idx0 is blank      
        global std_select_wavelength        
        global std_max_abs #y axis
        global std_linregress #slope,intercept,rvalue,pvalue,std_err 
        global std_analyte_result
        analyte_name= self.lineEdit_s2.text()
        from time import localtime, strftime 
        time_now = strftime("%Y-%m-%d_%H-%M-%S", localtime())
        savepath = 'Save//Standard_calibration' #r'C:\Program Files\arbitrary'
        if not os.path.exists(savepath):
           os.makedirs(savepath)
        filename = 'Save//Standard_calibration//%s Concentration analysis Report_(%s).csv'%(analyte_name,time_now)
        file = open(filename , "w")
        file.write('%s Concentration analysis Report   Date: %s \n'%(analyte_name,time_now))
        file.write('----------------------------------------------------------------------------\n')
        file.write('1.Method: External-standard calibration with Linear-regression\n')
        file.write('2.Calibration data: \n')
        file.write('  Selected Wavelength(nm): %s  \n'%(str(std_select_wavelength)))
        name_size_max = 0 #we need put 9 space behind the name which has the max length 
        for i in range(std_input_conc.size):            
            name_size = len(std_input_name[i])
            if name_size > name_size_max:
               name_size_max = name_size            
        space ='                              '#total 30 space for insert
        file.write('  Std.Name%sConc.(M)%sAbs  \n'%(space[0:9+name_size_max-8],space[0:6]))#str float float
        for i in range(std_input_conc.size):
           if i == 0: #blank
             insert = 9+(name_size_max-len(std_input_name[i]))
             line = '  %s%s%s%s%s \n'%(std_input_name[i],space[0:insert],'blank',space[0:9],'0')
           else:                
             insert = 9+(name_size_max-len(std_input_name[i]))
             line = '  %s%s%.5f%s%.5f \n'%(std_input_name[i],space[0:insert],std_input_conc[i],space[0:7],std_max_abs[i-1])
           file.write(line)
        file.write('  Slope:%.5f, Intercept:%.5f, R value:%.5f,  Std err:%.5f \n'%(std_linregress[0],std_linregress[1],std_linregress[2],std_linregress[4]))
        file.write('3.Analysis result: \n')
        file.write('  Sample%sAbs%sConc.(M) \n'%(space[0:9+len(analyte_name)-6],space[0:13]))
        file.write('  %s%s%.5f%s%.5f\n'%(analyte_name,space[0:9],std_analyte_result[0],space[0:9],std_analyte_result[1]))
        file.write('----------------------------------------------------------------------------\n')
        file.close()
        # plot report             
        std_plot_number +=1
        plt.figure(2356+std_plot_number).set_size_inches(8.27,11.69) #a4 = 8.27 x 11.69
        plt.gcf().canvas.set_window_title('%s Concentration analysis Report'%(analyte_name))                     
        plt.subplot(211)
        plt.title('%s Concentration analysis Report'%(analyte_name))        
        plt.xlabel('Conc.(M)')
        plt.ylabel('Absorbance')
        plt.minorticks_on()
        plt.tight_layout()    
        std_conc = np.array(std_input_conc[1:std_input_conc.size],dtype=float)    
        plt.xlim(0,std_conc.max()+std_conc.max()/10.)
        plt.plot(std_conc,std_max_abs,'r^')
        x = std_conc
        y = std_linregress[0]*std_conc+std_linregress[1]
        plt.plot(x,y,'k-',label=r'Calibration curve: y=%.5fx+%.5f  R$^2$=%.5f'%(std_linregress[0],std_linregress[1],std_linregress[2]**2))
        plt.legend(loc='best')
        plt.subplot(212)
        plt.axis("off")                     
        plt.tight_layout()      
        plt.text(0, 1,'Date: %s'%(time_now), fontsize=13)
        plt.text(0, 0.95,'---------------------------------------------------------------------------------', fontsize=13)
        plt.text(0, 0.9,'1.Method: External-standard calibration with Linear-regression', fontsize=12)
        plt.text(0, 0.85,'2.Calibration data:', fontsize=12)
        plt.text(0, 0.8,'  Selected Wavelength(nm): %s  '%(str(std_select_wavelength)), fontsize=12)
        plt.text(0, 0.75,'  Std.Name%sConc.(M)%sAbs '%(space[0:11+name_size_max-8],space[0:11]), fontsize=12)        
        name_size_max = 0 #we need put 9 space behind the name which has the max length 
        for i in range(std_input_conc.size):            
            name_size = len(std_input_name[i])
            if name_size > name_size_max:
               name_size_max = name_size    
        for i in range(std_input_conc.size):
           n = i 
           if i == 0: #blank
             insert = 13+(name_size_max-len(std_input_name[i]))
             line = '  %s%s%s%s%s '%(std_input_name[i],space[0:insert],'blank',space[0:11],'0')
           else:                
             insert = 13+(name_size_max-len(std_input_name[i]))
             line = '  %s%s%.5f%s%.5f '%(std_input_name[i],space[0:insert],std_input_conc[i],space[0:10],std_max_abs[i-1])
           plt.text(0, 0.7-i/20.,line, fontsize=12)#i=4 plot in 0.55           
        plt.text(0, 0.65-n/20.,'  Slope:%.5f, Intercept:%.5f, R value:%.5f,  Std err:%.5f '%(std_linregress[0],std_linregress[1],std_linregress[2],std_linregress[4]), fontsize=12)
        plt.text(0, 0.6-n/20.,'3.Analysis result: ', fontsize=12)
        plt.text(0, 0.55-n/20.,'  Sample%sAbs%sConc.(M) '%(space[0:12+len(analyte_name)-6],space[0:16]), fontsize=12)
        plt.text(0, 0.5-n/20.,'  %s%s%.5f%s%.5f'%(analyte_name,space[0:10],std_analyte_result[0],space[0:9],std_analyte_result[1]), fontsize=12)
        plt.text(0, 0.45-n/20.,'---------------------------------------------------------------------------------', fontsize=13)
        plt.savefig('Save//Standard_calibration//%s Concentration analysis Report (%s).png'%(analyte_name,time_now),format='png')
        plt.show() 
        print "Report files(.csv &.png) has been saved to folder: Save\\Standard_calibration"                                          
    def std_reset(self):
        global std_blank 
        global std_std 
        global std_std_number 
        global std_input_name 
        global std_input_conc
        global std_plot_number 
        global std_max_wavelength #for auto select
        global std_select_wavelength #for manual select
        global std_max_abs #for abs. at select w_l
        global std_linregress #slope,intercept,rvalue,pvalue,std_err 
        global std_analyte_result #store 2 item: abs unknown                     
        std_blank = np.array([],dtype=float)
        std_std = np.array([],dtype=float)
        std_input_name = np.array([],dtype=str)
        std_input_conc = np.array([],dtype=str)
        std_plot_number = 1
        std_max_wavelength = np.array([],dtype=float)#for auto select
        std_select_wavelength = 0.0 #for manual select
        std_max_abs = np.array([],dtype=float)#for abs. at select w_l
        std_linregress = np.zeros(5)#slope,intercept,rvalue,pvalue,std_err 
        std_analyte_result = np.array([],dtype=float)#store 2 item: abs unknown       
        self.tableWidget_s.clearContents()     
        for idx in range(std_std_number): #This will update the current index if the index is removed.
           self.comboBox_s.removeItem(1)      
        std_std_number = 0
        self.lineEdit_s1.setText('')
        self.lineEdit_s2.setText('')     
        self.label_s4.setText('') #result
        self.label_s6.setText('') #at wavelength
        self.label_s8.setText('') #abs
        self.label_s10.setText('') #conc

##################################################################################        
# Tab_1 start ##########################################################################        
##################################################################################        
    def openFile(self):      
        global path
        path, _ = QtGui.QFileDialog.getOpenFileName()#,"Open","All files (*.*)"
        self.label_9.setText(path)
        img = Image.open(path)#.convert('L') # Y'=0.299R+0.587G+0.114B
        print 'The image mode is ', img.mode #I is wb, RGB is color
        xsize, ysize = img.size
        self.label_10.setText('%d x %d'%(xsize,ysize))
        img_show = mpimg.imread(path)
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):
                #z = self.im.get_array()[int(y), int(x)]
                return 'x=%d, y=%d'%(int(x)+1, int(y)+1)
        filename1 = path.split('/')[len(path.split('/'))-1]                                             
        fig1, ax = plt.subplots()
        plt.gcf().canvas.set_window_title(filename1)
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.axis("off")        
        plt.xlim(0,xsize)
        plt.ylim(ysize,0)
        if img.mode[0] == 'I' or img.mode[0] == 'L' :       
          im = ax.imshow(img_show,cmap='Greys_r')
        else:
          im = ax.imshow(img_show)
        ax.format_coord = Formatter(im)
        plt.show()
##################################################     
    def plot_region(self):
        global box
        box[0] = int(self.lineEdit_2.text())-1 #[idx from 0 : to nth element]
        box[1] = int(self.lineEdit_3.text())
        print 'Region = %d %d'%(box[0]+1,box[1])
########################################################################        
    def plotProfile(self):
        global path
        global box  
        img = Image.open(path)
        xsize, ysize = img.size
        pix_area = img.crop((0,int(box[0]),xsize,int(box[1])))#left up right down
        if img.mode[0] == 'I' or img.mode[0] == 'L' :
           pix_gray = np.asarray(pix_area.getdata()).reshape(box[1]-box[0], xsize)#dirctive get grey scale
           pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16
        else:   
           pix = np.asarray(pix_area).reshape(box[1]-box[0],xsize,3)# 1pix==idx0 get rgb
           print pix.shape, pix.size
#          luma(BT.709)=R*0.2126 + G*0.7152 + B*0.0722
#          luma(BT.601)=R*0.299 + G*0.587 + B*0.114
           pix_gray = pix[:,:,0]*0.299+pix[:,:,1]*0.587+pix[:,:,2]*0.114#601            
#           pix_gray2 = pix[:,:,0]*0.2126+pix[:,:,1]*0.7152+pix[:,:,2]*0.0722#709          
#           pix_gray3 = np.asarray(img.getdata().convert('L')).reshape(ysize, xsize)                 
        plot_x = np.asarray(range(xsize))+1 #set x-axis +1 if there is no index operation of plot_x   
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):
                return 'x=%d, y=%.2f'%(int(x)+1, y)     
        intensity_box = pix_gray.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row                                                                                           

        filename1 = path.split('/')[len(path.split('/'))-1]                                             
        fig2, ax2 = plt.subplots()
        plt.gcf().canvas.set_window_title("Profile(Y=%d to %d)"%(int(box[0])+1,int(box[1])))          
        plt.xlim(1,xsize)
        plt.xlabel('x (pixel)')
        plt.ylabel('intensity (counts)')
        plt.tight_layout()
        plt.minorticks_on()
        plt.grid(True)       
        im2 = ax2.plot(plot_x,intensity_box,'k-',label=filename1)
#        im4 = ax2.plot(plot_x,intensity_box3,'b-',label='PIL(BT.601)')
        plt.legend(loc='best')    
        ax2.format_coord = Formatter(im2)
        plt.show()      
########################################################################
    def load_stdlight(self,light):
        global stdlight        
        if light == "Select Std. Light source":
           self.tableWidget.clearContents()
           stdlight = 'none'
        if light == "Neon Lamp":
           global neon_data
           stdlight = 'neon'
           data = np.array(neon_data,dtype=str)
           self.tableWidget.clearContents()
           n=0
           for i in data:            
             item = QtGui.QTableWidgetItem(i)        
             self.tableWidget.setItem(n, 0,item)
             item = QtGui.QTableWidgetItem()
             self.tableWidget.setItem(n, 1,item) #set blank memory site
             n+=1
        if light == "Sun":
           stdlight = 'sun'
           global sun_data_show
           self.tableWidget.clearContents()  
           n=0
           for i in sun_data_show:            
             item = QtGui.QTableWidgetItem(i)        
             self.tableWidget.setItem(n, 0,item)
             item = QtGui.QTableWidgetItem()
             self.tableWidget.setItem(n, 1,item)
             n+=1
        if light == "Custom":
           self.tableWidget.clearContents() 
           stdlight = 'custom'
           for i in range(30):
             item1 = QtGui.QTableWidgetItem()                              
             self.tableWidget.setItem(i, 0,item1) #set blank memory site
             item2 = QtGui.QTableWidgetItem()
             self.tableWidget.setItem(i, 1,item2) #set blank memory site 
########################################################################
    def show_ref_profile(self):
        chk_manul = self.checkBox_5.isChecked()
        if (chk_manul == True) & (stdlight == 'neon'):
            img_show = mpimg.imread('etc//Neon lamp reference profile and spectrum.png')
            plt.figure(4321)
            plt.gcf().canvas.set_window_title('Neon reference profile and spectrum')
            plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            plt.axis("off")        
            plt.imshow(img_show)
            plt.show()           
        if (chk_manul == True) & (stdlight == 'sun'):
            img_show = mpimg.imread('etc//Sun reference profile and spectrum.png')
            plt.figure(4321)
            plt.gcf().canvas.set_window_title('Sun reference profile and spectrum')
            plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            plt.axis("off")        
            plt.imshow(img_show)
            plt.show()       
        if (chk_manul == True) & (stdlight == 'custom'):
            print 'custom '            
        if (chk_manul == False): 
            print 'No manual'
########################################################################                     
    def calibrate(self):
        global neon_data
        global sun_data
        global x_p
        global y_nm
        global coef
        global cov
        global sigma
        global stdlight        
        chk_auto = self.checkBox_4.isChecked()
        chk_manul = self.checkBox_5.isChecked()
        if (chk_auto == True) & (stdlight == 'neon'):
           x_p,y_nm = auto_calibration_neon(self)
           self.tableWidget.clearContents()
           n=0
           for i in y_nm:            
               item = QtGui.QTableWidgetItem(str(i))        
               self.tableWidget.setItem(n, 0,item)      
               n+=1
           n=0
           for i in x_p:            
               item = QtGui.QTableWidgetItem(str(i))        
               self.tableWidget.setItem(n, 1,item)      
               n+=1            
        if (chk_manul == True) & (stdlight == 'neon') :    
           input_x = np.array([],dtype=str)
           for i in range(neon_data.size):
              item = self.tableWidget.item(i, 1) #get input_x memory site        
              input_x = np.append(input_x,item.text())#translate to unicode
              if input_x[i] == '':
                 input_x[i] = '0'    #let blank = 0 
           input_x = np.array(input_x,dtype=float)           
           x_p = np.array([],dtype=float) # return to ori
           y_nm = np.array([],dtype=float)
           for i in range(neon_data.size):
               if input_x[i] > 0.1: 
                  x_p = np.append(x_p,input_x[i])
                  y_nm = np.append(y_nm,neon_data[i])  
        if (chk_auto == True) & (stdlight == 'sun'):
           x_p,y_nm = auto_calibration_sun(self)
           self.tableWidget.clearContents()
           n=0
           for i in y_nm:            
               item = QtGui.QTableWidgetItem(str(i))        
               self.tableWidget.setItem(n, 0,item)      
               n+=1
           n=0
           for i in x_p:            
               item = QtGui.QTableWidgetItem(str(i))        
               self.tableWidget.setItem(n, 1,item)      
               n+=1            
        if (chk_manul == True) & (stdlight == 'sun') :    
           input_x = np.array([],dtype=str)
           for i in range(sun_data.size):
              item = self.tableWidget.item(i, 1)        
              input_x = np.append(input_x,item.text())#translate to unicode
              if input_x[i] == '':
                 input_x[i] = '0'    #let blank = 0 
           input_x = np.array(input_x,dtype=float)           
           x_p = np.array([],dtype=float) # return to ori
           y_nm = np.array([],dtype=float)
           for i in range(sun_data.size):
               if input_x[i] > 0.1: 
                  x_p = np.append(x_p,input_x[i])
                  y_nm = np.append(y_nm,sun_data[i])  

        if (chk_manul == True) & (stdlight == 'custom'):   #custom mode 
           input_x = np.array([],dtype=str)
           input_y = np.array([],dtype=str)
           for i in range(30):
              item = self.tableWidget.item(i, 1)        
              input_x = np.append(input_x,item.text())
              item = self.tableWidget.item(i, 0)        
              input_y = np.append(input_y,item.text())              
              if input_x[i] == '':
                 input_x[i] = '0'    #let blank = 0 
                 input_y[i] = '0'
           input_x = np.array(input_x,dtype=float) 
           input_y = np.array(input_y,dtype=float) 
           x_p = np.array([],dtype=float) # return to ori
           y_nm = np.array([],dtype=float)
           for i in range(30):
               if input_x[i] > 0.1: 
                  x_p = np.append(x_p,input_x[i])
                  y_nm = np.append(y_nm,input_y[i]) 
        from scipy.optimize import curve_fit
        def fun(x,a,b):
            return a*x+b
        coef, cov = curve_fit(fun, x_p, y_nm)
        sigma = np.sqrt(np.diag(cov))
        pm = u'±'
        self.label_14.setText('y(nm)=%.6f(%s%.6f)*x(pix)+%.5f(%s%.6f)'%(coef[0],pm,sigma[0],coef[1],pm,sigma[1]))
########################################################################      
    def current_fomula(self):
        global coef
        global cov
        global sigma
        pm = u'±'
        self.label_16.setText('y(nm)=%.6f(%s%.6f)*x(pix)+%.5f(%s%.6f)'%(coef[0],pm,sigma[0],coef[1],pm,sigma[1]))
########################################################################
    def plot_cali_profile(self):
        global path
        global times_cali_plot
        global box
        global coef
        img = Image.open(path)
        xsize, ysize = img.size
        if img.mode[0] == 'I':
           pix_gray = np.asarray(img.getdata()).reshape(ysize, xsize)
           pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16
        else:   
           pix_gray = np.asarray(img.getdata().convert('L')).reshape(ysize, xsize)
        xpixel = np.asarray(range(xsize))+1 #xpixel value
        x_wave = coef[0]*xpixel+coef[1]       
        times_cali_plot = times_cali_plot+1 
        plot_box = pix_gray[box[0]:box[1]]#intensity us averagy
        intensity_box = plot_box.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row       
        filename = path.split('/')[len(path.split('/'))-1]
        plt.figure(3000+times_cali_plot)
        plt.gcf().canvas.set_window_title("%s Calibrated Profile(Y=%d to %d)"%(filename,int(box[0])+1,int(box[1])))
        plt.xlim(x_wave.min(),x_wave.max())
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('intensity (counts)')
        plt.minorticks_on()
        plt.grid(True)
        plt.tight_layout()
        plt.plot(x_wave,intensity_box,'r-')          
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range
        plt.show()         
########################################################################             
    def Save_calibration_data(self):
        global path
        global box
        global stdlight
        global x_p
        global y_nm
        global coef
        global cov
        global sigma
        chk_auto = self.checkBox_4.isChecked()
        if chk_auto == True:
            state = 'auto'
        else:
            state = 'manual'
        pm = '±'
        savepath = 'Save//Wavelength_calibration' #r'C:\Program Files\arbitrary'
        if not os.path.exists(savepath):
           os.makedirs(savepath)                        
        filename1 = path.split(r'/')[len(path.split(r'/'))-1]
        filename = 'Save//Wavelength_calibration//%s_wavelength_calibration_data(%s).csv'%(filename1,state)
        file = open(filename , "w")
        file.write('# %s calibration data (%s)\n'%(filename1,stdlight))
        file.write('# Input Data : \n')               
        file.write('# box_y1 box_y2 \n')
        file.write('  %d %d \n' %(box[0],box[1])) #box info      
        file.write('# Wavelength(nm) x_pixel\n') 
        for i in range(x_p.size):         
            line = '  %s %s\n'%(str(y_nm[i]),str(x_p[i]))
            file.write(line)
        file.write('# Calibration  Results : \n')
        file.write('# y(nm)=%.7f%s%.6fx(pix)+%.4f%s%.6f \n'%(coef[0],pm,sigma[0],coef[1],pm,sigma[1]))
        file.write('  %.9f %.9f \n'%(coef[0],coef[1]))
        file.write('  %.9f %.9f \n'%(cov[0][0],cov[0][1]))
        file.write('  %.9f %.9f \n'%(cov[1][0],cov[1][1]))
        file.close()
        print r'Wavelength calibration data .csv file has been saved to folder: Save\Wavelength_calibration'
########################################################################             
    def Load_calibration_data(self):
        global path_data
        global box
        global x_p
        global y_nm
        global coef
        global cov
        global sigma
        pm = u'±'
        path_data, _ = QtGui.QFileDialog.getOpenFileName()
        data = np.genfromtxt(path_data,dtype=float,delimiter=' ')       
        coef = data[int(data.shape[0])-3] #count from last array  (3 fixed items) 
        cov = data[int(data.shape[0])-2:int(data.shape[0])]
        box = data[0]       
        x_p = data[1:int(data.shape[0])-3,1]
        y_nm = data[1:int(data.shape[0])-3,0]
        sigma = np.sqrt(np.diag(cov))*3
        self.label_16.setText('y(nm)=%.6f(%s%.6f)*x(pix)+%.5f(%s%.6f)'%(coef[0],pm,sigma[0],coef[1],pm,sigma[1]))
        if box[1] > 0:
           self.lineEdit_2.setText(str(int(box[0])+1))
           self.lineEdit_3.setText(str(int(box[1])))
        self.tableWidget.clearContents()        
        n=0
        for i in y_nm:            
            item = QtGui.QTableWidgetItem(str(i))        
            self.tableWidget.setItem(n, 0,item)      
            n+=1
        n=0
        for i in x_p:            
            item = QtGui.QTableWidgetItem(str(i))        
            self.tableWidget.setItem(n, 1,item)      
            n+=1
########################################################################             
    def Save_profile_value(self):
        global path
        global box
        global coef
        img = Image.open(path)
        xsize, ysize = img.size
        if img.mode[0] == 'I':
           pix_gray = np.asarray(img.getdata()).reshape(ysize, xsize)
           pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16
        else:   
           pix_gray = np.asarray(img.getdata().convert('L')).reshape(ysize, xsize)
        xpixel = np.asarray(range(xsize))+1 #xpixel value
        x_wave = coef[0]*xpixel+coef[1]       
        plot_box = pix_gray[box[0]:box[1]]#intensity us averagy
        intensity = plot_box.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row                 
        save_data = np.concatenate((x_wave.reshape(xsize,1), intensity.reshape(xsize,1)), axis=1) #兩組data結合成(x,y)
        savepath = 'Save//Wavelength_calibration' #r'C:\Program Files\arbitrary'
        if not os.path.exists(savepath):
           os.makedirs(savepath)
        filename1 = path.split(r'/')[len(path.split(r'/'))-1]
        filename = 'Save//Wavelength_calibration//%s_profile_value.csv'%(filename1)
        np.savetxt(filename,save_data,delimiter=',',fmt='%.3f')
        print r'Profile value .csv file has been saved to folder: Save\Wavelength_calibration'
########################################################################
    def Load_profile_value_plot(self):
        global times_cali_plot
        path_profile, _ =QtGui.QFileDialog.getOpenFileName()  
        data = np.genfromtxt(path_profile,dtype=float,delimiter=',')        
        filename = path_profile.split('/')[len(path_profile.split('/'))-1]
        times_cali_plot += 1        
        plt.figure(6000+times_cali_plot)
        plt.gcf().canvas.set_window_title(filename)             
        plt.xlim(data[:,0].min(),data[:,0].max())
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('intensity (counts)')
        plt.minorticks_on()
#        plt.grid(True)
        plt.tight_layout()    
        plt.plot(data[:,0],data[:,1],'b-')
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
        plt.show()          
########################################################################
    def plot_profile_and_spectrum(self):
        global path
        global times_cali_plot
        global x_p
        global y_nm        
        global box
        global coef         
        img = Image.open(path)
        xsize, ysize = img.size
        if img.mode[0] == 'I'or img.mode[0] == 'F' :
           pix_gray = np.asarray(img.getdata()).reshape(ysize, xsize)
           pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16           
        else:   
           pix_gray = np.asarray(img.getdata().convert('L')).reshape(ysize, xsize)        
        chk_psi = self.checkBox_11.isChecked() #profile stake image
        chk_puid = self.checkBox_12.isChecked()#profile up image down
        chk_sl = self.checkBox_3.isChecked()#show lebal
        xpixel = np.asarray(range(xsize))+1 #x-axis value
        x_wave = coef[0]*xpixel+coef[1]
        title = self.lineEdit_4.text()
        def label2(intensity_box):
           xx_label = coef[0]*x_p+coef[1]
           x_p_int = np.array(x_p,dtype=int)
           yy_label = intensity_box[x_p_int]  #該波長位置所對應的強度
           text = np.array(y_nm,dtype=str)
           for i in range(xx_label.size):
              if yy_label[i] > 228:
                 plt.annotate(text[i], xy=(xx_label[i], yy_label[i]), xytext=(xx_label[i], yy_label[i]+10),#textcoords='axes fraction',xytext=(xx_label[i], yy_label[i]+5)
                              arrowprops=dict(arrowstyle="->",color='blue'),color='blue',
                              fontsize=11,horizontalalignment='left',verticalalignment='bottom')                  
              elif (np.abs(xx_label[i]-xx_label[abs(i-1)]) < 1.6) & (i-1 >= 0 ):
                  if (np.abs(xx_label[i]-xx_label[abs(i-1)]) < 0.8) & (i-1 >= 0 ):
                     plt.annotate(text[i], xy=(xx_label[i], yy_label[i]), xytext=(xx_label[i]-7, yy_label[i]+30),#textcoords='axes fraction',xytext=(xx_label[i], yy_label[i]+5)
                                  arrowprops=dict(arrowstyle="->",color='blue'), color='blue',
                                  rotation=90,fontsize=11,horizontalalignment='left',verticalalignment='bottom')                     
                  else:
                     plt.annotate(text[i], xy=(xx_label[i], yy_label[i]), xytext=(xx_label[i]-4, yy_label[i]+30),#textcoords='axes fraction',xytext=(xx_label[i], yy_label[i]+5)
                                  arrowprops=dict(arrowstyle="->",color='blue'), color='blue',
                                  rotation=90,fontsize=11,horizontalalignment='left',verticalalignment='bottom')           
              else :
                 plt.annotate(text[i], xy=(xx_label[i], yy_label[i]), xytext=(xx_label[i], yy_label[i]+30),#textcoords='axes fraction',xytext=(xx_label[i], yy_label[i]+5)
                              arrowprops=dict(arrowstyle="->",color='blue'), color='blue',
                              rotation=90,fontsize=11,horizontalalignment='left',verticalalignment='bottom')                  
        if chk_psi == True: 
           times_cali_plot = times_cali_plot+1
           plot_box = pix_gray[box[0]:box[1]]#intensity us averagy
           intensity_box = plot_box.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row                               
           high = np.asarray(intensity_box,dtype=int)
           filename1 = path.split('/')[len(path.split('/'))-1]
           plt.figure(5105+times_cali_plot)
           plt.title('%s'%(title))
           plt.gcf().canvas.set_window_title("%s Calibrated Profile(Y=%d to %d)"%(filename1,int(box[0])+1,int(box[1])))        
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('intensity (counts)')                        
           plt.minorticks_on()            
           pixo = img.crop((0,int(box[0]),xsize,int(box[1])))#left up right down
           if img.mode[0] == 'I'or img.mode[0] == 'F' or img.mode[0] == 'L':
              pixo = pixo.convert('F').resize((xsize,255),Image.BILINEAR)#zoom in (32-bit floating)           
              pix = np.asarray([pixo.getdata()]).reshape(255,xsize)
              pix[pix < 0] = pix[pix < 0]+2**16
              if high.max() > 255: 
                 high = high/(65535/255) #change linear scale by 65535/255       
              for ii in range(xsize): #set to white for out of profile intensity region 
                  pix[high[ii]+1:255,ii] = [0]# need change linear scale by 65535/255                     
              pix = pix[:,np.argsort(x_wave)]
              plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 255, 0),interpolation='bilinear',cmap='Greys_r')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                                                             
           else:
              pixo = pixo.resize((xsize,255),Image.BILINEAR)#zoom in (32-bit floating)           
              pix = np.asarray([pixo.getdata()]).reshape(255,xsize,3)              
              for ii in range(xsize): #set to white for out of region 
                  pix[high[ii]+1:255,ii] = [254,254,254]# 
              pix = pix[:,np.argsort(x_wave),:]
              plt.imshow(256-pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 255, 0),interpolation='bilinear')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                                                             
           plt.ylim(255,0)
           if chk_sl == True:
              label2(intensity_box)                      
           plt.gca().invert_yaxis()
           plt.locator_params(axis='x', tight=True,nbins=30)
           plt.tight_layout()
           plt.show() 
############################################################################                     
        if chk_puid == True: 
           times_cali_plot = times_cali_plot+1
           plot_box = pix_gray[box[0]:box[1]]#intensity us averagy
           intensity_box = plot_box.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row                  
           img_show = mpimg.imread(path) #use matplolib to plot image          
           img_show = img_show[box[0]:box[1]]#corp
           filename1 = path.split('/')[len(path.split('/'))-1]
           plt.figure(7355+times_cali_plot)
           plt.gcf().canvas.set_window_title("%s Calibrated Profile(Y=%d to %d)"%(filename1,int(box[0])+1,int(box[1])))                              
           ###
           sp_up = plt.subplot2grid((4,1), (0, 0),rowspan=3)
           plt.title('%s'%(title))           
           plt.xlim(x_wave.min(),x_wave.max())           
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('intensity (counts)')           
           plt.tight_layout()
           plt.minorticks_on()
#           plt.grid(True) 
           plt.ylim(0,270)          
           if (img.mode[0] == 'I'or img.mode[0] == 'F' or img.mode[0] == 'L') and intensity_box.max() > 255: 
              intensity_box  = intensity_box /(65535/255)                               
           plt.plot(x_wave,intensity_box,'k-')
           plt.locator_params(axis='x', tight=True,nbins=30) 
           if chk_sl == True:
              label2(intensity_box)            
           sp_down = plt.subplot2grid((4,1), (3, 0),rowspan=1,sharex=sp_up)  
           plt.axis("off")                     
           plt.tight_layout()
           pixo = img.crop((0,int(box[0]),xsize,int(box[1])))#left up right down    
           if img.mode[0] == 'I' or img.mode[0] == 'F' or img.mode[0] == 'L' :
              pixo = pixo.convert('F').resize((xsize,2),Image.BILINEAR)#zoom in (32-bit floating)                          
              pix = np.asarray([pixo.getdata()]).reshape(2,xsize)              
              pix = pix[:,np.argsort(x_wave)]
              plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 65, 0),interpolation='bilinear',cmap='Greys_r')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                        
           else:              
              pixo = pixo.resize((xsize,2),Image.BILINEAR)#zoom in BILINEAR BICUBIC
              pix = np.asarray([pixo.getdata()],dtype=float).reshape(2,xsize,3)            
              pix = pix[:,np.argsort(x_wave),:]
              plt.imshow(256-pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 100, 0),interpolation='bilinear')# bilinear bicubic aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)           
           plt.locator_params(axis='x', tight=True,nbins=20)
           plt.show()  
########################################################################          
########################################################################         
########################################################################  
    def retranslateUi(self, MainWindow): #Python Spectrum Application
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PySA 1.1  (build 20160905)", None, QtGui.QApplication.UnicodeUTF8))
        ###tab_2  
        self.groupBox_t2re.setTitle(QtGui.QApplication.translate("MainWindow", "ReadMe", None, QtGui.QApplication.UnicodeUTF8)) 
        self.groupBox_abs.setTitle(QtGui.QApplication.translate("MainWindow", "Simple Calculate absorbance", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_abs1.setText(QtGui.QApplication.translate("MainWindow", "Add Blank", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_abs2.setText(QtGui.QApplication.translate("MainWindow", "Add Analyte", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_abs3.setText(QtGui.QApplication.translate("MainWindow", "Show Absorbance Spectra", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_abs4.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_abs.setItemText(0, QtGui.QApplication.translate("MainWindow", "Select and Save", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_abs2.setItemText(0, QtGui.QApplication.translate("MainWindow", "Select and Show", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_s.setTitle(QtGui.QApplication.translate("MainWindow", "Standard solution calibration and Analyte concentration", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s4.setText(QtGui.QApplication.translate("MainWindow", "Add std. solution", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s6.setText(QtGui.QApplication.translate("MainWindow", "Add blank solution", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s1.setText(QtGui.QApplication.translate("MainWindow", "The wavelength to be analyzed(nm):", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_s.setItemText(0, QtGui.QApplication.translate("MainWindow", "Show Abs. spectra(all in one)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s5.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s7.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s8.setText(QtGui.QApplication.translate("MainWindow", "Save Calibration Data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s2.setText(QtGui.QApplication.translate("MainWindow", "Result:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s9.setText(QtGui.QApplication.translate("MainWindow", "Load Analyte and Calculate Concentration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s3.setText(QtGui.QApplication.translate("MainWindow", "Absorbance = ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s10.setText(QtGui.QApplication.translate("MainWindow", "Load Calibration Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_s11.setText(QtGui.QApplication.translate("MainWindow", "Save Report", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s5.setText(QtGui.QApplication.translate("MainWindow", "At wavelength(nm) =", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s7.setText(QtGui.QApplication.translate("MainWindow", "(you can enter by manual)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s9.setText(QtGui.QApplication.translate("MainWindow", "Analyte Concentration(M) = ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_s11.setText(QtGui.QApplication.translate("MainWindow", "Enter analyte name:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_t4_about.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        ###tab_1
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Load Image", None, QtGui.QApplication.UnicodeUTF8))#Load Image
        self.groupBox_t1select.setTitle(QtGui.QApplication.translate("MainWindow", "Select image area", None, QtGui.QApplication.UnicodeUTF8)) 
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "The width is fixed equal to full width of image.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Y2 pixel (down)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Y1 pixel (up)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Show Profile without Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_t1wc.setTitle(QtGui.QApplication.translate("MainWindow", "WaveLength Calibration", None, QtGui.QApplication.UnicodeUTF8)) 
        self.checkBox_4.setText(QtGui.QApplication.translate("MainWindow", "Auto Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_5.setText(QtGui.QApplication.translate("MainWindow", "Manual Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(0, QtGui.QApplication.translate("MainWindow", "Select Std. Light source", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(1, QtGui.QApplication.translate("MainWindow", "Neon Lamp", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(2, QtGui.QApplication.translate("MainWindow", "Sun", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(3, QtGui.QApplication.translate("MainWindow", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(3).setText(QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(4).setText(QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(5).setText(QtGui.QApplication.translate("MainWindow", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(6).setText(QtGui.QApplication.translate("MainWindow", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(7).setText(QtGui.QApplication.translate("MainWindow", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(8).setText(QtGui.QApplication.translate("MainWindow", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(9).setText(QtGui.QApplication.translate("MainWindow", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(10).setText(QtGui.QApplication.translate("MainWindow", "11", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(11).setText(QtGui.QApplication.translate("MainWindow", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(12).setText(QtGui.QApplication.translate("MainWindow", "13", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(13).setText(QtGui.QApplication.translate("MainWindow", "14", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(14).setText(QtGui.QApplication.translate("MainWindow", "15", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(15).setText(QtGui.QApplication.translate("MainWindow", "16", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(16).setText(QtGui.QApplication.translate("MainWindow", "17", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(17).setText(QtGui.QApplication.translate("MainWindow", "18", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(18).setText(QtGui.QApplication.translate("MainWindow", "19", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(19).setText(QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(20).setText(QtGui.QApplication.translate("MainWindow", "21", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(21).setText(QtGui.QApplication.translate("MainWindow", "22", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(22).setText(QtGui.QApplication.translate("MainWindow", "23", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(23).setText(QtGui.QApplication.translate("MainWindow", "24", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(24).setText(QtGui.QApplication.translate("MainWindow", "25", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(25).setText(QtGui.QApplication.translate("MainWindow", "26", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(26).setText(QtGui.QApplication.translate("MainWindow", "27", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(27).setText(QtGui.QApplication.translate("MainWindow", "28", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(28).setText(QtGui.QApplication.translate("MainWindow", "29", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(29).setText(QtGui.QApplication.translate("MainWindow", "30", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "WaveLength (nm)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "InPut X pixel", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Residual", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("MainWindow", "Save calibration data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Result Formula:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_t1plot.setTitle(QtGui.QApplication.translate("MainWindow", "Show Wavelength-calibrated Profile", None, QtGui.QApplication.UnicodeUTF8)) 
        self.pushButton_11.setText(QtGui.QApplication.translate("MainWindow", "Use current formula ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_10.setText(QtGui.QApplication.translate("MainWindow", "Load Calibration Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("MainWindow", "Show Profile with Calibrated wavelength", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_8.setText(QtGui.QApplication.translate("MainWindow", "Save Profile value", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_9.setText(QtGui.QApplication.translate("MainWindow", "Load Profile value and Plot", None, QtGui.QApplication.UnicodeUTF8))

        self.groupBox2.setTitle(QtGui.QApplication.translate("MainWindow", "Plot Wavelength-calibrated Profile with Spectrum Image", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("MainWindow", "Show peak wavelength label", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_11.setText(QtGui.QApplication.translate("MainWindow","Type 1: Profile and spectrum in the same figure", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_12.setText(QtGui.QApplication.translate("MainWindow","Type 2: Profile in up panel , spectrum in down panel ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_20.setText(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Input figure Title :", None, QtGui.QApplication.UnicodeUTF8))

        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "README", None, QtGui.QApplication.UnicodeUTF8))
        self.README.setDocumentTitle(QtGui.QApplication.translate("MainWindow", "README", None, QtGui.QApplication.UnicodeUTF8))

def auto_calibration_neon(self):
    global path
    global box #np.array([0,0],dtype=int)
    global neon_data
    global x_p
    global y_nm
    import scipy.signal as signal
    img = Image.open(path)
    xsize, ysize = img.size
    pix_gray = np.asarray(img.getdata().convert('L')).reshape(ysize, xsize)
    xpixel = np.asarray(range(xsize))+1 #xpixel value         
    plot_box = pix_gray[box[0]:box[1]]#intensity us averagy
    intensity = plot_box.sum(axis=0)/(box[1]-box[0]+1.)#axis=0 is sum along row                          
    x_p = np.array([],dtype=float) # return to ori
    y_nm = np.array([],dtype=float)
    find_width1 = np.arange(1,5)#5 
    peaks = signal.find_peaks_cwt(intensity, find_width1)
    peakmax = xpixel[np.where(intensity == intensity[peaks].max())]
    if np.average(intensity[0:peakmax]) > np.average(intensity[peakmax:xsize]):
           print 'left region is red, right region is blue'
           x_p = np.append(x_p,peakmax)
           y_nm = np.append(y_nm,585.25) #neon_data[19]
           peaks2 = np.asarray(signal.find_peaks_cwt(intensity[0:peakmax], np.arange(1,32)))       
           peaks2 = peaks2[np.where(intensity[0:peakmax][peaks2] > np.average(intensity[0:peakmax]))]
           peaks3 = np.asarray(signal.find_peaks_cwt(intensity[peakmax:xsize-1], np.arange(1,40)))     
           peaks3 = peaks3[np.where(intensity[peakmax:xsize-1][peaks3] > np.average(intensity[peakmax:xsize-1]))]+peakmax       
           if (len(peaks2) == 20) & (len(peaks3) > 1):           
               x_p = np.append(x_p,peaks2[0:19]) #do not need last one idx=19
               y_nm = np.append(y_nm,neon_data[0:19]) 
               need = peaks3[np.argsort(intensity[peaks3])[::-1][1]] #need 2nd hight
               x_p = np.append(x_p,need)
               y_nm = np.append(y_nm,neon_data[20])
               plt.figure(9999)
               plt.gcf().canvas.set_window_title('Peak searching result') 
               plt.title('Peak searching result')
               plt.xlabel('x (pixel)')
               plt.ylabel('intensity (counts)')
               plt.plot(xpixel,intensity,'b-')
               plt.plot(xpixel[peakmax],intensity[peakmax],'ro')
               plt.plot(xpixel[peaks2[0:19]],intensity[peaks2[0:19]],'bo')
               plt.plot(xpixel[need],intensity[need],'bo')
               plt.show()          
           elif len(peaks3) > 1:
               need = peaks3[np.argsort(intensity[peaks3])[::-1][1]] #need 2nd hight
               x_p = np.append(x_p,need)
               y_nm = np.append(y_nm,neon_data[20])          
               plt.figure(9999)
               plt.gcf().canvas.set_window_title('Peak searching result') 
               plt.title('Peak searching result')
               plt.xlabel('x (pixel)')
               plt.ylabel('intensity (counts)')               
               plt.plot(xpixel,intensity,'b-')
               plt.plot(xpixel[peakmax],intensity[peakmax],'ro')
               plt.plot(xpixel[need],intensity[need],'bo')
               plt.show()
    else:   
           print 'left region is blue, right region is red'
           x_p = np.append(x_p,peakmax)
           y_nm = np.append(y_nm,585.25) #neon_data[19]
           #peaks2 is right
           peaks2 = np.asarray(signal.find_peaks_cwt(intensity[peakmax:xsize-1], np.arange(1,32)))     
           peaks2 = peaks2[np.where(intensity[peakmax:xsize-1][peaks2] > np.average(intensity[peakmax:xsize-1]))]+peakmax             
           peaks3 = np.asarray(signal.find_peaks_cwt(intensity[0:peakmax], np.arange(1,40)))       
           peaks3 = peaks3[np.where(intensity[0:peakmax][peaks3] > np.average(intensity[0:peakmax]))]            
           if (len(peaks2) == 20) & (len(peaks3) > 1):           
               x_p = np.append(x_p,peaks2[1:20])#do not need first one
               y_nm = np.append(y_nm,neon_data[0:19][::-1]) 
               need = peaks3[np.argsort(intensity[peaks3])[::-1][1]] #need 2nd hight
               x_p = np.append(x_p,need)
               y_nm = np.append(y_nm,neon_data[20])
               plt.figure(9999)
               plt.gcf().canvas.set_window_title('Peak searching result') 
               plt.title('Peak searching result')
               plt.xlabel('x (pixel)')
               plt.ylabel('intensity (counts)')              
               plt.plot(xpixel,intensity,'b-')
               plt.plot(xpixel[peakmax],intensity[peakmax],'ro')
               plt.plot(xpixel[peaks2[1:20]],intensity[peaks2[1:20]],'bo')
               plt.plot(xpixel[need],intensity[need],'bo')
               plt.show()          
           elif len(peaks3) > 1:
               need = peaks3[np.argsort(intensity[peaks3])[::-1][1]] #need 2nd hight
               x_p = np.append(x_p,need)
               y_nm = np.append(y_nm,neon_data[20])          
               plt.figure(9999)
               plt.gcf().canvas.set_window_title('Peak searching result') 
               plt.title('Peak searching result')
               plt.xlabel('x (pixel)')
               plt.ylabel('intensity (counts)')               
               plt.plot(xpixel,intensity,'b-')
               plt.plot(xpixel[peakmax],intensity[peakmax],'ro')
               plt.plot(xpixel[need],intensity[need],'bo')
               plt.show()
    return x_p, y_nm 


def readme(self): #tab1
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is i write into Qt 
#    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is Qt object name
#    QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is local document
    self.README.setText('此頁面的功能為將光譜影像轉換成波長-強度圖，同時可以儲存相關參數及數')
    self.README.append('據，最後將波長-強度圖結合光譜影像輸出。\n')
    self.README.append('1. 載入之光譜影像必須是橫向展開且不歪斜')
    self.README.append('2. Auto calibration 僅適用於氖燈光譜')
    self.README.append('3. Manual Calibration 建議使用3種以上的波長') 
    self.README.append('4. 手動輸入選擇影像區域的Y值(最小值=1)後，必需按下[OK]鍵')
    self.README.append('5. .csv文字檔(Calibration data,Profile value)皆儲存於此程式所在的資料夾下')
    self.README.append('    名為Save的資料夾')   
    self.README.append('6. Input_figure_Title欄位僅支援輸入英文與數字')
    self.README.append('7. 萬事皆從[Load Image]開始，除非只要執行第8,9點') 
    self.README.append('8. 可以單獨載入Profile value直接繪製profile')     
    self.README.append('9. 可以單獨載入Calibration data檢視其內容')
    self.README.append('10.當完成第一張光譜波長校正後，可以載入另一張來自於相同拍攝環境的')   
    self.README.append('    光譜影像，選擇使用當前校正公式或載入外部校正資料，可以直接繪製')
    self.README.append('    該光譜影像的profile')
    self.README.append('11.如欲使用下一頁面的計算吸收度及濃度功能,請按下[Save_Profile_value]')   
    self.README.append('    將強度及波長值儲存起來')
    self.README.append('12.目前支援 .jpg .bmp .png .tiff 的24,32bits彩色光譜影像(8bits/channel)')
    self.README.append('    以及8和16bits的單色影像')
    self.README.append('13.載入的光譜影像其路徑和檔名不得出現中文和特殊字符')
    self.README.append('14.如欲離開本程式，按右上角X即可，切勿自行關閉黑色視窗\n')     


def tab2_readme1(self):#textEdit_t2re1
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) 
    self.textEdit_t2re1.setText('Simple Calculate absorbance 計算分析物吸收度')
    self.textEdit_t2re1.append('1. 萬事皆從[Add blank]開始') 
    self.textEdit_t2re1.append('2. blank是指不含分析物的光譜;analyte是指含分析物')
    self.textEdit_t2re1.append('   的光譜 (以紅茶的吸收光譜為例,blank為背景光穿透') 
    self.textEdit_t2re1.append('   容器及溶劑(水)的光譜;analyte為背景光穿透容器及') 
    self.textEdit_t2re1.append('   紅茶的光譜)') 
    self.textEdit_t2re1.append('3. blank亦可為單純的背景光光譜;而此時analyte可')
    self.textEdit_t2re1.append('   為任何會吸收此光的物質光譜(例如顏色片,氣體)') 
    self.textEdit_t2re1.append('4. 所有載入之blank及analyte檔案必須是經由前一分頁')
    self.textEdit_t2re1.append('   (Wavelength Calibration)的[Save Profile value]')
    self.textEdit_t2re1.append('   所產生的.csv檔,檔案路徑不得出現中文和特殊字符')
    self.textEdit_t2re1.append('5. 在按下[Show Absorbance Spectra]之前,務必先在上') 
    self.textEdit_t2re1.append('   方Name欄位反白選取(可多選)要看的吸收光譜') 
    self.textEdit_t2re1.append('6. 可透過下拉選單[Select and Show]單選要看的穿透') 
    self.textEdit_t2re1.append('   光譜') 
    self.textEdit_t2re1.append('7. 所有可輸入欄位僅支援輸入英文與數字') 
    self.textEdit_t2re1.append('8. 所有儲存之檔案均存於此程式所在的資料夾下名為') 
    self.textEdit_t2re1.append('   Save的資料夾\n') 


def tab2_readme2(self):
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) 
    self.textEdit_t2re2.setText('Standard solution calibration and Analyte concentration 以標準品計算分析物濃度')
    self.textEdit_t2re2.append('1. 目前僅適用於External-standard calibration且不能分析螢光激發光譜')
    self.textEdit_t2re2.append('2. 萬事皆從[Add blank solution]開始')
    self.textEdit_t2re2.append('3. 所有載入之blank及analyte檔案必須是經由前一分頁(Wavelength Calibration)的')
    self.textEdit_t2re2.append('   [Save Profile value]所產生的.csv檔,檔案路徑和檔名不得出現中文和特殊字符')
    self.textEdit_t2re2.append('4. 所有可輸入欄位僅支援輸入英文與數字')   
    self.textEdit_t2re2.append('5. 可參考吸收光譜[Show Abs spectra(all in one)],自行輸入欲分析之波長以配合實際情')
    self.textEdit_t2re2.append('   況，預設為出現最大吸收度的波長')
    self.textEdit_t2re2.append('6. 注意容液濃度不可太高,目前單位顯示固定使用體積莫耳濃度M(mol/L)') 
    self.textEdit_t2re2.append('7. 當算出analyte的濃度後,可按下[Save Report],將分析結果儲存成.csv文字檔及.png圖檔 ') 
    self.textEdit_t2re2.append('8. 所有儲存之檔案均存於此程式所在的資料夾下名為Save的資料夾') 
    self.textEdit_t2re2.append('9. 在已載入blank檔案的情況下,可載入calibration data檔案及analyte檔案,直接計算分析') 
    self.textEdit_t2re2.append('   物濃度') 
    self.textEdit_t2re2.append('10.如要更換blank檔案或想全部重來,請按下[Reset]\n')


def tab4_about1(self):
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) 
    self.textEdit_t4re1.setText('PySA (Python Spectrum Application)')
    self.textEdit_t4re1.append('Version: 1.1  Build: 20160905')
    self.textEdit_t4re1.append('主要功能:')
    self.textEdit_t4re1.append('功能1 校正光譜波長,得出光譜影像的強度-波長圖')
    self.textEdit_t4re1.append('功能2 分析光譜得出吸收度與穿透率')
    self.textEdit_t4re1.append('功能3 以外標準品法分析吸收光譜得出樣品濃度\n')   
    self.textEdit_t4re1.append('') 
    self.textEdit_t4re1.append('Created by Yen-Chun Luo Cho (Robert)  Email: lcrobert.rocket@gmail.com')     
    self.textEdit_t4re1.append('Powered by Python, Matplotlib, PySide, PyInstaller\n') 
    self.textEdit_t4re1.append('Copyright 2016 lcrobert\n') 


class ControlMainWindow(QtGui.QMainWindow):
 def __init__(self, parent=None):
     super(ControlMainWindow, self).__init__(parent)
     self.ui = Ui_MainWindow()
     self.ui.setupUi(self)  
 
 def closeEvent(self,event):
     result = QtGui.QMessageBox.question(self,
              "Exit or not...",
              "Are you sure you want to exit ?",
              QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)   
     if result == QtGui.QMessageBox.Yes:
        event.accept()
     else:
        event.ignore()

 def resizeEvent(self,resizeEvent):   
     newheight = resizeEvent.size().height()
     newidth = resizeEvent.size().width()
     self.ui.scrollArea.setGeometry(QtCore.QRect(0, 0, newidth, newheight))

if __name__ == '__main__':
 app = QtGui.QApplication(sys.argv)
 mySW = ControlMainWindow()
 mySW.show()
 sys.exit(app.exec_())	

