# PySA2 - A GUI tool of spectral image analysis
###   [ This repo is no longer supported. ]

This repo is no longer supported, if you need a tool like this, please use the [PySA WebApp](https://lcrobert.pythonanywhere.com/pysa/) website.  Actually, I have a plan to rewrite the code with python3 and pyside2, and add something new functions like spectral  flat-field correction, but now I don't have enough time so currently I will focus on maintaining the PySA Web App website first.   

Last update : 20190131

------

<br/>

PySA2 is a gui program mainly used to analyze spectral images ( **!! not hyperspectral images !!**  )  and supports .jpg and .tiff color ( 8 bit / channel ) or monochrome ( 8, 16 bit ) images currently.



> ### **The 5 main functions :** 
>
> - Wavelength calibration ( using polynomial fitting )
>
> - Showing spectra ( profile ) and spectral image in same figure
>
> - Continuum normalization ( baseline correction )
>
>   method 1 : Asymmetric Least Squares Smoothing
>
>   method 2 : Pseudocontinuum Points Fitting
>
> - Arc-line correction  ( straighten 'smile' curve ) 
>
> - Plot multiple spectra

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









































