#-*- coding: utf-8 -*-
#file : BAChange.py
#Created by Park Dong Jin
#Create 2017/08/30
#Version 1.0

import os, glob, math
#---Find .inp files---------------------------------------------------------------------------------------------------------------------------
lstTempList = []

for (path, dir, files) in os.walk('./'):
    for filename in files:
		lstext = os.path.splitext(filename)[-1]
		if lstext == '.PYN':
			lstTempList.append(filename + '\n')
			
filefile = open('filelist.txt', 'w')
filefile.writelines(lstTempList)
'''

for (path, dir, files) in os.walk('./'):
    for filename in files:
		lstext = os.path.splitext(filename)[-1]
		if lstext == '.PYN':
			InpFileList = open(filename)
			lstInpFileList = InpFileList.readlines()
			if lstInpFileList[2] == '*MAT, NAME=' + os.path.splitext(filename)[0] + '\n':
				Rev = os.path.splitext(filename)[0]
				test = Rev.split('_')[0] + '_' + Rev.split('_')[1]
				lstInpFileList[2] = '*MAT, NAME=' + test + '\n'
#				lstInpFileList.insert(2, '*MAT, NAME=' + test + '\n')
#				print lstInpFileList
#				NewFile = open(filename, 'w')
#				NewFile.writelines(lstInpFileList)
				NewFile = open(filename, 'w')
				NewFile.writelines(lstInpFileList)
'''