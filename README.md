# PySA2 - A GUI tool of spectral image analysis
###   [ This repo is no longer supported. ]

這個 repo 將於 20190205 停止維護，如有類似的光譜影像分析需求，可到 [PySA WebApp](https://lcrobert.pythonanywhere.com/pysa/) 網站使用線上影像分析工具 。其實本來有預計把程式碼重新以 py3 和 pyside2 改寫，並加入光譜平場修正  ( code已寫好雛型 ) 及其他小功能，但因為時間實在不夠用，目前我會先以開發維護 PySA WebApp 網站為主。 

Last update : 20190131

------

<br/>

[README.md English version](https://github.com/lcrobert/PySA/blob/master/README.en.md)

PySA2 主要用於分析光譜影像，目前影像支援 .jpg 及 .tiff 的彩色 (8 bit / channel) 或單色 (8、16 bit )。

目前程式有以下功能 : 

- > 光譜波長校正 ( 使用多項式擬合 )

  ```bash
  - 內建三種參考光源之波長數據(sun,neon,hg)
  - 藉由點選參考光源圖譜(profile)上的譜線，程式自動輸入參考波長
  - 使用高斯擬合找出波峰位置
  - 自動儲存校正資料及圖譜數據
  - 可顯示圖譜結合實際影像的畫面。
  ```

- > 連續光譜強度歸一化 ( continuum normalization or baseline correction )

  ```bash
  - 方法1 : Asymmetric Least Squares Smoothing
  - 方法2 : Pseudocontinuum Points Fitting
  - 自動儲存歸一化參數及圖譜數據
  - 可顯示圖譜結合實際影像的畫面
  ```

- > 光譜影像中的譜線弧度修正 ( straighten 'smile' curve ) 

  ```bash
  影像中的譜線呈現如同微笑曲線般的彎曲形狀，且彎曲弧度隨波長增加而變大，通常發生在以光學透鏡為準直元件的低精密度光譜儀上。
  此功能目地就是要找出曲線的平均弧度然後將之拉直，此外也提供批次處理影像的功能，可選擇輸出影像或profile值
  ```

- > 其他

  ```
  - 提供多重圖譜數據顯示功能，方便比較數據差異
  - 使用 Matplotlib 作為影像、圖譜顯示工具
  ```

<br/>

Package requirements
---------------------

Python 2.7.12

Qt4 (absolutely not 5 )

- version 2  :  *PySA_2_20170915.py*

  Numpy 1.11.1 ;  Scipy 0.18.1 ;  Matplotlib 1.5.3 ;  PySide 1.2.4 ;  Pillow 3.3.1

- version 2.0.1 :  *PySA_2.0.1_20180205.py*

  Numpy 1.11.3 ;  Scipy 1.00.0 ;  Matplotlib 2.1.2 ;  PySide 1.2.4 ;  Pillow 5.0.0

  

<br/>


Executable version 
----------------
The .exe version of PySA2 can be downloaded from here ( ~ 191 MB) : ( packaged by PyInstaller3.2.1 )
https://drive.google.com/open?id=0B8NFdyNDlKXgTDBuSVdiNFh1Tk0

The tutorial video : 
https://youtu.be/1pVMPJT6UWw

<br/>



## Program snapshots

- ### Main window 

  ![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s1.png)



- ### Wavelength calibration 

  ![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s2.png)



- ### Continuum normalization ( Baseline correction )

  ![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s4-1.png)

  <br/>![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s4-2-2.png)



- ### Arc-line correction ( Straighten 'smile' curve )

  ![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s5.png)

  <br/>![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s6.png)



- ### Plot multiple spectra

  ![](https://lcycblog.files.wordpress.com/2019/01/pysa2_s3.png)









































