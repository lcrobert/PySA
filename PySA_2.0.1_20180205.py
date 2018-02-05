# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from PySide import QtCore, QtGui
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as tick
tick.MultipleLocator(base=25.0)
from PIL import Image 
version = "PySA 2.0.1  (build 20180205)"
path = ""#img path
box = np.array([0,0,0],dtype=int)#(y1,y2,lock)
intensity_box = np.array([],dtype=float)
neon_data = np.array([671.70, 667.83, 659.90, 653.29, 650.65, 640.22, 638.30, 633.44,
                      630.48, 626.65, 621.73, 616.36, 614.31, 609.62, 607.43, 603.00,
                      597.55, 594.48, 588.19, 585.25, 540.06, 534.11,533.08],dtype=float)
sun_data = np.array([656.281, 589.592, 588.995, 527.039, 518.362, 517.270, 516.733, 495.761,
                     486.134, 466.814, 438.355, 434.047, 430.8, 422.673 , 410.175, 396.847, 393.368],dtype=float)
hg_data = np.array([579.2, 577.0, 546.0, 435.8, 404.6],dtype=float)

ylist = []
xlist = []        
result_peak = np.array([],dtype=float)
result_max_x = np.array([],dtype=float)
result_max_y = np.array([],dtype=float) 
select_wave = np.array([],dtype=float) 

poly_order = 1
x_p = np.array([],dtype=float)
y_nm = np.array([],dtype=float)
coef = np.array([],dtype=float)
sigma_p = np.array([],dtype=float) 
rs = 0.
rms = 0.
cali_formula = ''

def intensitybox(path,box):
    img = Image.open(path)
    xsize, ysize = img.size
    pix_area = img.crop((0,box[0],xsize,box[1]))#left up(idx) right down(nth)
    if img.mode == 'RGBA': pix_area = pix_area.convert('RGB') 
    if img.mode[0] == 'I' or img.mode[0] == 'L' or img.mode[0] == 'F' :
       pix_gray = np.asarray(pix_area.getdata()).reshape(box[1]-box[0], xsize)#dirctive get grey scale
       pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16  
    else:   
       pix = np.asarray(pix_area).reshape(box[1]-box[0],xsize,3)#get rgb
#          luma(BT.709)=R*0.2126 + G*0.7152 + B*0.0722
#          luma(BT.601)=R*0.299 + G*0.587 + B*0.114
#       pix_gray = pix[:,:,0]*0.2126+pix[:,:,1]*0.7152+pix[:,:,2]*0.0722
       pix_gray = pix[:,:,0]*0.333+pix[:,:,1]*0.333+pix[:,:,2]*0.333
    plot_x = np.asarray(range(xsize))+1 #set x-axis +1      
    intensity_box = pix_gray.sum(axis=0)/(box[1]-box[0])   
    return plot_x, intensity_box

def xwave(x):
    if coef.size == 2:           
       x_wave = coef[0]*x+coef[1] 
    if coef.size == 3:           
       x_wave = coef[0]*x**2+coef[1]*x+coef[2]
    if coef.size == 4:           
       x_wave = coef[0]*x**3+coef[1]*x**2+coef[2]*x+coef[3]
    if coef.size == 5:           
       x_wave = coef[0]*x**4+coef[1]*x**3+coef[2]*x**2+coef[3]*x+coef[4]
    return x_wave
 
def chk_cht(text):
    return any(u'\u4e00' <= char <= u'\u9fbb' for char in text)    
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(970, 710)
################################################################
        self.scrollArea = QtGui.QScrollArea()#self.centralwidget
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 990, 730))  #1000, 740     
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)#AlwaysOn        
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        MainWindow.setCentralWidget(self.scrollArea)             
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 960, 700))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setItalic(True)                
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.scrollArea.setWidget(self.tabWidget)
        self.scrollArea.ensureWidgetVisible(self.tabWidget)        
###########################################################            
        self.tab_1 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_1, "Spectral Image Analysis")        
        self.groupBox_t1select = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1select.setGeometry(QtCore.QRect(17, 54, 340, 102))
        self.label_4 = QtGui.QLabel(self.groupBox_t1select)#first label
        self.label_4.setGeometry(QtCore.QRect(15, 15, 340, 31))
        self.pushButton = QtGui.QPushButton(self.tab_1)#load image
        self.pushButton.setGeometry(QtCore.QRect(14, 13, 110, 32))
        font = QtGui.QFont() #set for tabwidget label
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setWeight(75)#bold size
        font.setBold(True)
        self.pushButton.setFont(font)
        self.label = QtGui.QLabel(self.tab_1) #y2 pixel
        self.label.setGeometry(QtCore.QRect(31, 128, 112, 21))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label_3 = QtGui.QLabel(self.tab_1) #y1 pixel
        self.label_3.setGeometry(QtCore.QRect(31, 101, 89, 21))
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_1)# y1
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 100, 76, 20))
        self.lineEdit_3 = QtGui.QLineEdit(self.tab_1)#y2
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 127, 76, 20))
        font.setBold(False)
        self.lineEdit_3.setFont(font)
        self.lineEdit_2.setFont(font)                
        self.label_7 = QtGui.QLabel(self.tab_1)#Image
        self.label_7.setGeometry(QtCore.QRect(133, 7, 63, 21))
        self.label_8 = QtGui.QLabel(self.tab_1) #size
        self.label_8.setGeometry(QtCore.QRect(133, 29, 61, 21))
        self.label_9 = QtGui.QLabel(self.tab_1) #image path
        self.label_9.setGeometry(QtCore.QRect(182, 8, 870, 21))
        self.label_9.setText("")
        self.label_10 = QtGui.QLabel(self.tab_1) #image size
        self.label_10.setGeometry(QtCore.QRect(172, 29, 138, 21))        
        self.label_10.setText("")
        self.label_9.setFont(font)        
        self.label_10.setFont(font)        
        self.pushButton_2 = QtGui.QPushButton(self.tab_1) #show profile in pixel
        self.pushButton_2.setGeometry(QtCore.QRect(18, 164, 186, 32))
        self.pushButton_4 = QtGui.QPushButton(self.tab_1)#ok groupBox_t1select
        self.pushButton_4.setGeometry(QtCore.QRect(260, 106, 71, 32))
        font.setBold(True)
        self.pushButton_2.setFont(font)        
        self.pushButton_4.setFont(font)
        font.setBold(False)
        self.pushButton_geoadj = QtGui.QPushButton(self.tab_1) #show profile in pixel
        self.pushButton_geoadj.setGeometry(QtCore.QRect(250, 164, 170, 32))
        self.pushButton_geoadj.setText("Straighten arc llines... ") 
        self.pushButton_geoadj.setFont(font)        
        self.groupBox_t1wc = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1wc.setGeometry(QtCore.QRect(17, 207, 407, 455))
        self.stdLight = QtGui.QComboBox(self.groupBox_t1wc)
        self.stdLight.setGeometry(QtCore.QRect(15, 28, 170, 28))        
        self.stdLight.setEditable(False)
        self.stdLight.setMaxVisibleItems(6)
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.stdLight.addItem("")
        self.stdLight.addItem("")        
        self.poly_cali = QtGui.QComboBox(self.groupBox_t1wc)
        self.poly_cali.setGeometry(QtCore.QRect(208, 28, 182, 28))
        self.poly_cali.setEditable(False)
        self.poly_cali.setMaxVisibleItems(5)
        self.poly_cali.addItem("")
        self.poly_cali.addItem("")
        self.poly_cali.addItem("")
        self.poly_cali.addItem("")       
        self.poly_cali.addItem("")
        font.setPointSize(11)
        self.stdLight.setFont(font)
        self.poly_cali.setFont(font)           
        self.tableWidget = QtGui.QTableWidget(self.groupBox_t1wc)
        self.tableWidget.setGeometry(QtCore.QRect(14, 71, 375, 163))
        font.setPointSize(9)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(30)
        for item_idx in range(30):
            item = QtGui.QTableWidgetItem(str(item_idx+1))
            self.tableWidget.setVerticalHeaderItem(item_idx, item)                             
            item1 = QtGui.QTableWidgetItem('')                              
            self.tableWidget.setItem(item_idx, 0,item1) #set blank memory site
            item2 = QtGui.QTableWidgetItem('')
            self.tableWidget.setItem(item_idx, 1,item2) #set blank memory site
            item3 = QtGui.QTableWidgetItem('')
            self.tableWidget.setItem(item_idx, 2,item3)        
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
        self.pushButton_5.setGeometry(QtCore.QRect(14, 245, 103, 32))
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_5.setFont(font)
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_t1wc)#load  cali
        self.pushButton_6.setGeometry(QtCore.QRect(216, 245, 171, 32))
        self.label_13 = QtGui.QLabel(self.groupBox_t1wc) #result
        self.label_13.setGeometry(QtCore.QRect(20, 280, 70, 21))
        font.setBold(False)
        self.label_13.setFont(font)
        self.label_13.setTextFormat(QtCore.Qt.PlainText)
        self.results = QtGui.QTextEdit(self.groupBox_t1wc)
        self.results.setGeometry(QtCore.QRect(20, 305, 375, 138))#(9, 20, 389, 286)
        self.results.setFont(font)
        self.results.setReadOnly(True)        
        self.groupBox_t1plot = QtGui.QGroupBox(self.tab_1)
        self.groupBox_t1plot.setGeometry(QtCore.QRect(455, 54, 480, 115))
        self.pushButton_7 = QtGui.QPushButton(self.groupBox_t1plot) #plot profile in wavelength
        self.pushButton_7.setGeometry(QtCore.QRect(17, 27, 233, 32))        
        font.setBold(True)
        self.pushButton_7.setFont(font)        
        self.pushButton_9 = QtGui.QPushButton(self.groupBox_t1plot)#load profiles and plot
        self.pushButton_9.setGeometry(QtCore.QRect(272, 27, 196, 32))#143 70 
        self.checkBox_11 = QtGui.QCheckBox(self.groupBox_t1plot)#image in profile shap
        self.checkBox_11.setGeometry(QtCore.QRect(21, 58, 400, 36))
        font.setBold(False)
        font.setPointSize(11)
        self.checkBox_11.setFont(font)
        self.pushButton_cn = QtGui.QPushButton(self.groupBox_t1plot) #continuum normalization
        self.pushButton_cn.setGeometry(QtCore.QRect(272, 70, 196, 32))        
        self.pushButton_cn.setText("Continuum normalization...")
        font.setPointSize(12)        
        self.pushButton_cn.setFont(font)                
        self.groupBox = QtGui.QGroupBox(self.tab_1)#readme
        self.groupBox.setGeometry(QtCore.QRect(455, 337, 480, 324))#(x, y, l,w )
        self.groupBox.setFont(font)#455, 305, 480, 357
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.README = QtGui.QTextEdit(self.groupBox)
        self.README.setGeometry(QtCore.QRect(8, 25, 464, 198))#(9, 20, 389, 286)
        font.setPointSize(10)
        self.README.setFont(font)
        self.README.setReadOnly(True)           
        self.README_about = QtGui.QTextEdit(self.groupBox)
        self.README_about.setGeometry(QtCore.QRect(8, 240, 464, 77))#(9, 20, 389, 286)
        font.setPointSize(10)
        self.README_about.setFont(font)      
        self.README_about.setReadOnly(True)        
###################################################################
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.plotProfile)
        self.pushButton_4.clicked.connect(self.plot_region)#plot region ok button
        self.stdLight.activated[str].connect(self.load_stdlight)
        self.poly_cali.activated[str].connect(self.load_poly_cali)
        self.pushButton_5.clicked.connect(self.calibrate)#calibrate button
        self.pushButton_6.clicked.connect(self.Load_calibration_data) #load cali data
        self.pushButton_7.clicked.connect(self.plot_cali_profile)#plot cali profile
        self.pushButton_9.clicked.connect(self.Load_profile_value_plot_nw)
        self.pushButton_cn.clicked.connect(self.continuum_nw) 
        self.pushButton_geoadj.clicked.connect(self.geoadj_nw) 
        readme(self)
        readme_about(self)
        self.label_9.mousePressEvent = self.reopenimg
#        self.label_qr = QtGui.QLabel(self.tab_1)
#        self.label_qr.setGeometry(QtCore.QRect(750, 500, 148, 148))
#        pixmap = QtGui.QPixmap('REF//lcycblog.png')#148*148
#        self.label_qr.setPixmap(pixmap)
#        self.label_qr.show()
##################################################################################        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setItalic(False)        
        self.tab_1.setFont(font)
        self.tabWidget.setCurrentIndex(0)
        self.stdLight.setCurrentIndex(0)        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
##################################################################################        
# Tab_1 start ##########################################################################        
##################################################################################        
    def openFile(self):      
        global path
        global y0
        path_op, _ = QtGui.QFileDialog.getOpenFileName(None, "Open Image...",os.getcwd(), "Image (*.jpg *.jpeg *.tif *.tiff)") #
        if path_op == "":return
        path = path_op       
        img = Image.open(path)
        if img.mode == 'RGBA': img = img.convert('RGB')        
        self.label_9.setText(path)
        print 'The image mode is ', img.mode #I is wb, RGB is color
        xsize, ysize = img.size
        self.label_10.setText('%d x %d'%(xsize,ysize))
        if chk_cht(path):           
           try:
               img_show = mpimg.imread(path)
           except UnicodeEncodeError:
               print "The fileName have problem. Do not use Chinese in fileName"
#               reload(sys)
#               sys.setdefaultencoding('utf-8')
#               img_show = mpimg.imread(path)
#               sys.setdefaultencoding('ascii')
        else:
           img_show = mpimg.imread(path)          
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):               
                return 'x=%d, y=%d'%(int(x)+1, int(y)+1) #z = self.im.get_array()[int(y), int(x)]
        filename = path.split('/')[len(path.split('/'))-1]                                             
        fig1, ax1 = plt.subplots()        
        plt.gcf().canvas.set_window_title(filename)
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.axis("off")        
        plt.xlim(0,xsize)
        plt.ylim(ysize,0)
        plt.ion()
        if img.mode[0] == 'I' or img.mode[0] == 'L' or img.mode[0] == 'F' :       
           im = ax1.imshow(img_show,interpolation='none',cmap='Greys_r')
        else:
           im = ax1.imshow(img_show,interpolation='none')
        ax1.format_coord = Formatter(im)
        plt.show()
        y0 = 0
        def onclick(event):
            if event.inaxes!=ax1.axes: return            
            onclick_chk(event.ydata+1)                                                      
        def onclick_chk(y1):
            global y0
            global box
            if y1 > y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y0))                                                     
              self.lineEdit_3.setText('%d'%(y1))
            if y1 < y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y1))                                     
              self.lineEdit_3.setText('%d'%(y0))
            if y1 == y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y1))                                     
              self.lineEdit_3.setText('%d'%(y1))              
            y0 = y1
        def close_figure(event):
            plt.close(fig1)
            img.close()
        cid_open = fig1.canvas.mpl_connect('button_press_event',onclick)
        fig1.canvas.mpl_connect('close_event', close_figure)          
    def reopenimg(self,event):
        global y0
        if path == "": return
        img = Image.open(path)
        xsize, ysize = img.size
        img_show = mpimg.imread(path)
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):               
                return 'x=%d, y=%d'%(int(x)+1, int(y)+1) #z = self.im.get_array()[int(y), int(x)]
        filename = path.split('/')[len(path.split('/'))-1]                                             
        fig11, ax11 = plt.subplots()
        plt.gcf().canvas.set_window_title(filename)
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.axis("off")        
        plt.xlim(0,xsize)
        plt.ylim(ysize,0)
        plt.ion()
        if img.mode[0] == 'I' or img.mode[0] == 'L' or img.mode[0] == 'F' :       
           im = ax11.imshow(img_show,interpolation='none',cmap='Greys_r')
        else:
           im = ax11.imshow(img_show,interpolation='none')
        ax11.format_coord = Formatter(im)
        plt.show()
        y0 = 0
        def onclick(event):
            if event.inaxes!=ax11.axes: return            
            onclick_chk(event.ydata+1)                                            
        def onclick_chk(y1):
            global y0
            global box
            if y1 > y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y0))                                                     
              self.lineEdit_3.setText('%d'%(y1))
            if y1 < y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y1))                                     
              self.lineEdit_3.setText('%d'%(y0))
            if y1 == y0 and box[2]==0 :
              self.lineEdit_2.setText('%d'%(y1))                                     
              self.lineEdit_3.setText('%d'%(y1))              
            y0 = y1
        def close_figure(event):
            plt.close(fig11)
            img.close()
        cid_reopen = fig11.canvas.mpl_connect('button_press_event',onclick)
        fig11.canvas.mpl_connect('close_event', close_figure) 
##################################################
    def plot_region(self):
        global box
        if self.lineEdit_2.text() == "" : return  
        if box[2] == 0:  #unlock
           box[0] = int(self.lineEdit_2.text())-1 #[idx from 0 : to nth element]
           box[1] = int(self.lineEdit_3.text())
           box[2] = 1 #chk 
           self.pushButton_4.setText("Unlock")
           self.pushButton_4.setStyleSheet('color: red')
           self.lineEdit_2.setReadOnly(True)
           self.lineEdit_3.setReadOnly(True)
           print 'Region = %d %d'%(box[0]+1,box[1])         
        else :  #lock
            box[2] = 0 
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_3.setReadOnly(False)
            self.pushButton_4.setText("Lock")
            self.pushButton_4.setStyleSheet('color: black')
########################################################################        
    def plotProfile(self):
        from scipy.optimize import leastsq
        global intensity_box,result_max_x,result_max_y
        result_max_x = np.array([],dtype=float)
        result_max_y = np.array([],dtype=float) 
        if path == "" or box[1] == 0: return
        plot_x, intensity_box = intensitybox(path,box)                                                                                         
        def onkey(event):    
            if event.inaxes!=ax2.axes: return            
            onkey_chk(event.key,event.xdata,event.ydata)                                   
        def onkey_chk(key,x,y):   
            global xlist,ylist,line
            global result_peak,result_max_x,result_max_y
            if key == u'a': 
               xlist.append(x)#start from 1, idx need -1
               ylist.append(y)
               ax2.plot(x,y,'ro')       
               if len(xlist)%2 == 0: #even
                  linex = [x,xlist[len(xlist)-2]] 
                  liney = [y,ylist[len(xlist)-2]] 
                  line = ax2.plot(linex,liney,'r-')                            
                  intensity_box1 = intensity_box[int(min(linex))-1:int(max(linex))]
                  fit_x =  plot_x[int(min(linex))-1:int(max(linex))]                           
                  mean = np.mean(fit_x)
                  std = np.std(fit_x)
                  amp = np.max(intensity_box1)
                  pini = [5., amp, mean, std]
                  res, flag = leastsq(residulas, pini, args=(fit_x, intensity_box1))          
                  fit_xx = np.linspace(int(min(linex)),int(max(linex)),200) #let it more smooth                        
                  fit_result = gauss(fit_xx, res)
                  if fit_result[10]-np.mean(fit_result)<0: #test peak up or down ,<0 is up 
                     fit_max_y = np.max(fit_result)
                  else:
                     fit_max_y = np.min(fit_result)              
                  fit_max_x = np.mean(fit_xx[np.where(fit_result == fit_max_y)])#                  
                  result_max_x = np.append(result_max_x,fit_max_x)   
                  result_max_y = np.append(result_max_y,fit_max_y)                  
                  line = ax2.plot(fit_max_x,fit_max_y,'bo')
                  line = ax2.plot(fit_xx,fit_result,'g-')
                  line = ax2.text(fit_max_x+0.5,fit_max_y+1,str(result_max_x.size),color='blue',fontsize=15)           
                  fit_max_x_text = '%.1f'%(fit_max_x)
                  item = QtGui.QTableWidgetItem(fit_max_x_text)        
                  self.tableWidget.setItem(result_max_x.size-1, 0,item)
            if key == u'c':
               xlist = []
               ylist = []
               result_max_x = np.array([],dtype=float)
               result_max_y = np.array([],dtype=float)
               last_step = len(ax2.lines)
               last_step2 = len(ax2.texts)
               del ax2.lines[1:last_step]
               del ax2.texts[0:last_step2]
               line = ax2.plot([],[],'r-')
               for i in range(30):
                  item_c = QtGui.QTableWidgetItem('')                              
                  self.tableWidget.setItem(i, 0,item_c)                     
            if key == u'd':
               if result_max_x.size > 0:     
                  xlist = []
                  ylist = []
                  if result_max_x.size == 1:
                     result_max_x = np.array([],dtype=float)
                     result_max_y = np.array([],dtype=float)
                  else:
                     result_max_x = result_max_x[0:result_max_x.size-1]
                     result_max_y = result_max_y[0:result_max_y.size-1]                  
                  last_step = len(ax2.lines)
                  last_step2 = len(ax2.texts)
                  del ax2.lines[last_step-6:last_step]
                  del ax2.texts[last_step2-1:last_step2]
                  line = ax2.plot([],[],'r-')
                  item_d = QtGui.QTableWidgetItem('')                              
                  self.tableWidget.setItem(result_max_x.size, 0,item_d)                   
                                                                    
        def gauss(x, p):
            noi = p[0]
            aa = p[1]
            mu = p[2]
            sigma =p[3] 
            fun = aa*np.exp(-(x-mu)**2/(2.*sigma**2))+noi
            return fun            
        def residulas(p, fit_x, intensity_box1):
            return (gauss(fit_x, p)-intensity_box1)**2                
               
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):
                return 'x=%d, y=%.2f'%(int(x)+1, y)                 
        fig2, ax2 = plt.subplots()
        plt.gcf().canvas.set_window_title("Profile(Y=%d to %d)"%(int(box[0])+1,int(box[1])))          
        plt.xlim(0,plot_x.size)
        plt.xlabel('x (pixel)')
        plt.ylabel('intensity (counts)')
        plt.title('Use keyboard key "a" to add the x value to the table')
        des = 'Press key "a" on both sides of the peak.\nPress key "d" to delete current selection.\nPress key "c" to clear all selection.'
        plt.tight_layout()
        plt.minorticks_on()
        plt.grid(True)
        plt.ion()
        im2 = ax2.plot(plot_x,intensity_box,'k-',label=des)
        plt.legend(loc='best')    
        ax2.format_coord = Formatter(im2)
        line = ax2.plot([],[],'r-')  # empty line        
        plt.show()       
        cid_pro = fig2.canvas.mpl_connect('key_press_event', onkey)
########################################################################
    def load_stdlight(self,light):
        if light == "Light source":
           for item_idx in range(30):                            
               item1 = QtGui.QTableWidgetItem('')                              
               self.tableWidget.setItem(item_idx, 0,item1) #set blank memory site
               item2 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(item_idx, 1,item2) #set blank memory site
               item3 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(item_idx, 2,item3)            
        if light == "Neon Lamp":
           for i in range(30):
               item2 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(i, 1,item2)
           if os.path.isfile('REF//Neon_ref_profile_value.csv'):           
              ne_data = np.genfromtxt('REF//Neon_ref_profile_value.csv',dtype=float,delimiter=',')        
              ne_w_ref = ne_data[:,0]
              ne_i_ref = ne_data[:,1]
           else:
              ne_w_ref = np.array([380,730],dtype=int)
              ne_i_ref = np.array([0.0001,0.0001],dtype=float)                  
           fig_neon, ax_neon = plt.subplots()
           plt.gcf().canvas.set_window_title('Neon_Lamp')             
           plt.xlim(ne_w_ref.min(),ne_w_ref.max())
           plt.ylim(0,255)          
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('intensity (counts)')
           plt.title('Click on the red line to add the wavelength to the table')
           plt.minorticks_on()
           plt.tight_layout()
           plt.ion()           
           plt.plot(ne_w_ref,ne_i_ref,'k-')                           
           for ndata in neon_data:
               plt.axvline(x=ndata,ymin=0,ymax=1,linewidth=1,color='r',picker=4)
               plt.text(ndata+0.25,240,str(ndata),rotation=90,fontsize=11,color='b')               
           plt.show()
           def onpick_ne(event):                           
               this_obj = event.artist   #if sinstance(event.artist, Line2D):
               xdata = this_obj.get_xdata()
               ind = event.ind
               points, = np.take(xdata, ind)
               onpick_item_ne(points)
           def onpick_item_ne(line):
               item_ne = QtGui.QTableWidgetItem(str(line))                       
               for n in range(30):               
                   item = self.tableWidget.item(n, 1)#w   
                   item_txt = item.text()
                   if item_txt == '':
                      self.tableWidget.setItem(n, 1,item_ne)   
                      break  
           cid_neon = fig_neon.canvas.mpl_connect('pick_event', onpick_ne)                              
        if light == "Sun":
           for i in range(30):
               item2 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(i, 1,item2) 
           if os.path.isfile('REF//Sun_ref_profile_value.csv'):           
              sun_datas = np.genfromtxt('REF//Sun_ref_profile_value.csv',dtype=float,delimiter=',')        
              sun_w_ref = sun_datas[:,0]
              sun_i_ref = sun_datas[:,1]
           else:
              sun_w_ref = np.array([380,730],dtype=int)
              sun_i_ref = np.array([0.0001,0.0001],dtype=float)                 
           fig_sun, ax_sun = plt.subplots()
           plt.gcf().canvas.set_window_title('Sun')             
           plt.xlim(sun_w_ref.min(),sun_w_ref.max())
           plt.ylim(0,210)
           plt.title('Click on the red line to add the wavelength to the table')
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('intensity (counts)')
           plt.minorticks_on()
           plt.tight_layout()
           plt.ion()                       
           plt.plot(sun_w_ref,sun_i_ref,'k-')
           n = 1
           s_data_plot = np.array([r'$H_\alpha (C)  656.281$',r'$Na (D1)  589.592$',
                                   r'$Na (D2)  588.995$',r'$Fe (E2)  527.039$',r'$Mg (b1)  518.362$',r'$Mg (b2)  517.270$',
                                   r'$Mg (b4)  516.733$',r'$Fe (c)  495.761$',r'$H_\beta (F)  486.134$',r'$Fe (d)  466.814$',
                                   r'$Fe (e)  438.355$',r'$H_\gamma (f)  434.047$',r'$Fe/Ca (G)  430.8$',r'$Ca (g)  422.673$',
                                   r'$H_\delta (h)  410.175$',r'$Ca+ (H)  396.847$',r'$Ca+ (K)  393.368$'],dtype=str)           
           for sdata in sun_data:
               plt.axvline(x=sdata,ymin=0,ymax=1,linewidth=1,color='r',picker=4)                       
               plt.text(sdata+0.2,192,s_data_plot[n-1],rotation=90,fontsize=12,color='b')
               n += 1                                          
           plt.show()           
           def onpick(event):                           
               this_obj = event.artist   #if sinstance(event.artist, Line2D):
               xdata = this_obj.get_xdata()
               ind = event.ind
               points, = np.take(xdata, ind)
               onpick_item(points)
           def onpick_item(line):
               item_sun = QtGui.QTableWidgetItem(str(line))        
               for n in range(30):               
                   item = self.tableWidget.item(n, 1)
                   item_txt = item.text()
                   if item_txt == '':
                      self.tableWidget.setItem(n, 1,item_sun)   
                      break  
           cid_sun = fig_sun.canvas.mpl_connect('pick_event', onpick)              
        if light == "Fluorescent(Hg) Lamp":
           for i in range(30):
               item2 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(i, 1,item2)
           if os.path.isfile('REF//Hg_ref_profile_value.csv'):           
              hg_datas = np.genfromtxt('REF//Hg_ref_profile_value.csv',dtype=float,delimiter=',')        
              hg_w_ref = hg_datas[:,0]
              hg_i_ref = hg_datas[:,1]
           else:
              hg_w_ref = np.array([380,730],dtype=int)
              hg_i_ref = np.array([0.0001,0.0001],dtype=float)                
           fig_hg, ax_hg = plt.subplots()
           plt.gcf().canvas.set_window_title('Fluorescent(Hg) Lamp')             
           plt.xlim(hg_w_ref.min(),hg_w_ref.max())
           plt.ylim(0,255)          
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('intensity (counts)')
           plt.title('Click on the red line to add the wavelength to the table')
           plt.minorticks_on()
           plt.tight_layout()
           plt.ion()           
           plt.plot(hg_w_ref,hg_i_ref,'k-')
           for ndata in hg_data:
               plt.axvline(x=ndata,ymin=0,ymax=1,linewidth=1,color='r',picker=4)
               plt.text(ndata+0.25,240,str(ndata),rotation=90,fontsize=11,color='b')               
           plt.show()
           def onpick_hg(event):                           
               this_obj = event.artist   #if sinstance(event.artist, Line2D):
               xdata = this_obj.get_xdata()
               ind = event.ind
               points, = np.take(xdata, ind)
               onpick_item_hg(points)
           def onpick_item_hg(line):
               item_hg = QtGui.QTableWidgetItem(str(line))
               for n in range(30):               
                   item = self.tableWidget.item(n, 1)#w   
                   item_txt = item.text()
                   if item_txt == '':
                      self.tableWidget.setItem(n, 1,item_hg)   
                      break                           
           cid_hg = fig_hg.canvas.mpl_connect('pick_event', onpick_hg)                    
        if light == "Custom":
           for item_idx in range(30):                            
               item1 = QtGui.QTableWidgetItem('')                              
               self.tableWidget.setItem(item_idx, 0,item1) #set blank memory site
               item2 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(item_idx, 1,item2) #set blank memory site
               item3 = QtGui.QTableWidgetItem('')
               self.tableWidget.setItem(item_idx, 2,item3)              
########################################################################          
    def load_poly_cali(self,poly):
        global poly_order
        if poly == "Polynomial calibration": poly_order = 1         
        if poly == "1st order (simple linear)": poly_order = 1            
        if poly == "2ed order ": poly_order = 2             
        if poly == "3rd order ": poly_order = 3            
        if poly == "4th order ": poly_order = 4  
########################################################################                  
    def calibrate(self):
        global x_p
        global y_nm
        global coef
        global sigma_p,rs,rms
        global cali_formula
        pm = '+/-'#pm = u'±'
        s4 = u'\u2074' #4 up sscripts
        s3 = u'\u00B3' #3 up sscripts
        s2 = u'\u00B2' #2 up sscripts                
        item_chkx = self.tableWidget.item(2, 0)#x                
        item_chky = self.tableWidget.item(2, 1)#w
        if (item_chkx.text() == '') | (item_chky.text() == ''):
           print 'Please input at least 3 of x and wavelength values in the table above.' 
           return 
        savepath = 'Save//Wavelength_calibration'
        if not os.path.exists(savepath): os.makedirs(savepath)
        if path == "": 
            img_name = 'NoIMG'   
        else:               
            img_name = path.split(r'/')[len(path.split(r'/'))-1]#number-1        
        filename = 'Save//Wavelength_calibration//%s_wavelength_calibration_data.csv'%(img_name)                     
        #Check calibration result file exist or not
        if os.path.isfile(filename) and img_name != 'NoIMG':     
           info = "Wavelength calibration of image %s has been done before.\n\
                   Do you want to overwrite existing result?\n\
                   Yes   : Overwrite the existing file.\n\
                   No    : Save as new file.\n\
                   Ignore: Do the calibration and don't save anything."%(img_name)
           result = QtGui.QMessageBox.question(self.scrollArea,
                    "Overwrite or not...",info,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Ignore, QtGui.QMessageBox.Yes)   
           if result == QtGui.QMessageBox.Yes:
              save_action = True
           elif result == QtGui.QMessageBox.Ignore:
              save_action = False 
           else :
              save_action = True
              path_save, _ = QtGui.QFileDialog.getSaveFileName(None, "Calibration data Save as...",os.getcwd(), "text (*.csv)") #
              if path_save == "": return
              filename = path_save
        else:
            save_action = True
        #read table
        input_x = np.array([],dtype=str) 
        input_y = np.array([],dtype=str) 
        for i in range(30):
          item_x = self.tableWidget.item(i, 0)#x
          item_w = self.tableWidget.item(i, 1)#w          
          input_x = np.append(input_x,item_x.text())
          input_y = np.append(input_y,item_w.text())           
        input_xp = input_x[np.where(input_x != '')]
        input_yw = input_y[np.where(input_y != '')]          
        x_p = np.asarray(input_xp,dtype=float) 
        y_nm = np.asarray(input_yw,dtype=float)
        #poly regress
        from scipy.optimize import curve_fit
        def fun(x,a,b):
           return a*x+b
        def fun2(x,a,b,c):
           return a*x**2+b*x+c  
        def fun3(x,a,b,c,d):
           return a*x**3+b*x**2+c*x+d
        def fun4(x,a,b,c,d,e):
           return a*x**4+b*x**3+c*x**2+d*x+e
        if poly_order == 1:  
           coef, cov = curve_fit(fun, x_p, y_nm)
           sigma_p = np.sqrt(np.diag(cov))
           text = 'Y(nm) = %.7fx+%.4f'
           cali_formula = text%(coef[0],coef[1])  
           self.results.setText(cali_formula)                              
           text_plot = cali_formula
        elif poly_order == 2:
             if x_p.size < 4:
                print 'Please input at least 4 of x and wavelength values in the table above.' 
                return                         
             coef, cov = curve_fit(fun2, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.7fx+%.4f'             
             cali_formula = text%(coef[0],s2,coef[1],coef[2])
             self.results.setText(cali_formula)
             text_p = 'Y(nm) = %.3Ex$^2$+%.7fx+%.4f'
             text_plot = text_p%(coef[0],coef[1],coef[2])
#             error_nm = ((x_p*sigma_p[0])**2+(sigma_p[1])**2)**0.5             
#             print 'error=',error_nm            
        elif poly_order == 3:
             if x_p.size < 5:
                print 'Please input at least 5 of x and wavelength values in the table above.' 
                return  
             coef, cov = curve_fit(fun3, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.3Ex%s+%.7fx+%.4f'
             cali_formula = text%(coef[0],s3,coef[1],s2,coef[2],coef[3])
             self.results.setText(cali_formula)                      
             text_p = 'Y(nm) = %.3Ex$^3$+%.3Ex$^2$+%.7fx+%.4f'
             text_plot = text_p%(coef[0],coef[1],coef[2],coef[3])
        elif poly_order == 4:
             if x_p.size < 6:
                print 'Please input at least 6 of x and wavelength values in the table above.' 
                return              
             coef, cov = curve_fit(fun4, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.3Ex%s+%.3Ex%s+%.7fx+%.4f'
             cali_formula = text%(coef[0],s4,coef[1],s3,coef[2],s2,coef[3],coef[4])
             self.results.setText(cali_formula)              
             text_p = 'Y(nm) = %.3Ex$^4$+%.3Ex$^3$+%.3Ex$^2$+%.7fx+%.4f'
             text_plot = text_p%(coef[0],coef[1],coef[2],coef[3],coef[4])
        f_fit = np.polyval(coef,x_p)                
        res = y_nm-f_fit
        sse = np.sum((res)**2)#
        ssr = np.sum((f_fit-np.mean(y_nm))**2)#
        ssy = np.sum((y_nm)**2)-(np.sum(y_nm)**2/y_nm.size)#
        rs = ssr/ssy#
        rms = (sse/(x_p.size-poly_order-1))**0.5 
        sigma_p = np.sqrt(np.diag(cov))          
#        sigma_t = np.sqrt(sse/(x_p.size-poly_order-1))#     
#        ssx = np.sum((x_p)**2)-(np.sum(x_p)**2/x_p.size)#
#        sigma_a = sigma_t/(ssx**0.5)
#        sigma_b = sigma_t*((1./x_p.size)+(np.mean(x_p)**2/ssx))**0.5#
        for res_idx in range(res.size):        
            item_res = QtGui.QTableWidgetItem('%.3f'%(res[res_idx]))        
            self.tableWidget.setItem(res_idx, 2, item_res)          
        for para_idx in range(coef.size):
            if coef.size == 2:
               if para_idx+1 == 1:
                  para_text = 'coef %d = %.7f %s %.7f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                   
               else:    
                  para_text = 'coef %d = %.4f %s %.4f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])
            else: # 3p=1 [2 3] ; 4p = 1 2 [3 4] ; 5p = 1 2 3 [4 5] 
               if coef.size-(para_idx+1) >= 2:
                  para_text = 'coef %d = %.3E %s %.3E'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])          
               else:
                  if coef.size-(para_idx+1) == 1:
                     para_text = 'coef %d = %.7f %s %.7f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                   
                  else:    
                     para_text = 'coef %d = %.4f %s %.4f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                                     
            self.results.append(para_text)
        self.results.append('R-squared = %.6f'%(rs))
        self.results.append('RMS = %.4f'%(rms))
        fig_cali, ax_cali = plt.subplots()
        plt.gcf().canvas.set_window_title('Wavelength calibration curve')             
        plt.xlabel('Pixel (x)')
        plt.ylabel('Wavelength (nm)')
        plt.minorticks_on()
        plt.tight_layout()            
        plt.plot(x_p,y_nm,'ko')
        plt.plot(x_p,f_fit,'r-',label=r'%s  R$^2$=%.6f'%(text_plot,rs))
        plt.legend(loc='best')         
        plt.show()
        #save result
        if save_action:                       
           file = open(filename , "w")
           file.write('# Wavelength calibration data\n')
           file.write('# box_y1  box_y2  flag \n')
           file.write('  %d  %d  %d\n'%(box[0],box[1],box[2]))                
           file.write('# X_pixel  Wavelength(nm)  Residual \n') 
           for i in range(x_p.size):           
               line = '  %s  %s  %.3f\n'%(str(x_p[i]),str(y_nm[i]),res[i])#2
               file.write(line)
           file.write('# Results (Polynomial Regression, Order = %d) : \n'%(poly_order))
           file.write('# 1. Coefficients : \n')        
           for i in range(coef.size):
               file.write('  %.8E'%(coef[i]))
           file.write('\n')
           file.write('# 2. Standard error of coefficient : \n')                
           for i in range(sigma_p.size):
               file.write('  %.8E'%(sigma_p[i]))        
           file.write('\n')
           file.write('# 3. R-squared : \n')                
           file.write('  %.6f\n'%(rs))        
           file.write('# 4. RMS : \n')                
           file.write('  %.6f\n'%(rms))          
           file.close()
           print r'Saved in folder: Save\Wavelength_calibration'        
########################################################################             
    def Load_calibration_data(self):
        global box
        global x_p
        global y_nm
        global coef
        global poly_order
        global sigma_p,rs,rms
        pm = '+/-' 
        s4 = u'\u2074' #4 up sscripts
        s3 = u'\u00B3' #3 up sscripts
        s2 = u'\u00B2' #2 up sscripts 
        x_p = np.array([],dtype=float)
        y_nm = np.array([],dtype=float)
        res = np.array([],dtype=float) 
        path_cali_data, _ = QtGui.QFileDialog.getOpenFileName(None, "Open csv file...",os.getcwd(), "text file (*.csv)")
        if path_cali_data == "": return
        file = open(path_cali_data , "r")
        data = file.readlines()
        file.close()
        if len(data) > 45 : 
           print 'Open wrong file!!' 
           return 
        for item_idx in range(30):  #set blank memory site                          
            item1 = QtGui.QTableWidgetItem('')                              
            self.tableWidget.setItem(item_idx, 0,item1) 
            item2 = QtGui.QTableWidgetItem('')
            self.tableWidget.setItem(item_idx, 1,item2) 
            item3 = QtGui.QTableWidgetItem('')
            self.tableWidget.setItem(item_idx, 2,item3)         
        box = np.asarray(data[2].split('  ')[1:4],dtype=int)#3rd line;first element is ''
        for i in range(len(data)-13): #size of x_p
            line_list = data[4+i].split('  ')#5th line
            x_p = np.append(x_p,float(line_list[1]))
            y_nm = np.append(y_nm,float(line_list[2]))
            res = np.append(res,float(line_list[3]))
        coef = np.asarray(data[len(data)-7].split('  ')[1::],dtype=float)
        poly_order = coef.size-1       
        for idx in range(x_p.size):
            item_x = QtGui.QTableWidgetItem(str(x_p[idx]))
            item_w = QtGui.QTableWidgetItem(str(y_nm[idx]))            
            item_r = QtGui.QTableWidgetItem(str(res[idx]))                    
            self.tableWidget.setItem(idx, 0,item_x)                       
            self.tableWidget.setItem(idx, 1,item_w)                       
            self.tableWidget.setItem(idx, 2,item_r)  
        self.lineEdit_2.setText('%d'%(int(box[0])+1))   
        self.lineEdit_3.setText('%d'%(int(box[1])))                                   
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)                                
        self.pushButton_4.setText("Unlock")
        self.pushButton_4.setStyleSheet('color: red')
        #######################################################################
        from scipy.optimize import curve_fit
        def fun(x,a,b):
           return a*x+b
        def fun2(x,a,b,c):
           return a*x**2+b*x+c  
        def fun3(x,a,b,c,d):
           return a*x**3+b*x**2+c*x+d
        def fun4(x,a,b,c,d,e):
           return a*x**4+b*x**3+c*x**2+d*x+e
        if poly_order == 1:  
           coef, cov = curve_fit(fun, x_p, y_nm)
           sigma_p = np.sqrt(np.diag(cov))
           text = 'Y(nm) = %.7fx+%.4f'
           cali_formula = text%(coef[0],coef[1])  
           self.results.setText(cali_formula)                              
        elif poly_order == 2:                        
             coef, cov = curve_fit(fun2, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.7fx+%.4f'             
             cali_formula = text%(coef[0],s2,coef[1],coef[2])
             self.results.setText(cali_formula)             
        elif poly_order == 3:
             coef, cov = curve_fit(fun3, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.3Ex%s+%.7fx+%.4f'
             cali_formula = text%(coef[0],s3,coef[1],s2,coef[2],coef[3])
             self.results.setText(cali_formula)                      
        elif poly_order == 4:
             coef, cov = curve_fit(fun4, x_p, y_nm)
             sigma_p = np.sqrt(np.diag(cov))
             text = 'Y(nm) = %.3Ex%s+%.3Ex%s+%.3Ex%s+%.7fx+%.4f'
             cali_formula = text%(coef[0],s4,coef[1],s3,coef[2],s2,coef[3],coef[4])
             self.results.setText(cali_formula)              
        f_fit = np.polyval(coef,x_p)                
        res = y_nm-f_fit
        sse = np.sum((res)**2)#
        ssr = np.sum((f_fit-np.mean(y_nm))**2)#
        ssy = np.sum((y_nm)**2)-(np.sum(y_nm)**2/y_nm.size)#
        rs = ssr/ssy#
        rms = (sse/(x_p.size-poly_order-1))**0.5 
        sigma_p = np.sqrt(np.diag(cov))                  
        for para_idx in range(coef.size):
            if coef.size == 2:
               if para_idx+1 == 1:
                  para_text = 'coef %d = %.7f %s %.7f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                   
               else:    
                  para_text = 'coef %d = %.4f %s %.4f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])
            else:
               if coef.size-(para_idx+1) >= 2:
                  para_text = 'coef %d = %.3E %s %.3E'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])          
               else:
                  if coef.size-(para_idx+1) == 1:
                     para_text = 'coef %d = %.7f %s %.7f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                   
                  else:    
                     para_text = 'coef %d = %.4f %s %.4f'%(para_idx+1,coef[para_idx],pm,sigma_p[para_idx])                                     
            self.results.append(para_text)
        self.results.append('R-squared = %.6f'%(rs))
        self.results.append('RMS = %.4f'%(rms))    
########################################################################
    def plot_cali_profile(self):
        global intensity_box
        if path == "":
           print 'Please load spectral image.' 
           return
        if coef.size < 2:
           print 'Please do the wavelength-calibration or load the calibration data.' 
           return
        img_name = path.split('/')[len(path.split('/'))-1]           
        savepath = 'Save//Profile_value' 
        if not os.path.exists(savepath): os.makedirs(savepath)          
        filename = 'Save//Profile_value//%s_profile_value.csv'%(img_name)
        #Check profile value file exist or not
        if os.path.isfile(filename):     
           info = "The profile value of image %s has been saved before.\n\
                   Do you want to overwrite existing profile?\n\
                   Yes   : Overwrite the existing file.\n\
                   No    : Save as new file.\n\
                   Ignore: Just show profile and don't save anything."%(img_name)
           result = QtGui.QMessageBox.question(self.scrollArea,
                    "Overwrite or not...",info,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Ignore, QtGui.QMessageBox.Yes)   
           if result == QtGui.QMessageBox.Yes:
              save_action = True
           elif result == QtGui.QMessageBox.Ignore:
              save_action = False 
           else :
              save_action = True
              path_save, _ = QtGui.QFileDialog.getSaveFileName(None, "Profile value Save as...",os.getcwd(), "text (*.csv)") #
              if path_save == "": return
              filename = path_save
        else:
            save_action = True
        plot_x, intensity_box = intensitybox(path,box)        
        x_wave = xwave(plot_x) #coef in global
        fig_cali_p, ax_cali_p = plt.subplots()
        plt.gcf().canvas.set_window_title("%s Profile in wavelength(Y=%d to %d)"%(img_name,int(box[0])+1,int(box[1])))
        plt.xlim(x_wave.min(),x_wave.max())
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity (counts)')
        plt.minorticks_on()
        plt.grid(True)
        plt.tight_layout()
        plt.plot(x_wave,intensity_box,'r-')          
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range
        plt.show()                                    
        if save_action: #save value or not
           save_data = np.concatenate((x_wave.reshape(x_wave.size,1), intensity_box.reshape(x_wave.size,1)), axis=1) #兩組data結合成(x,y)
           np.savetxt(filename,save_data,delimiter=',',fmt='%.4f')
           print r'Saved to folder: Save\Profile_value'        
        img = Image.open(path)
        xsize, ysize = img.size
        pix_area = img.crop((0,box[0],xsize,box[1])) 
        f_spimg, ax_spimg = plt.subplots()        
        ax_spimg = plt.subplot2grid((4,1), (0, 0),rowspan=3)
        plt.gcf().canvas.set_window_title("%s Profile in wavelength with image(Y=%d to %d)"%(img_name,int(box[0])+1,int(box[1])))        
        ax_spimg.set_xlabel('Wavelength (nm)')
        ax_spimg.set_ylabel('Intensity (counts)')
        plt.xlim(x_wave.min(),x_wave.max())
        plt.minorticks_on()       
        plt.plot(x_wave,intensity_box,'r-')
        plt.locator_params(axis='x',nbins=20) #set ticks range     
        plt.subplot2grid((4,1), (3, 0),rowspan=1,sharex=ax_spimg)  
        plt.axis("off")                     
        if img.mode[0] == 'I' or img.mode[0] == 'F' or img.mode[0] == 'L' :
           pix_area = pix_area.convert('F').resize((xsize,2),Image.BILINEAR)#zoom in (32-bit floating)                          
           pix = np.asarray([pix_area.getdata()],np.float64).reshape(2,xsize)              
           pix = pix[:,np.argsort(x_wave)]
           plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 65, 0),interpolation='bilinear',cmap='Greys_r')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                        
        else:              
           pix_area = pix_area.resize((xsize,2),Image.BILINEAR)#zoom in BILINEAR BICUBIC
           pix = np.asarray([pix_area.getdata()],dtype=np.uint8).reshape(2,xsize,3)            
           pix = pix[:,np.argsort(x_wave),:]
           plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 100, 0),interpolation='bilinear')# bilinear bicubic aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)             
        f_spimg.tight_layout()       
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.05)
        plt.show()          

        chk_psi = self.checkBox_11.isChecked() #image in profile shape
        if chk_psi == True: 
           fig_psi, ax_psi = plt.subplots()
           plt.gcf().canvas.set_window_title("%s in profile shape(Y=%d to %d)"%(img_name,int(box[0])+1,int(box[1])))        
           plt.xlabel('Wavelength (nm)')
           plt.ylabel('Intensity (counts)')                        
           plt.minorticks_on()
           high = np.asarray(intensity_box,dtype=int)           
           if img.mode[0] == 'I'or img.mode[0] == 'F' or img.mode[0] == 'L':
              pix_area = pix_area.convert('F').resize((xsize,255),Image.BILINEAR)#zoom in (32-bit floating)           
              pix = np.asarray([pix_area.getdata()],np.uint8).reshape(255,xsize)
              pix[pix < 0] = pix[pix < 0]+2**16
              if high.max() > 255: 
                 high = high/(65535/255) #change linear scale by 65535/255       
              for ii in range(xsize): #set to white for out of profile intensity region 
                  pix[high[ii]+1:255,ii] = [0]# need change linear scale by 65535/255                     
              pix = pix[:,np.argsort(x_wave)]
              plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 255, 0),interpolation='bilinear',cmap='Greys_r')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                                                             
           else:
              pix_area = pix_area.resize((xsize,255),Image.BILINEAR)#zoom in (32-bit floating)           
              pix = np.asarray([pix_area.getdata()],dtype=np.uint8).reshape(255,xsize,3)              
              for ii in range(xsize): #set to white for out of region 
                  pix[high[ii]+1:255,ii] = [254,254,254]# 
              pix = pix[:,np.argsort(x_wave),:]
              plt.imshow(pix,aspect='equal',extent=(x_wave.min(),x_wave.max(), 255, 0),interpolation='bilinear')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                                                                            
           plt.gca().invert_yaxis()
           plt.tight_layout()
           plt.show()        
########################################################################
########################################################################
    def Load_profile_value_plot_nw(self):
        global profile_loc
        profile_loc = np.array([],dtype=str)
        self.scrollArea_lpvp = QtGui.QScrollArea()
        self.scrollArea_lpvp.resize(490, 330)      
        self.scrollArea_lpvp.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)#AlwaysOn        
        self.scrollArea_lpvp.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea_lpvp.setWindowTitle('Load Profile(s) and Plot')
        self.scrollArea_lpvp.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)                
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(12)                
        self.nw_lpvp = QtGui.QWidget()
        self.nw_lpvp.resize(480, 320)
        self.scrollArea_lpvp.setWidget(self.nw_lpvp)       
        self.pushButton_adp = QtGui.QPushButton(self.nw_lpvp) #load Profile
        self.pushButton_adp.setGeometry(QtCore.QRect(18, 18, 100, 28))        
        self.pushButton_adp.setText("Add Profile")             
        self.pushButton_adp.setFont(font)
        self.pushButton_rmp = QtGui.QPushButton(self.nw_lpvp) 
        self.pushButton_rmp.setGeometry(QtCore.QRect(135, 18, 100, 28))        
        self.pushButton_rmp.setText("Remove")    
        self.pushButton_rmp.setFont(font)
        self.pushButton_plots = QtGui.QPushButton(self.nw_lpvp) 
        self.pushButton_plots.setGeometry(QtCore.QRect(363, 18, 100, 28))        
        self.pushButton_plots.setText("Plot")    
        self.pushButton_plots.setFont(font)                
        self.listWidget_lpvp = QtGui.QListWidget(self.nw_lpvp)
        self.listWidget_lpvp.setGeometry(QtCore.QRect(18, 60, 445, 240))
        self.listWidget_lpvp.setFont(font) 
        self.pushButton_adp.clicked.connect(self.lpvp_adp)
        self.pushButton_rmp.clicked.connect(self.lpvp_rmp)
        self.pushButton_plots.clicked.connect(self.lpvp_plots)
        self.scrollArea_lpvp.show()                     
    def lpvp_adp(self): 
        global profile_loc
        path_profile, _ =QtGui.QFileDialog.getOpenFileName(None, "Open csv file...",os.getcwd(), "text file (*.csv)")
        if path_profile == "": return 
        try:
            data = np.genfromtxt(path_profile,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(path_profile,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')
        if data[0].size != 2:                    
           print 'Open wrong file!!' 
           return 
        filename = path_profile.split('/')[len(path_profile.split('/'))-1]        
        profile_loc = np.append(profile_loc,path_profile)
        item = QtGui.QListWidgetItem()
        item.setText(filename)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)#Unchecked
        self.listWidget_lpvp.addItem(item)
    def lpvp_rmp(self):        
        global profile_loc
        if profile_loc.size == 0:return
        item = self.listWidget_lpvp.item(profile_loc.size-1)
        self.listWidget_lpvp.removeItemWidget(item)
        self.listWidget_lpvp.takeItem(profile_loc.size-1)        
        profile_loc = profile_loc[0:profile_loc.size-1]       
    def lpvp_plots(self): 
        if profile_loc.size == 0: return 
        plot_idx = []
        for idx in range(profile_loc.size):
            item = self.listWidget_lpvp.item(idx)            
            if item.checkState() == QtCore.Qt.Checked : plot_idx.append(idx)
        if len(plot_idx) == 0: return        
        fig_pv, ax_pv = plt.subplots()
        plt.gcf().canvas.set_window_title('Profiles Plot')             
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')
        plt.minorticks_on()
        plt.grid(True)        
        plt.tight_layout() 
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
        for idx in plot_idx:         
            loc = profile_loc[idx]
            try:
               data = np.genfromtxt(loc,dtype=float,delimiter=',') 
            except UnicodeDecodeError:
               reload(sys)
               sys.setdefaultencoding('big5')
               data = np.genfromtxt(loc,dtype=float,delimiter=',') 
               sys.setdefaultencoding('utf-8')
            filename = loc.split('/')[len(loc.split('/'))-1]
            plt.plot(data[:,0],data[:,1],label=filename)
        plt.legend(loc='best')
        plt.show()          
########################################################################
########################################################################
    def continuum_nw(self):
        global profile_path #stored profile path
        profile_path = ""
        global cnabem_state #stored chk_state
        cnabem_state = ''
        global method
        method = ''        
        global xlist,ylist
        xlist = []
        ylist = []
        global z #continuum normalization result         
        z = np.array([],dtype=float) 
        self.nw_cn = QtGui.QWidget()
        self.nw_cn.resize(575, 380)
        self.nw_cn.setWindowTitle('Continuum normalization')
#        self.nw_cn.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)                
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_cnlp = QtGui.QPushButton(self.nw_cn) #load Profile
        self.pushButton_cnlp.setGeometry(QtCore.QRect(8, 13, 110, 27))        
        self.pushButton_cnlp.setText("Load Profile") 
        font.setBold(True)        
        self.pushButton_cnlp.setFont(font)
        font.setBold(False)        
        self.label_cnpn = QtGui.QLabel(self.nw_cn) #profile name
        self.label_cnpn.setGeometry(QtCore.QRect(126, 16, 440, 25))
        self.label_cnpn.setTextFormat(QtCore.Qt.PlainText)#"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbaaaaba"
        font.setPointSize(11)
        self.label_cnpn.setFont(font)       
        self.checkBox_cnab = QtGui.QCheckBox(self.nw_cn)
        self.checkBox_cnab.setGeometry(QtCore.QRect(9, 43, 195, 25))
        self.checkBox_cnab.setText("Absorption spectrum")
        font.setPointSize(12)
        self.checkBox_cnab.setFont(font)        
        self.checkBox_cnem = QtGui.QCheckBox(self.nw_cn)
        self.checkBox_cnem.setGeometry(QtCore.QRect(204, 43, 180, 25))
        self.checkBox_cnem.setText("Emission spectrum")
        self.checkBox_cnem.setFont(font)
        
        self.label_cnrange = QtGui.QLabel(self.nw_cn)
        self.label_cnrange.setGeometry(QtCore.QRect(389, 43, 59, 25))
        self.label_cnrange.setText("Range :")
        self.label_cnrange.setFont(font)
        self.lineEdit_cnrange = QtGui.QLineEdit(self.nw_cn)# y1
        self.lineEdit_cnrange.setGeometry(QtCore.QRect(448, 45, 86, 22))
        self.lineEdit_cnrange.setFont(font)
        self.label_cnrangeu = QtGui.QLabel(self.nw_cn)
        self.label_cnrangeu.setGeometry(QtCore.QRect(543, 43, 22, 25))
        self.label_cnrangeu.setText("nm")
        self.label_cnrangeu.setFont(font)
         
        self.tabWidget_cn = QtGui.QTabWidget(self.nw_cn)  
        self.tabWidget_cn.setGeometry(QtCore.QRect(9, 77, 560, 190))
        self.tabWidget_cn.setMouseTracking(False)
        self.tabWidget_cn.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget_cn.setFont(font)           
        self.tabcn_1 = QtGui.QWidget()
        self.tabWidget_cn.addTab(self.tabcn_1, "Method A - AsLS Smoothing")            
        self.tabcn_2 = QtGui.QWidget()
        self.tabWidget_cn.addTab(self.tabcn_2, "Method B - Pseudocontinuum points Fitting")         
        self.label_cnd1 = QtGui.QLabel(self.tabcn_1)
        self.label_cnd1.setGeometry(QtCore.QRect(QtCore.QRect(5, 1, 552, 22)))        
        self.label_cnd1.setText("The higher S the more smoothness; the higher P the higher baseline. Generally, the S between ")
        self.label_cnd2 = QtGui.QLabel(self.tabcn_1)
        self.label_cnd2.setGeometry(QtCore.QRect(QtCore.QRect(5, 19, 552, 22)))        
        self.label_cnd2.setText("3 and 6 is a good choice both for emission and absroption spectrum, the P between 0.01 and ")
        self.label_cnd3 = QtGui.QLabel(self.tabcn_1)
        self.label_cnd3.setGeometry(QtCore.QRect(QtCore.QRect(5, 37, 552, 22)))        
        self.label_cnd3.setText("0.2 is suitable for emission spectrum but need to be greater than 0.9 for absorption spectrum.")               
        font.setPointSize(10)
        self.label_cnd1.setFont(font)
        self.label_cnd2.setFont(font)
        self.label_cnd3.setFont(font)
        self.label_cnsp1 = QtGui.QLabel(self.tabcn_1)
        self.label_cnsp1.setGeometry(QtCore.QRect(QtCore.QRect(165, 65, 117, 20)))                         
        self.label_cnsp1.setText("S (1~9) : ")
        font.setPointSize(12)
        self.label_cnsp1.setFont(font)         
        self.spbox_cn1 = QtGui.QSpinBox(self.tabcn_1)
        self.spbox_cn1.setGeometry(QtCore.QRect(QtCore.QRect(315, 65, 65, 24)))
        self.spbox_cn1.setSingleStep(1)
        self.spbox_cn1.setRange(1, 9)
        self.label_cnsp2 = QtGui.QLabel(self.tabcn_1)
        self.label_cnsp2.setGeometry(QtCore.QRect(QtCore.QRect(165, 95, 165, 20)))                         
        self.label_cnsp2.setText("P (0.01~0.99) : ")
        self.label_cnsp2.setFont(font)         
        self.spbox_cn2 = QtGui.QDoubleSpinBox(self.tabcn_1)
        self.spbox_cn2.setGeometry(QtCore.QRect(QtCore.QRect(315, 95, 65, 24)))          
        self.spbox_cn2.setSingleStep(0.01)
        self.spbox_cn2.setRange(0.01, 0.99)        
        self.pushButton_cngc = QtGui.QPushButton(self.tabcn_1) #generate comtinuum function
        self.pushButton_cngc.setGeometry(QtCore.QRect(130, 134, 300, 27))  
        self.pushButton_cngc.setText("Generate Continuum Function")   
        self.pushButton_cngc.setFont(font)
        self.checkBox_cnpi = QtGui.QCheckBox(self.nw_cn)#plot with image 
        self.checkBox_cnpi.setGeometry(QtCore.QRect(9, 275, 550, 27))
        self.checkBox_cnpi.setText("Plot with image")
        self.checkBox_cnpi.setFont(font)
#        if path == "":  self.checkBox_cnpi.setEnabled(False)          
        self.label_cnin = QtGui.QLabel(self.nw_cn) #image name
        self.label_cnin.setGeometry(QtCore.QRect(27, 294, 540, 24))
        self.label_cnin.setTextFormat(QtCore.Qt.PlainText)#"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbaaaaba"
        self.label_cnin.setText('(need to load corresponding image and select the image area from main screen)')
        font.setPointSize(11)
        self.label_cnin.setFont(font)                
        self.pushButton_cnplot = QtGui.QPushButton(self.nw_cn) #Plot Profile in Relative Intensity
        self.pushButton_cnplot.setGeometry(QtCore.QRect(16, 345, 288, 27))        
        self.pushButton_cnplot.setText("Plot normalized spectrum")
        font.setPointSize(12)
        font.setBold(True)        
        self.pushButton_cnplot.setFont(font)        
        self.pushButton_cnsave = QtGui.QPushButton(self.nw_cn) #save result
        self.pushButton_cnsave.setGeometry(QtCore.QRect(325, 345, 110, 27))        
        self.pushButton_cnsave.setText("Save Result")
        font.setBold(False)        
        self.pushButton_cnsave.setFont(font)        
        self.pushButton_cnload = QtGui.QPushButton(self.nw_cn) #load 
        self.pushButton_cnload.setGeometry(QtCore.QRect(448, 345, 110, 27))        
        self.pushButton_cnload.setText("Load result")
        self.pushButton_cnload.setFont(font) 
        ######################################      
        self.label_cndt2_1 = QtGui.QLabel(self.tabcn_2)
        self.label_cndt2_1.setGeometry(QtCore.QRect(QtCore.QRect(5, 1, 552, 22)))        
        self.label_cndt2_1.setText("Pick out continuum points along pseudocontinuum curve by your eyes in ~10 nm interval on")
        self.label_cndt2_2 = QtGui.QLabel(self.tabcn_2)
        self.label_cndt2_2.setGeometry(QtCore.QRect(QtCore.QRect(5, 19, 552, 22)))        
        self.label_cndt2_2.setText("the profile figure. Press 'a' to add point; 'd' to remove current point; 'c' to remove all points.")
        font.setPointSize(10)
        self.label_cndt2_1.setFont(font)
        self.label_cndt2_2.setFont(font)
        self.text_cnpickup = QtGui.QTextEdit(self.tabcn_2) 
        self.text_cnpickup.setGeometry(QtCore.QRect(190, 45, 190, 84))#(9, 20, 389, 286)
        self.text_cnpickup.setFont(font)
        self.text_cnpickup.setReadOnly(True)
        self.text_cnpickup.setText('X(nm)              Y(intensity)')#space 6
        self.pushButton_cngc2 = QtGui.QPushButton(self.tabcn_2) #generate comtinuum function
        self.pushButton_cngc2.setGeometry(QtCore.QRect(130, 134, 300, 27))  
        self.pushButton_cngc2.setText("Generate Continuum Function") 
        font.setPointSize(12)
        self.pushButton_cngc2.setFont(font)
        ######################################
        self.pushButton_cnlp.clicked.connect(self.cnlp_ldpf)#load profile
        self.checkBox_cnab.stateChanged.connect(self.cnab)        
        self.checkBox_cnem.stateChanged.connect(self.cnem)                
        self.pushButton_cngc.clicked.connect(self.cngc)#generate cn function       
        self.pushButton_cngc2.clicked.connect(self.cngc2)#generate cn function       
        self.checkBox_cnpi.stateChanged.connect(self.cnpi_ck) #plot with img
        self.pushButton_cnplot.clicked.connect(self.cnplot)#plot
        self.pushButton_cnsave.clicked.connect(self.cnsave)#save
        self.pushButton_cnload.clicked.connect(self.cnload)#load
        self.label_cnpn.mousePressEvent = self.reopenprofile#reopen_profile       
        self.nw_cn.show()                 
        self.spbox_cn1.setValue(5)
        self.spbox_cn2.setValue(0.01)
    def cnlp_ldpf(self): 
        global profile_path #stored profile path
        global xlist,ylist         
        path_profile, _ =QtGui.QFileDialog.getOpenFileName(None, "Open csv file...",os.getcwd(), "text file (*.csv)") #"TXT(*.txt);;AllFiles(*.*)"          
        if path_profile == "": return      
        profile_path = path_profile
        try:
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')
        if data[0].size != 2:                    
           print 'Open wrong file!!' 
           return
        nm_range1 = int(np.min(data[:,0]))
        nm_range2 = int(np.max(data[:,0])) 
        self.lineEdit_cnrange.setText('%d-%d'%(nm_range1, nm_range2))         
        filename = path_profile.split('/')[len(path_profile.split('/'))-1]                
        self.label_cnpn.setText(filename)        
        x_nm = data[:,0]#nm
        y_ii = data[:,1]#intensity                                                                                             
        def cnlp_onkey(event):    
            if event.inaxes!=ax_cnlp.axes: return            
            onkey_chk(event.key,event.xdata,event.ydata)                                   
        def onkey_chk(key,x,y):   
            global xlist,ylist
            if key == u'a':
               for n in xlist:
                   if n == x: return #chk same element                  
               xlist.append(x)
               ylist.append(y)
               ax_cnlp.plot(x,y,'bo')
               self.text_cnpickup.append('%.3f            %.3f'%(x,y)) 
               fig_cnlp.canvas.draw()
            if key == u'c':
               if len(xlist) > 0:
                  xlist = []
                  ylist = []
                  self.text_cnpickup.setText('X(nm)              Y(intensity)')
                  last_step = len(ax_cnlp.lines)
                  del ax_cnlp.lines[1:last_step]
                  fig_cnlp.canvas.draw()                    
            if key == u'd':
               if len(xlist) > 0:     
                  xlist = xlist[0:len(xlist)-1]
                  ylist = ylist[0:len(ylist)-1]                
                  last_step = len(ax_cnlp.lines)
                  del ax_cnlp.lines[last_step-1]
                  fig_cnlp.canvas.draw()
                  self.text_cnpickup.undo()                                                                                                             
        fig_cnlp, ax_cnlp = plt.subplots()
        plt.gcf().canvas.set_window_title("Profile")
        plt.title('Press key "a" to add point in Method B')     
        plt.xlabel('x (nm)')
        plt.ylabel('intensity (counts)')
        plt.tight_layout()
        plt.minorticks_on()
        plt.grid(True) 
        plt.ion()
        ax_cnlp.plot(x_nm, y_ii,'k-')
        plt.show()       
        cid_cnlp = fig_cnlp.canvas.mpl_connect('key_press_event', cnlp_onkey)
    def reopenprofile(self,event):
        global xlist,ylist        
        if profile_path == "": return
        try:
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')                               
        x_nm = data[:,0]#nm
        y_ii = data[:,1]#intensity                                                                                             
        def cnlp_onkey(event):    
            if event.inaxes!=ax_cnlp.axes: return            
            onkey_chk(event.key,event.xdata,event.ydata)                                   
        def onkey_chk(key,x,y):   
            global xlist,ylist
            if key == u'a':
               for n in xlist:
                   if n == x: return #chk same element                  
               xlist.append(x)
               ylist.append(y)
               ax_cnlp.plot(x,y,'bo')
               self.text_cnpickup.append('%.3f            %.3f'%(x,y)) 
               fig_cnlp.canvas.draw()
            if key == u'c':
               if len(xlist) > 0:
                  xlist = []
                  ylist = []
                  self.text_cnpickup.setText('X(nm)              Y(intensity)')
                  last_step = len(ax_cnlp.lines)
                  del ax_cnlp.lines[1:last_step]
                  fig_cnlp.canvas.draw()                    
            if key == u'd':
               if len(xlist) > 0:     
                  xlist = xlist[0:len(xlist)-1]
                  ylist = ylist[0:len(ylist)-1]                
                  last_step = len(ax_cnlp.lines)
                  del ax_cnlp.lines[last_step-1]
                  fig_cnlp.canvas.draw()
                  self.text_cnpickup.undo()                                                                                                             
        fig_cnlp, ax_cnlp = plt.subplots()
        plt.gcf().canvas.set_window_title("Profile")
        plt.title('Press key "a" to add point in Method B')     
        plt.xlabel('x (nm)')
        plt.ylabel('intensity (counts)')
        plt.tight_layout()
        plt.minorticks_on()
        plt.grid(True) 
        plt.ion()
        ax_cnlp.plot(x_nm, y_ii,'k-')
        plt.show()       
        cid_cnlp = fig_cnlp.canvas.mpl_connect('key_press_event', cnlp_onkey)                   
    def cnab(self): 
        global cnabem_state #stored chk_state
        if self.checkBox_cnab.isChecked() == True:
           cnabem_state = 'Abs'
           self.checkBox_cnem.setCheckState(QtCore.Qt.Unchecked)
        else:
           cnabem_state = 'Emi'
           self.checkBox_cnem.setCheckState(QtCore.Qt.Checked)                
    def cnem(self): 
        global cnabem_state #stored chk_state
        if self.checkBox_cnem.isChecked() == True:
           cnabem_state = 'Emi'
           self.checkBox_cnab.setCheckState(QtCore.Qt.Unchecked)
        else:
           cnabem_state = 'Abs'
           self.checkBox_cnab.setCheckState(QtCore.Qt.Checked)  
    def cngc(self):
        if profile_path == "": return
        if cnabem_state == '': return 
        global z
        global method
        global nm_range
        s_value = self.spbox_cn1.value()#1-9
        p_value = self.spbox_cn2.value()#0.01-0.99
        try:
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')
        nm_range = self.lineEdit_cnrange.text().split('-')
        if nm_range == '' or len(nm_range) != 2:
           print 'Please input the wavelength range with correct format.'
           return
        nm_range = [int(nm_range[0]),int(nm_range[1])]      
        if nm_range[1] == nm_range[0]: nm_range[1] = nm_range[1]+1 
        if nm_range[1]-nm_range[0]<0: nm_range = [min(nm_range),max(nm_range)]           
        x_nm = data[:,0]#nm
        y_ii = data[:,1]#intensity            
        nm_range_idx = np.where((x_nm>=nm_range[0])&(x_nm<=nm_range[1]))
        x_nm = x_nm[nm_range_idx]
        y_ii = y_ii[nm_range_idx]

        from scipy import sparse
        from scipy.sparse.linalg import spsolve
        def baseline_als(y, lam = 5e5, p = 0.01, niter=10): #lam = 1e7, p = 0.05 0.03
            L = y.size#2e4
            D = sparse.csc_matrix(np.diff(np.eye(L), 2))
            w = np.ones(L)
            for i in xrange(niter):
              W = sparse.spdiags(w, 0, L, L)
              Z = W + lam * D.dot(D.transpose())
              zr = spsolve(Z, w*y)
              w = p * (y > zr) + (1-p) * (y < zr)
            return zr        
        lam1 = 5.*10**s_value #5e5 #5e5 ne #5e5 na #5e3  hg #5e3 sun  (1-9)
        p1 = p_value #0.96#0.01 ne #0.01 na #0.01  hg #0.96 sun (0.99-0.01)        
        z1 = baseline_als(y_ii,lam = lam1*2, p = p1)
        z= z1
        self.pushButton_cnplot.setText("Plot normalized spectrum (A)")
        method = 'A'
        fig_cnfit, ax_cnfit = plt.subplots()
        plt.gcf().canvas.set_window_title('Continuum smooth result')             
        plt.xlim(x_nm.min(),x_nm.max())
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity (counts)')
        plt.minorticks_on()
        plt.tight_layout()
        plt.plot(x_nm,y_ii,'k-',label='Orignal')
        plt.plot(x_nm,z1,'r-',label='Continuum smoother')      
        plt.legend(loc='best')
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
        plt.show()
    def cnpi_ck(self):
        if self.checkBox_cnpi.isChecked() == True:
           if path == '':self.checkBox_cnpi.setCheckState(QtCore.Qt.Unchecked)             
           if box[2] == 0 :self.checkBox_cnpi.setCheckState(QtCore.Qt.Unchecked)       
    def cngc2(self):
        if profile_path == "": return
        if cnabem_state == '': return 
        if len(xlist) < 4: 
           print 'The number of points need more than 4.'
           return        
        global z
        global method
        global nm_range
        try:
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')
        nm_range = self.lineEdit_cnrange.text().split('-')
        if nm_range == '' or len(nm_range) != 2:
           print 'Please input the wavelength range with correct format.'
           return
        nm_range = [int(nm_range[0]),int(nm_range[1])]      
        if nm_range[1] == nm_range[0]: nm_range[1] = nm_range[1]+1 
        if nm_range[1]-nm_range[0]<0: nm_range = [min(nm_range),max(nm_range)]           
        x_nm = data[:,0]#nm
        y_ii = data[:,1]#intensity            
        nm_range_idx = np.where((x_nm>=nm_range[0])&(x_nm<=nm_range[1]))
        x_nm = x_nm[nm_range_idx]
        y_ii = y_ii[nm_range_idx]
        if max(xlist)>nm_range[1] or min(xlist)<nm_range[0]:             
           print 'The selected points are out of range,please reselect!!' 
           return                            
        from scipy.interpolate import CubicSpline 
#        from scipy import interpolate       
        CS = CubicSpline(np.sort(xlist),np.asarray(ylist)[np.argsort(xlist)])
#        xlist = x_nm
#        ylist = y_ii
#        CS = interpolate.InterpolatedUnivariateSpline(xlist, ylist)
#        CS = CubicSpline(xlist,ylist)
#        x_sample = np.linspace(x_nm.min(),x_nm.max(),x_nm.size/50) 
        z2 = CS(x_nm)
#        CS = CubicSpline(x_sample,z2)        
#        z2 = CS(x_nm)
        z= z2
        self.pushButton_cnplot.setText("Plot normalized spectrum (B)")
        method = 'B'      
        fig_cnfit2, ax_cnfit2 = plt.subplots()
        plt.gcf().canvas.set_window_title('Continuum spline fitting result')             
        plt.xlim(x_nm.min(),x_nm.max())
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity (counts)')
        plt.minorticks_on()
        plt.tight_layout()
        plt.plot(x_nm,y_ii,'k-',label='Orignal')
        plt.plot(x_nm,z2,'r-',label='Continuum fitting')       
        plt.legend(loc='best')
        plt.locator_params(axis='x', tight=True,nbins=20) #set ticks range        
        plt.show()                      
    def cnplot(self):
        if profile_path == "": return #g
        if cnabem_state == '': return #g  
        if z.size == 0 : return
        if method == '': return
        try:
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('big5')
            data = np.genfromtxt(profile_path,dtype=float,delimiter=',') 
            sys.setdefaultencoding('utf-8')                                          
        x_nm = data[:,0]#nm
        y_ii = data[:,1]#intensity            
        nm_range_idx = np.where((x_nm>=nm_range[0])&(x_nm<=nm_range[1]))
        x_nm = x_nm[nm_range_idx]
        y_ii = y_ii[nm_range_idx]
#        current_tab = self.tabWidget_cn.currentIndex()# 0 for first
        savepath = 'Save//Profile_value//Normalization'
        if not os.path.exists(savepath): os.makedirs(savepath)
        file_name = profile_path.split(r'/')[len(profile_path.split(r'/'))-1]
        file_name = file_name[0:len(file_name)-4]
        file_save_path = 'Save//Profile_value//Normalization//%s_normalization_value_%s.csv'%(file_name, method)                     
        if os.path.isfile(file_save_path):     
           info = "Continuum normalization of this profile in Method %s has been done before.\n\
                   Do you want to overwrite existing profile?\n\
                   Yes   : Overwrite the existing file.\n\
                   No    : Save as new file.\n\
                   Ignore: Just show normalized spectrum and don't save anything."%(method)
           result = QtGui.QMessageBox.question(self.scrollArea,
                    "Overwrite or not...",info,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Ignore, QtGui.QMessageBox.Yes)   
           if result == QtGui.QMessageBox.Yes:
              save_action = True
           elif result == QtGui.QMessageBox.Ignore:
              save_action = False 
           else :
              save_action = True
              path_save, _ = QtGui.QFileDialog.getSaveFileName(None, "Normalized profile Save as...",os.getcwd(), "text (*.csv)") #
              if path_save == "": return
              file_save_path = path_save
        else:
            save_action = True
        
        if self.checkBox_cnpi.isChecked() == False:   
           fig_cnfit2, ax_cnfit2 = plt.subplots()
           plt.gcf().canvas.set_window_title('Continuum normalization')             
           plt.xlim(x_nm.min(),x_nm.max())
           plt.xlabel('Wavelength (nm)')
           plt.minorticks_on()
           plt.ylabel('Relative Intensity')  
           plt.tight_layout()
           if cnabem_state == 'Emi':  
              rmbaseline_y = (y_ii-z)/np.max(y_ii-z)              
           else: #abs
              rmbaseline_y = y_ii/z
              mask = np.where(y_ii>9)
              rmbaseline_y = rmbaseline_y[mask]
              x_nm = x_nm[mask]
           plt.plot(x_nm, rmbaseline_y,'r-',label=' ')
           save_data = np.concatenate((x_nm.reshape(x_nm.size,1), rmbaseline_y.reshape(x_nm.size,1)), axis=1) 
#           plt.legend(loc='best')        
           plt.locator_params(axis='x', tight=True,nbins=20)       
           plt.show()
        else:
           img = Image.open(path)
           xsize, ysize = img.size
           pix_area = img.crop((0,box[0],xsize,box[1]))            
           fig_cnfit2, ax_cnfit2 = plt.subplots()        
           ax_spimg = plt.subplot2grid((4,1), (0, 0),rowspan=3)
           plt.gcf().canvas.set_window_title("Continuum normalization")        
           ax_spimg.set_xlabel('Wavelength (nm)')
           ax_spimg.set_ylabel('Relative Intensity')
           plt.xlim(data[:,0].min(),data[:,0].max())
           plt.minorticks_on()       
           if cnabem_state == 'Emi':
              rmbaseline_y = (y_ii-z)/np.max(y_ii-z)
           else: #abs
              rmbaseline_y = y_ii/z
              mask = np.where(y_ii>9)
              rmbaseline_y = rmbaseline_y[mask] 
              x_nm = x_nm[mask]             
           plt.plot(x_nm, rmbaseline_y,'r-',label=' ')
           save_data = np.concatenate((x_nm.reshape(x_nm.size,1), rmbaseline_y.reshape(x_nm.size,1)), axis=1) 
           plt.locator_params(axis='x',nbins=20) #set ticks range     
           plt.subplot2grid((4,1), (3, 0),rowspan=1,sharex=ax_spimg)  
           plt.axis("off")                     
           if img.mode[0] == 'I' or img.mode[0] == 'F' or img.mode[0] == 'L' :
              pix_area = pix_area.convert('F').resize((xsize,2),Image.BILINEAR)#zoom in (32-bit floating)                          
              pix = np.asarray([pix_area.getdata()],dtype=np.uint8).reshape(2,xsize)              
              pix = pix[:,np.argsort(data[:,0])]
              plt.imshow(pix,aspect='equal',extent=(data[:,0].min(),data[:,0].max(), 65, 0),interpolation='bilinear',cmap='Greys_r')#aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)                                        
           else:              
              pix_area = pix_area.resize((xsize,2),Image.BILINEAR)#zoom in BILINEAR BICUBIC
              pix = np.asarray([pix_area.getdata()],dtype=np.uint8).reshape(2,xsize,3)            
              pix = pix[:,np.argsort(data[:,0]),:]
              plt.imshow(pix,aspect='equal',extent=(data[:,0].min(),data[:,0].max(), 100, 0),interpolation='bilinear')# bilinear bicubic aspect='auto''nearest''bilinear',aspect='equal',extent=(0, xsize, 1000, 0)             
           fig_cnfit2.tight_layout()       
           plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.05)
           plt.show()
        if save_action:  
           np.savetxt(file_save_path,save_data,delimiter=',',fmt='%.4f')
           print r'Saved to folder: Save\Profile_value\Normalization'        
                           
    def cnsave(self):
        if profile_path == "": return
        if cnabem_state == '': return   
        if z.size == 0: return        
        """
        profile_path, abs or emi, method
        A: s value, pvalue, z
        B: selected points(x and y), z          
        """ 
        savepath = 'Save//Profile_value//Normalization'
        if not os.path.exists(savepath):
           os.makedirs(savepath)
        filename1 = profile_path.split('/')[len(profile_path.split('/'))-1]
        filename1 = filename1[0:len(filename1)-4]
        filename = 'Save//Profile_value//Normalization//%s_normalization_data_%s.csv'%(filename1, method)
        file = open(filename , "w")                      
        if chk_cht(profile_path):           
           file.write('# %s continuum normalization data\n'%(filename1.encode('utf8')))#utf8
           file.write('# Profile file path:\n') 
           file.write('  %s\n'%(profile_path.encode('utf8')))          
        else: #all ascii
           file.write('# %s continuum normalization data\n'%(filename1)) 
           file.write('# Profile file path:\n')  
           file.write('  %s\n'%(profile_path))                                         
        file.write('# Type:\n')
        file.write('  %s\n'%(cnabem_state))
        file.write('# Method:(A=AsLS Smoothing; B=Pseudocontinuum points Fitting)\n')
        file.write('  %s\n'%(method))
        if method == 'A':
           file.write('# Parameters:(s_value, p_value)\n')
           s_value = self.spbox_cn1.value()#1-9
           p_value = self.spbox_cn2.value()#0.01-0.99
           file.write('  %d %.2f\n'%(s_value,p_value))          
           file.write('# Result:(z value)\n') 
           for i in range(z.size):           
               line = '  %.4f\n'%(z[i])
               file.write(line)               
        if method == 'B':
           file.write('# Parameters:(number of selected points, value of selected points)\n')            
           n = len(xlist)          
           file.write('  %d\n'%(n))          
           for i in range(n):           
               file.write('  %.3f %.4f\n'%(xlist[i],ylist[i])) 
           file.write('# Result:(z value)\n') 
           for i in range(z.size):           
               line = '  %.5f\n'%(z[i])
               file.write(line)
        file.write("%s-%s"%(nm_range[0],nm_range[1]))  
        file.close()
        print r'Saved to folder: Save\Profile_value\Normalization'                   
    def cnload(self):
        global profile_path #stored profile path
        global cnabem_state #stored chk_state
        global method
        global xlist,ylist
        global z #continuum normalization result 
        xlist = []
        ylist = []                
        z = np.array([],dtype=float)         
        path_cnload, _ =QtGui.QFileDialog.getOpenFileName(None, "Open csv file...",os.getcwd(), "text file (*.csv)") #"TXT(*.txt);;AllFiles(*.*)"          
        if path_cnload == "": return      
        file = open(path_cnload , "r")
        data = file.readlines()
        file.close()
        if data[1] != '# Profile file path:\n':
           print 'Open wrong file!!'
           return   
        profile_path = data[2][2:len(data[2])-1]#last is \n 
        if chk_cht(unicode(profile_path,'utf8')):
           profile_path = unicode(profile_path,'utf8') 
        #if lost the profile value
        if os.path.isfile(profile_path) != True:     
           info = "The profile value file of this result was not found.\n\
                   Do you want to select the profile value file manually?\n\
                   Yes   : Select the file.\n\
                   No    : End the task."               
           result = QtGui.QMessageBox.question(self.scrollArea,
                    "The profile value file was gone...",info,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)   
           if result == QtGui.QMessageBox.Yes:
              path_profile, _ = QtGui.QFileDialog.getOpenFileName(None, "Open profile value...",os.getcwd(), "text (*.csv)") #
              if profile_path == "": return
              profile_path = path_profile               
           else :
              return    
        profile_name = profile_path.split('/')[len(profile_path.split('/'))-1]
        self.label_cnpn.setText(profile_name)
        cnabem_state = data[4][2:len(data[4])-1]#last is \n
        if cnabem_state == 'Emi': self.checkBox_cnem.setCheckState(QtCore.Qt.Checked)
        if cnabem_state == 'Abs': self.checkBox_cnab.setCheckState(QtCore.Qt.Checked)  
        method = data[6][2:len(data[6])-1]#last is \n
        if method =='A':
           self.tabWidget_cn.setCurrentIndex(0)
           self.spbox_cn1.setValue(int(data[8][2]))
           self.spbox_cn2.setValue(float(data[8][4:8]))
           for i in range(len(data)-11): #size of x_p
               line_item = data[10+i][2:len(data[10+i])-1]
               z = np.append(z,float(line_item))
           self.pushButton_cnplot.setText("Plot normalized spectrum (A)")                      
        if method =='B':
           self.tabWidget_cn.setCurrentIndex(1)
           points = int(data[8][2:len(data[8])-1])
           for i in range(points): #size of x_p
               line_item = data[9+i][2:len(data[9+i])-1].split(' ')
               xlist.append(float(line_item[0]))
               ylist.append(float(line_item[1]))
               self.text_cnpickup.append('%.3f            %.3f'%(xlist[i],ylist[i])) 
           for i in range(len(data)-11-points): #size of x_p
               line_item = data[10+points+i][2:len(data[10+points+i])-1]
               z = np.append(z,float(line_item))   
           self.pushButton_cnplot.setText("Plot normalized spectrum (B)")                      
        w_range = data[-1]
        self.lineEdit_cnrange.setText(w_range)
        nm_range = self.lineEdit_cnrange.text().split('-')
        nm_range = [int(nm_range[0]),int(nm_range[1])]       
########################################################################
########################################################################           
    def geoadj_nw(self):
        global stretch_delta
        stretch_delta = np.array([],dtype=float)       
        self.scrollArea_geo = QtGui.QScrollArea()
        self.scrollArea_geo.resize(314, 319)      
        self.scrollArea_geo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)#AlwaysOn        
        self.scrollArea_geo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea_geo.setWindowTitle('Straighten arc llines...') 
        self.scrollArea_geo.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)        
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(11)
        self.nw_geoadj = QtGui.QWidget()#self.scrollArea_geo
        self.nw_geoadj.resize(304, 309)   
        self.scrollArea_geo.setWidget(self.nw_geoadj)       
        self.label_geoadj1 = QtGui.QLabel(self.nw_geoadj)
        self.label_geoadj1.setGeometry(QtCore.QRect(QtCore.QRect(7, 4, 304, 66)))#22       
        self.label_geoadj1.setText("Click the button 'Select Peaks' to choose 1 ~\n3 peaks which well spaced over the whole of \nspectrum in the profile figure.")                                    
        self.label_geoadj1.setFont(font)       
        self.pushButton_geosp = QtGui.QPushButton(self.nw_geoadj) #do it 
        self.pushButton_geosp.setGeometry(QtCore.QRect(74, 69, 165, 28))        
        self.pushButton_geosp.setText("Select Peaks") 
        self.pushButton_geosp.setFont(font)
        self.label_geoadj2 = QtGui.QLabel(self.nw_geoadj)
        self.label_geoadj2.setGeometry(QtCore.QRect(QtCore.QRect(7, 109, 304, 44)))#22       
        self.label_geoadj2.setText("Then click the button 'Straighten' to run the \nprocess and show the results.")                                    
        self.label_geoadj2.setFont(font) 
        self.pushButton_dostr = QtGui.QPushButton(self.nw_geoadj) #do it 
        self.pushButton_dostr.setGeometry(QtCore.QRect(74, 153, 165, 28))        
        self.pushButton_dostr.setText("Straighten") #145
        font.setBold(True)           
        self.pushButton_dostr.setFont(font)
        font.setBold(False)
        self.pushButton_savedata = QtGui.QPushButton(self.nw_geoadj) 
        self.pushButton_savedata.setGeometry(QtCore.QRect(88, 186, 137, 28))        
        self.pushButton_savedata.setText("Save result data")    
        self.pushButton_savedata.setFont(font)
        self.label_geoadj2 = QtGui.QLabel(self.nw_geoadj)        
        self.label_geoadj2.setGeometry(QtCore.QRect(QtCore.QRect(7, 217, 304, 66)))        
        self.label_geoadj2.setText("You can do batch process of images by using\nthe result data above and get the straightened\nimages and profiles.")
        self.label_geoadj2.setFont(font)                
        self.pushButton_batpro = QtGui.QPushButton(self.nw_geoadj) 
        self.pushButton_batpro.setGeometry(QtCore.QRect(74, 278, 165, 27))        
        self.pushButton_batpro.setText("Batch processing")    
        self.pushButton_batpro.setFont(font)
        #########################################################
        self.pushButton_geosp.clicked.connect(self.geoadj_select)             
        self.pushButton_dostr.clicked.connect(self.geoadj_dostr)
        self.pushButton_savedata.clicked.connect(self.geoadj_savedata)
        self.pushButton_batpro.clicked.connect(self.geoadj_batch)  
        self.scrollArea_geo.show()                     
        
    def geoadj_select(self):         
        global plot_x,intensity_box,xlist,ylist
        if path == "" or box[1] == 0: 
           print 'Please load image and select image area.'
           return
        ylist = []
        xlist = []
        plot_x, intensity_box = intensitybox(path,box)#plot_x idx0 is 1                                                                                                 
        def geoadj_onkey(event):    
            if event.inaxes!=ax_geoadj.axes: return            
            onkey_chk(event.key,event.xdata,event.ydata)                                   
        def onkey_chk(key,x,y):   
            global xlist,ylist
            if key == u'a': 
               xlist.append(x)#ori_point is 1 ,only used xlist
               ylist.append(y)#ori_point is 0, not use
               ax_geoadj.plot(x,y,'ro')               
               if len(xlist)%2 == 0: #even
                  linex = [x,xlist[len(xlist)-2]] 
                  liney = [y,ylist[len(xlist)-2]] 
                  ax_geoadj.plot(linex,liney,'r-')  
               fig_geoadj.canvas.draw()
            if key == u'c':
               if len(xlist) > 0:               
                  xlist = []
                  ylist = []
                  last_step = len(ax_geoadj.lines)
                  del ax_geoadj.lines[1:last_step]
                  fig_geoadj.canvas.draw()
        class Formatter(object): # set mpl gui x y show in int
            def __init__(self, im):
                self.im = im
            def __call__(self, x, y):
                return 'x=%d, y=%d'%(int(x), int(y))                                                                              
        fig_geoadj, ax_geoadj = plt.subplots()
        plt.gcf().canvas.set_window_title("Profile(Y=%d to %d) select peaks"%(int(box[0])+1,int(box[1])))          
        plt.xlim(0,plot_x.size)
        plt.xlabel('x (pixel)')
        plt.ylabel('intensity (counts)')
        plt.title('Use the keyboard key "a" to select 1~3 peaks')
        des = 'Press key "a" on both sides of the peak.\nPress key "c" to clear all selection.'
        plt.tight_layout()
        plt.minorticks_on()
        plt.grid(True)
        plt.ion()
        im = ax_geoadj.plot(plot_x,intensity_box,'k-',label=des)        
        ax_geoadj.format_coord = Formatter(im)        
        plt.legend(loc='best')    
        plt.show()       
        cid_geoadj = fig_geoadj.canvas.mpl_connect('key_press_event', geoadj_onkey)               
    def geoadj_dostr(self):
        global stretch_delta
        if path == "" or box[1] == 0: 
           print 'Please load image and select image area.'
           return
        if len(xlist) < 1 or len(xlist) > 6 or len(xlist)%2 != 0 : 
           print 'Please select 1~3 peaks.'
           return
        if box[1] - box[0] < 8 : #img y 
           print 'The image area should large than 8 pixel.'
           return 
        from scipy.optimize import leastsq 
        ################################
        def gauss(x, p):
            noi = p[0]
            aa = p[1]
            mu = p[2]
            sigma =p[3] 
            fun = aa*np.exp(-(x-mu)**2/(2.*sigma**2))+noi
            return fun            
        def residulas(p, fitx, select_y_range):
            return (gauss(fit_x, p)-select_y_range)**2 
        ###############################          
        img = Image.open(path) 
        xsize, ysize = img.size          
        pix_area = img.crop((0,box[0],xsize,box[1]))#left up(idx) right down(nth)
        if img.mode[0] == 'L' or img.mode[0] == 'I' or img.mode[0] == 'F' :
           pix_gray = np.asarray(pix_area.getdata()).reshape(box[1]-box[0], xsize)#dirctive get grey scale
           pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16  
        else:   
           pix = np.asarray(pix_area).reshape(box[1]-box[0],xsize,3)#get rgb
           pix_gray = pix[:,:,0]*0.333+pix[:,:,1]*0.333+pix[:,:,2]*0.333 

        fit_arc_line_y_all = np.zeros(box[1]-box[0])
        fit_arc_line_x_all = np.zeros(box[1]-box[0]) 
        delta_all = np.zeros(box[1]-box[0])                      
        for arc_number in range(len(xlist)/2) : #0:2  2:4  4:6 0 1 2 
            x1min = int(min(xlist[arc_number*2:arc_number*2+2]))-1
            x1max = int(max(xlist[arc_number*2:arc_number*2+2]))       
            fit_x =  plot_x[x1min:x1max]-1#xlist start from 1 same as plot x
            mean = np.mean(fit_x)         #and fit_x need match img so need -1
            std = np.std(fit_x)       
            result_max_x = np.array([],dtype=float) #img x
            result_max_y = np.array([],dtype=float) #img y         
            for n in np.linspace(0,box[1]-box[0]-1,(box[1]-box[0])/3+1,dtype=int):# img y direction and number -1
                select_y = pix_gray[n] #pix_gray is 2d, idx0 is 0
                select_y_range = select_y[fit_x]
                amp = np.max(select_y_range)
                pini = [5., amp, mean, std]
                res, flag = leastsq(residulas, pini, args=(fit_x, select_y_range))         
                fit_result = gauss(fit_x, res)           
                fit_max_y = np.max(fit_result) # not use
                fit_max_x = fit_x[np.where(fit_result == fit_max_y)]
                if fit_max_x.size == 1:                    
                   result_max_x = np.append(result_max_x,fit_max_x)   
                   result_max_y = np.append(result_max_y,n)                    
                else:
                   print 'skip row = ',n            
            fit_arc_line = np.polyfit(result_max_y, result_max_x, 3) #get fit para
            fit_arc_line_fun = np.poly1d(fit_arc_line)#build function
            fit_arc_line_y = np.arange(box[1]-box[0])
            fit_arc_line_x = fit_arc_line_fun(fit_arc_line_y)#input y get x, start from 0
            delta = fit_arc_line_x-fit_arc_line_x[fit_arc_line_x.size/2]#n=top0~down0
            fit_arc_line_y_all = np.vstack((fit_arc_line_y_all,fit_arc_line_y))
            fit_arc_line_x_all = np.vstack((fit_arc_line_x_all,fit_arc_line_x)) 
            delta_all = np.vstack((delta_all,delta)) 
        n_arc_line = np.int(fit_arc_line_x_all.shape[0])-1
        delta = np.sum(delta_all,axis=0)/n_arc_line 
        stretch_delta = delta              
        def plot_fitting_arc_line(nt_line):      
            img_show = mpimg.imread(path)
            class Formatter(object): # set mpl gui x y show in int
                def __init__(self, im):
                    self.im = im
                def __call__(self, x, y):
                    return 'x=%d, y=%d'%(int(x), int(y))
            fig15, ax15 = plt.subplots()
            plt.gcf().canvas.set_window_title('The reslut of fitting arc line')
            plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            plt.axis("off")        
            plt.xlim(0,xsize)
            plt.ylim(ysize,0)            
            if img.mode[0] == 'I' or img.mode[0] == 'L' or img.mode[0] == 'F' :       
               im = ax15.imshow(img_show,interpolation='none',cmap='Greys_r')
            else:
               im = ax15.imshow(img_show,interpolation='none')            
            for n in range(nt_line): 
                ax15.plot(fit_arc_line_x_all[n+1], fit_arc_line_y_all[n+1]+box[0],'w-')        
            ax15.format_coord = Formatter(im)
            plt.show()        
        ###############################################creat new image
        new_img_mono = np.zeros((box[1]-box[0],xsize),dtype=float)                
        for idx in range(box[1]-box[0]):  #pix_gray is mono         
            if delta[idx] > 0:                 
               new_img_mono[idx,0:xsize-int(np.round(delta[idx],0))] = pix_gray[idx,int(np.round(delta[idx],0)):xsize]             
            if delta[idx] == 0:
               new_img_mono[idx,0:xsize] = pix_gray[idx,0:xsize]                           
            if delta[idx] < 0:
               new_img_mono[idx,int(np.round(-delta[idx],0)):xsize] = pix_gray[idx,0:xsize-int(np.round(-delta[idx],0))]        
        ###############################################                     
        def plot_new_img(img_show_mono):
            class Formatter(object): # set mpl gui x y show in int
                def __init__(self, im):
                    self.im = im
                def __call__(self, x, y):
                    return 'x=%d, y=%d'%(int(x)+1, int(y)+1)
            fig_new_img_mono, ax_new_img_mono = plt.subplots()
            plt.gcf().canvas.set_window_title('The stretched image')
            plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            plt.axis("off")        
            plt.xlim(0,xsize)
            plt.ylim(box[1]-box[0],0)      
            im_mono = ax_new_img_mono.imshow(img_show_mono,cmap='Greys_r',interpolation='none')
            ax_new_img_mono.format_coord = Formatter(im_mono)
            plt.show()
#            plt.imsave('ttt.tiff',img_show_mono,cmap='Greys_r',vmin=0.,vmax=255.)
        def plot_new_profile(img_show_mono): 
            fig_new_img_profile, ax_new_img_profile = plt.subplots()
            plt.gcf().canvas.set_window_title('The result of profile')
            plt.axis("on")
            plt.tight_layout()
            plt.minorticks_on()
            plt.grid(True)            
            plt.xlim(0,xsize)
            plt.xlabel('x (pixel)')
            plt.ylabel('intensity (counts)')
            plot_x = np.asarray(range(xsize)) #set x-axis +1      
            intensity_new = img_show_mono.sum(axis=0)/(box[1]-box[0])            
            plt.plot(plot_x, intensity_new,'b-',label='New')
            plt.plot(plot_x, intensity_box,'k--',label='Orignal')        
            plt.legend(loc='best')                 
            plt.show()
        plot_fitting_arc_line(n_arc_line)             
        plot_new_img(new_img_mono)             
        plot_new_profile(new_img_mono)             
    def geoadj_savedata(self):
        if stretch_delta.size == 0: 
           print "Please select 1~3 peaks than click buttom 'Straighten'."
           return
        path_save, _ = QtGui.QFileDialog.getSaveFileName(None, "Save result data...",os.getcwd(), "text (*.csv)") #
        if path_save == "": return
        path_savedata = path_save
        np.savetxt(path_savedata, stretch_delta, delimiter=',',fmt='%.3f')
        file = open(path_savedata , "a")
        file.write('# box_y1  box_y2  flag \n')
        file.write('#   %d   %d   %d\n'%(box[0],box[1],box[2]))                
        file.close()
#######################################################################
    def geoadj_batch(self):       
        global st_img_loc
        st_img_loc = np.array([],dtype=str)
        self.nw_geoadj_batch = QtGui.QWidget()
        self.nw_geoadj_batch.resize(480, 380)
        self.nw_geoadj_batch.setWindowTitle('Batch Straighten Images')
        font = QtGui.QFont() 
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)     
        self.pushButton_ipdata = QtGui.QPushButton(self.nw_geoadj_batch)
        self.pushButton_ipdata.setGeometry(QtCore.QRect(12, 12, 115, 28))        
        self.pushButton_ipdata.setText("Input data...")             
        self.pushButton_ipdata.setFont(font)
        self.pushButton_savefolder = QtGui.QPushButton(self.nw_geoadj_batch)
        self.pushButton_savefolder.setGeometry(QtCore.QRect(12, 45, 115, 28))        
        self.pushButton_savefolder.setText("Output folder...")             
        self.pushButton_savefolder.setFont(font)
        self.lineEdit_ipdata = QtGui.QLineEdit(self.nw_geoadj_batch)
        self.lineEdit_ipdata.setGeometry(QtCore.QRect(131, 12, 344, 26))
        self.lineEdit_ipdata.setText('')
        self.lineEdit_ipdata.setFont(font)        
        self.lineEdit_savefolder = QtGui.QLineEdit(self.nw_geoadj_batch)
        self.lineEdit_savefolder.setGeometry(QtCore.QRect(131, 46, 344, 26))
        self.lineEdit_savefolder.setText('')
        self.lineEdit_savefolder.setFont(font)     
        self.pushButton_addimg = QtGui.QPushButton(self.nw_geoadj_batch)
        self.pushButton_addimg.setGeometry(QtCore.QRect(12, 78, 115, 28))        
        self.pushButton_addimg.setText("Add Image")             
        self.pushButton_addimg.setFont(font) 
        self.pushButton_rmimg = QtGui.QPushButton(self.nw_geoadj_batch)
        self.pushButton_rmimg.setGeometry(QtCore.QRect(135, 78, 115, 28))        
        self.pushButton_rmimg.setText("Remove Image")             
        self.pushButton_rmimg.setFont(font)         
        self.listWidget_addimg = QtGui.QListWidget(self.nw_geoadj_batch)
        self.listWidget_addimg.setGeometry(QtCore.QRect(12, 113, 463, 188))
        self.listWidget_addimg.setFont(font)         
        self.label_save_option = QtGui.QLabel(self.nw_geoadj_batch)
        self.label_save_option.setGeometry(QtCore.QRect(12, 303, 115, 28))
        self.label_save_option.setTextFormat(QtCore.Qt.PlainText)
        self.label_save_option.setText('Output Options:')      
        self.label_save_option.setFont(font)                 
        self.combobox_save_option = QtGui.QComboBox(self.nw_geoadj_batch)        
        self.combobox_save_option.setGeometry(QtCore.QRect(127, 306, 180, 24))
        self.combobox_save_option.setEditable(False)#(12, 330, 190, 28)
        self.combobox_save_option.setMaxVisibleItems(3)
        self.combobox_save_option.addItem("Mono Image in TIFF")#.setItemText(0,'aa')
        self.combobox_save_option.addItem("Profile Value in CSV")        
        self.combobox_save_option.addItem("Both Image and Profile")
        self.combobox_save_option.setFont(font)
        self.combobox_save_option.setCurrentIndex(0)    
        self.pushButton_doitst = QtGui.QPushButton(self.nw_geoadj_batch) 
        self.pushButton_doitst.setGeometry(QtCore.QRect(355, 340, 115, 28))        
        self.pushButton_doitst.setText("Straighten")             
        self.pushButton_doitst.setFont(font)    
        self.progressbar_st = QtGui.QProgressBar(self.nw_geoadj_batch)
        self.progressbar_st.setGeometry(QtCore.QRect(12, 341, 153, 26))
        font.setPointSize(10)
        self.progressbar_st.setFont(font) 
        ###########################################################
        self.pushButton_ipdata.clicked.connect(self.bat_ipdata)
        self.pushButton_savefolder.clicked.connect(self.bat_savefolder)
        self.pushButton_addimg.clicked.connect(self.bat_addimg)
        self.pushButton_rmimg.clicked.connect(self.bat_rmimg)
        self.pushButton_doitst.clicked.connect(self.bat_doitst)
        self.nw_geoadj_batch.show()       
    def bat_ipdata(self):   
        path_load, _ = QtGui.QFileDialog.getOpenFileName(None, "Load Result Data...",os.getcwd(), "text (*.csv)") #
        if path_load == "": return
        file = open(path_load , "r")   
        data = file.readlines()
        file.close()
        if data[-1][0] != '#':#open wrong file
           self.lineEdit_ipdata.setText('')
           print 'Input wrong file!!'
           del data
           return 
        self.lineEdit_ipdata.setText(path_load)
        del data
    def bat_savefolder(self):   
        path_load = QtGui.QFileDialog.getExistingDirectory(None, "Choose Output Folder...",os.getcwd()) #QtGui.QFileDialog.ShowDirsOnly
        if path_load == "": return
        self.lineEdit_savefolder.setText(path_load)        
    def bat_addimg(self):
        global st_img_loc
        path_img, _ =QtGui.QFileDialog.getOpenFileName(None, "Load image...",os.getcwd(), "Image (*.jpg *.jpeg *.tif *.tiff)")
        if path_img == "": return        
        filename = path_img.split('/')[len(path_img.split('/'))-1]            
        st_img_loc = np.append(st_img_loc,path_img)        
        item = QtGui.QListWidgetItem()
        item.setText(filename)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)#Unchecked
        self.listWidget_addimg.addItem(item)               
    def bat_rmimg(self):        
        global st_img_loc
        if st_img_loc.size == 0:return
        item = self.listWidget_addimg.item(st_img_loc.size-1)
        self.listWidget_addimg.removeItemWidget(item)
        self.listWidget_addimg.takeItem(st_img_loc.size-1)        
        st_img_loc = st_img_loc[0:st_img_loc.size-1]       
    def bat_doitst(self):
        if st_img_loc.size == 0:return
        if self.lineEdit_savefolder.text() == "" : return        
        if self.lineEdit_ipdata.text() == "" : return
        doit_idx = []
        for idx in range(st_img_loc.size):
            item = self.listWidget_addimg.item(idx)            
            if item.checkState() == QtCore.Qt.Checked : doit_idx.append(idx)
        if len(doit_idx) == 0: return 
        try:
            delta = np.genfromtxt(self.lineEdit_ipdata.text(),dtype=float,delimiter=',')
        except UnicodeDecodeError:
               reload(sys)  
               sys.setdefaultencoding('big5')               
               delta = np.genfromtxt(self.lineEdit_ipdata.text(),dtype=float,delimiter=',')
               sys.setdefaultencoding('utf-8')              
        file = open(self.lineEdit_ipdata.text(),   "r")   
        temp = file.readlines()
        file.close()
        box = np.asarray(temp[-1].split('   ')[1:4],dtype=int)#3rd line;first element is ''
        del temp        
        savepath = self.lineEdit_savefolder.text()
        save_opt = str(self.combobox_save_option.currentText())
        self.progressbar_st.reset()
        self.progressbar_st.setRange(0,len(doit_idx))        
        step = 1               
        def st_save_img(savepath,filename,new_img_mono,img_mode):
            if img_mode == 'I' or img_mode == 'F': #32bits or 16bits
               img_mono = Image.fromarray(np.uint16(new_img_mono),'I;16')               
            else: # RGB L b bit
               img_mono = Image.fromarray(np.uint8(new_img_mono),'L') 
               img_mono.save(savepath+'\\'+filename+'_straightened.tiff')
        def st_save_profile(savepath,filename,new_img_mono,img_mode):
            intensity_new = new_img_mono.sum(axis=0)/(box[1]-box[0])            
            plotx_new = np.arange(intensity_new.size)
            save_data = np.concatenate((plotx_new.reshape(plotx_new.size,1), intensity_new.reshape(plotx_new.size,1)), axis=1)       
            np.savetxt(savepath+'\\'+filename+'_straightened_profile_value.csv', save_data, delimiter=',',fmt='%.4f')
               
        for idx_chk in doit_idx: #process image         
            loc = st_img_loc[idx_chk]
            filename = loc.split('/')[len(loc.split('/'))-1] 
            img = Image.open(loc)
            xsize, ysize = img.size
            img_mode = img.mode[0]
            if img_mode == 'RGBA': return             
            try:
                pix_area = img.crop((0,box[0],xsize,box[1]))                 
            except UnicodeDecodeError:
#                   print 'UnicodeDecodeError'
                   reload(sys)  
                   sys.setdefaultencoding('big5')               
                   pix_area = img.crop((0,box[0],xsize,box[1])) 
                   sys.setdefaultencoding('utf-8')
            except UnicodeEncodeError:
#                   print 'UnicodeEncodeError'
                   reload(sys)  
                   sys.setdefaultencoding('utf8')               
                   pix_area = img.crop((0,box[0],xsize,box[1])) 
                   sys.setdefaultencoding('utf-8')
            if img_mode == 'L' or img_mode == 'I' or img_mode == 'F' :
               pix_gray = np.asarray(pix_area.getdata()).reshape(box[1]-box[0], xsize)
               pix_gray[pix_gray < 0] = pix_gray[pix_gray < 0]+2**16  
            else:   
               pix = np.asarray(pix_area).reshape(box[1]-box[0],xsize,3)
               pix_gray = pix[:,:,0]*0.333+pix[:,:,1]*0.333+pix[:,:,2]*0.333         
            ##############################creat new image
            new_img_mono = np.zeros((box[1]-box[0],xsize),dtype=float)                
            for idx in range(box[1]-box[0]):  #pix_gray is mono         
                if delta[idx] > 0:                 
                   new_img_mono[idx,0:xsize-int(np.round(delta[idx],0))] = pix_gray[idx,int(np.round(delta[idx],0)):xsize]             
                if delta[idx] == 0:
                   new_img_mono[idx,0:xsize] = pix_gray[idx,0:xsize]                           
                if delta[idx] < 0:
                   new_img_mono[idx,int(np.round(-delta[idx],0)):xsize] = pix_gray[idx,0:xsize-int(np.round(-delta[idx],0))]        
            ###############################################                
            if save_opt == "Mono Image in TIFF": 
               st_save_img(savepath,filename,new_img_mono,img_mode)
            if save_opt == "Profile Value in CSV":
               st_save_profile(savepath,filename,new_img_mono,img_mode)          
            if save_opt == "Both Image and Profile":    
               st_save_img(savepath,filename,new_img_mono,img_mode)
               st_save_profile(savepath,filename,new_img_mono,img_mode)
            self.progressbar_st.setValue(step)
            step += 1   
########################################################################         
########################################################################  
    def retranslateUi(self, MainWindow): #Python Spectrum Application
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", '%s'%(version), None, QtGui.QApplication.UnicodeUTF8))
        ###tab_1
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Load Image", None, QtGui.QApplication.UnicodeUTF8))#Load Image
        self.groupBox_t1select.setTitle(QtGui.QApplication.translate("MainWindow", "1. Select image area", None, QtGui.QApplication.UnicodeUTF8)) 
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "The width is fixed equal to full width of image.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Y2 pixel (down)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Y1 pixel (up)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "Lock", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Show Profile in Pixel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_t1wc.setTitle(QtGui.QApplication.translate("MainWindow", "2. WaveLength Calibration", None, QtGui.QApplication.UnicodeUTF8)) 
        self.stdLight.setItemText(0, QtGui.QApplication.translate("MainWindow", "Light source", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(1, QtGui.QApplication.translate("MainWindow", "Sun", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(2, QtGui.QApplication.translate("MainWindow", "Neon Lamp", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(3, QtGui.QApplication.translate("MainWindow", "Fluorescent(Hg) Lamp", None, QtGui.QApplication.UnicodeUTF8))
        self.stdLight.setItemText(4, QtGui.QApplication.translate("MainWindow", "Custom", None, QtGui.QApplication.UnicodeUTF8))      
        self.poly_cali.setItemText(0, QtGui.QApplication.translate("MainWindow", "Polynomial calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.poly_cali.setItemText(1, QtGui.QApplication.translate("MainWindow", "1st order (simple linear)", None, QtGui.QApplication.UnicodeUTF8))
        self.poly_cali.setItemText(2, QtGui.QApplication.translate("MainWindow", "2ed order ", None, QtGui.QApplication.UnicodeUTF8))
        self.poly_cali.setItemText(3, QtGui.QApplication.translate("MainWindow", "3rd order ", None, QtGui.QApplication.UnicodeUTF8))
        self.poly_cali.setItemText(4, QtGui.QApplication.translate("MainWindow", "4th order ", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "InPut X pixel", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Wavelength (nm)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Residual", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("MainWindow", "Load calibration data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Result:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_t1plot.setTitle(QtGui.QApplication.translate("MainWindow", "3. Show Wavelength-calibrated Profile", None, QtGui.QApplication.UnicodeUTF8)) 
        self.pushButton_7.setText(QtGui.QApplication.translate("MainWindow", "Plot Profile in Wavelength", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_9.setText(QtGui.QApplication.translate("MainWindow", "Load Profile(s) and Plot...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_11.setText(QtGui.QApplication.translate("MainWindow","Plot with image in curve shape", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Information", None, QtGui.QApplication.UnicodeUTF8))

def readme(self): #tab1
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is i write into Qt 
#    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is Qt object name
#    QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("utf8")) #told Qt what codec is local document
    self.README.setText('PySA主要用於解析光譜影像，快速生成圖譜數據(profile value)並結合影像顯示，可輸出數據及影像作為後續分析使用。\
支援 .jpg 及.tiff 的彩色(8bits)或單色(8、16bits)影像。')
    self.README.append('2.0.1 Script 版建議使用環境:')
    self.README.append('Python 2.7.12; Matplotlib 2.1.2; Numpy 1.11.3; Scipy 1.0.0; Pillow 5.0.0; Pyside 1.2.4' )
    self.README.append('')
    self.README.append('PySA 2.0.1 主要有以下功能:')
    self.README.append('A. 光譜波長校正(使用多項式回歸分析)')
    self.README.append('   >>內建三種參考光源之波長數據(sun,neon,hg)。') 
    self.README.append('   >>可從圖譜(profile)上選取譜線自動輸入譜線位置或參考波長。') 
    self.README.append('   >>自動儲存校正資料，方便之後校正其他光譜影像。') 
    self.README.append('   >>自動儲存校正後的圖譜數據，方便供後續分析使用。') 
    self.README.append('   >>圖譜數據結合光譜影像顯示。') 
    self.README.append('B. 連續光譜強度歸一化(continuum normalization or baseline correction)')    
    self.README.append('   >>提供兩種歸一化方式:') 
    self.README.append('       Asymmetric Least Squares Smoothing')     
    self.README.append('       Pseudocontinuum Points Fitting') 
    self.README.append('   >>可儲存歸一化結果，方便之後再度使用。') 
    self.README.append('   >>自動儲存歸一化後之圖譜數據，數據可結合光譜影像顯示。') 
    self.README.append('C. 光譜影像之弧線校直(straighten smile curve)')
    self.README.append('   >>快速顯示校直結果。')     
    self.README.append('   >>提供批次處理影像功能，輸出校直後之影像或是圖譜數據(pixel unit)。') 
    self.README.append('D. 其他')
    self.README.append('   >>提供多重圖譜數據顯示功能，方便比較數據差異。') 
    self.README.append('   >>本程式使用Matplotlib作為主要繪製工具，故可客製化圖表呈現方式。') 
    self.README.append('E. 注意事項')
    self.README.append('   >>載入之光譜影像必須是橫向展開且不歪斜。') 
    self.README.append('   >>輸入選擇影像區域的Y值(最小值=1)後，必需按下[LOCK]鍵。') 
    self.README.append('   >>自動儲存的檔案存放於此程式所在的資料夾下名為Save的資料夾。') 
    self.README.append('   >>如欲離開本程式，按右上角X即可。\n') 

def readme_about(self):
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf8")) 
    self.README_about.setText('PySA (Python Spectrum Application)')
    self.README_about.append('Version: 2.0.1  Build: 20180205  GitHub: https://github.com/lcrobert/PySA') 
    self.README_about.append('Created by Yen-Chun Luo Cho (Robert)  Email: lcrobert.rocket@gmail.com')     
    self.README_about.append('Powered by Python, Matplotlib, Numpy, Scipy, PIL, PySide, PyInstaller')

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

if __name__ == '__main__':
 app = QtGui.QApplication(sys.argv)
 screen_rect = app.desktop().screenGeometry()
 width, height = screen_rect.width(), screen_rect.height()
# import platform
# osver = platform.platform().split('-')[0:2] 
 mySW = ControlMainWindow()
 mySW.show()
 sys.exit(app.exec_())	
