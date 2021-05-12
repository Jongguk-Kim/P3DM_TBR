# -*- coding: utf-8 -*-

import os, sys, glob, math, json, shutil, time, string, struct, CheckExecution
from math import *

def deleteBlank(strIsBlank):
	return ''.join(strIsBlank.split())

def createInpFile(path, strInpLine, AnalysisConditionNo, lstSnsInfo):
	if lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D101' \
		or lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D102' \
		or lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D103' \
		or lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D104' \
		or lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D105':
		fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '.inp'
		fileNewInp = open(fileName, 'wb')
		fileNewInp.write(strInpLine)
		fileNewInp.close()
	elif lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D201':
		if AnalysisConditionNo < 9:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-IF00' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
		else:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-IF0' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
	elif lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D202':
		if AnalysisConditionNo < 9:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-DP00' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
		else:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-DP0' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
	elif lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D203':
		if AnalysisConditionNo < 9:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-FM00' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
		else:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-FM0' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
	elif lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2] == 'D204':
		if AnalysisConditionNo < 9:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-WS00' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()
		else:
			fileName = path + '/' + str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-WS0' + str(AnalysisConditionNo + 1) + '.inp'
			fileNewInp = open(fileName, 'wb')
			fileNewInp.write(strInpLine)
			fileNewInp.close()

def createSeqDir(IndivName, i):
	print IndivName, ',', i
	IndivSimName= str(lstSnsInfo["AnalysisInformation"]["SimulationCode"][i]["Task"])
	inpName = str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-' + IndivSimName + '.inp'
	os.makedirs(IndivSimName)
	shutil.copy(strJobDir + '/' + inpName, IndivSimName + '/' + inpName)
	print 'Dir and Inp File Check', IndivSimName, inpName

def ModifyCordName(strFECordName):
	firstSpellingTextileCord = ['A','N66','DSP','HDSP','R']
	SplitCordName = strFECordName.split('+')
	CordName      = ''
	i = 0
	while i < len(SplitCordName):
		DetailedCordName = SplitCordName[i].split(' ')
		if DetailedCordName[0] in firstSpellingTextileCord:
			if DetailedCordName[2] == '(28T)':
				CordName = DetailedCordName[0] + '(' + DetailedCordName[1] + ')' + DetailedCordName[2]
			else:
				CordName = DetailedCordName[0] + '(' + DetailedCordName[1] + ')'
		else:
			for strDetailedCordName in DetailedCordName:
				CordName = CordName + strDetailedCordName
		if len(SplitCordName) > 1 and i < len(SplitCordName)-1: 
			CordName = CordName + '+'
		i = i + 1
	return CordName	

def SearchCordDB(strMatCode, strCompound, fltEPI):
	fileCordName = open('/home/fiper/ISLM_MAT/CordDB_SLM_PCI_v2.txt')
	lstCordNameTempLines = fileCordName.readlines()
	CordNamePos = -1
	for lstCordNameTempLine in lstCordNameTempLines:
		lstCordNameTempLine = lstCordNameTempLine.rstrip()
		if CordNamePos == 1:
			if lstCordNameTempLine != '':
				lstCordNameTempLineArray =  lstCordNameTempLine.split(',')
				if strMatCode == 'ABP219A':
					strMatCode = 'ABP218A'
				if strMatCode == 'ABP331A':
					strMatCode = 'ABP330A'
#				if strMatCode == 'ABN343A':
#					strMatCode = 'ABM301A'
				if lstCordNameTempLineArray[1].strip() == strMatCode:
					if lstCordNameTempLineArray[2].strip() == strCompound:
						if math.fabs(float(lstCordNameTempLineArray[3].strip())-fltEPI)<1.0E-9:
							return lstCordNameTempLineArray[0].strip()
		if lstCordNameTempLine == '*OLD_SPEC_CORD_NAME':
			CordNamePos = 1
	return "No Mat!"

def ChangeCompd(MatType):
	CompdList = [["P60","P01"],["Z27","P39"],["Y45","P40"],["Z45","P44"],["Y57","P57"],["P94","P57"],["P71","P90"],["P72","P95"],["P79","P50"],["T93","T38"],\
				["Y01","P07"],["Y05","P05"],["Y10","P10"],["Y13","P13"],["Y17","P51"],["Z17","P51"],["Y51","P51"],["Y19","P19"],["Y23","S23"],["Y38","P38"],\
				["Y43","P43"],["P21","P56"],["Y56","P56"],["Y81","P81"],["Z48","C48"],["Z69","H69"],["Z73","U73"],["Y76","P53"],["Y94","P58"],["Y27","P19"],\
				["P32","Z12"],["P62","P12"],["Y12","P12"],["Y09","P16"],["Y16","P16"],["P82","Z24"],["P46","P43X"],["P21","P27X"],["Y34_LAB","P34_LAB"],["Y83_LAB","P83_LAB"],["Z75_LAB","T77_LAB"]]
	i = 0
	while i < len(lstSnsInfo["ElsetMaterialInfo"][MatType]):
		j = 0
		while j < len(CompdList):
			if lstSnsInfo["ElsetMaterialInfo"][MatType][i]["Compound"] in CompdList[j][0]:
				lstSnsInfo["ElsetMaterialInfo"][MatType][i]["Compound"] = CompdList[j][1]
			j = j + 1
		i = i + 1

##############################################################################################
###############################   PCI   ######################################################
##############################################################################################
def BDWidthforPCI():
	filename = 'bead.tmp'
	BDWidthfile = open(filename, 'r')
	readBDWidth = BDWidthfile.readlines()
	return readBDWidth[0].strip()

def checkCCT():
	strJobDir = os.getcwd()
	CUTEInpFileName = strJobDir.split('/')[-2] + '.inp'
	ReadCUTEInpFile = open(CUTEInpFileName, 'r')
	CUTEInpFileLine = ReadCUTEInpFile.readlines()
	
#	try:
#		if '*ELSET, ELSET=CCT\r\n' in CUTEInpFileLine:
#			CCT = 'OK'
#		else:
#			CCT = 'NG'
#	except:
#		if '*ELSET, ELSET=CCT\n' in CUTEInpFileLine:
#			CCT = 'OK'
#		else:
#			CCT = 'NG'
			
	if '*ELSET, ELSET=CCT\n' in CUTEInpFileLine:
		CCT = 'OK'
	elif '*ELSET, ELSET=CCT\r\n' in CUTEInpFileLine:
		CCT = 'OK'
	else:
		CCT = 'NG'

	return CCT
	
class ErrorCheck:
	def VirtualTireParametersErrorCheck(self):
		VTError = []
		self.VTParam = lstSnsInfo["VirtualTireParameters"]
		for self.VTkey in self.VTParam.keys():
			if self.VTkey == "BeadSetDistance":
				if float(self.VTParam[self.VTkey]) < 1 or self.VTParam[self.VTkey] == '':
					VTError.append('!!!BeadSetDistance was not defined.!!!\n')
			if "BeadSetDistance" not in self.VTParam:
				VTError.append('!!!BeadSetDistance was not defined.!!!\n')
			if self.VTkey == "BeltLiftRatio":
				try:
					if float(self.VTParam[self.VTkey]) < 1.0 and float(self.VTParam[self.VTkey]) >= 1.1:
						VTError.append('!!!BeltLiftRatio was defined incorrectly.!!! value : ' + str(self.VTParam[self.VTkey]) + '\n')
				except:
					VTError.append('!!!BeltLiftRatio was defined incorrectly.!!! value : ' + str(self.VTParam[self.VTkey]) + '\n')
		return VTError
	def AnalysisInformationErrorCheck(self):
		AIError = []
		self.NumCase = len(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"])
		self.SimType = lstSnsInfo["AnalysisInformation"]["SimulationCode"].split('-')[-2]
		i = 0
		while i < self.NumCase:
			self.AIParam = lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][i]
			for self.AIkey in self.AIParam.keys():
				if self.AIkey == "PCIType":
					if self.AIParam[self.AIkey] == '':
						AIError.append('!!!PCIType was not defined.!!!\n')
					elif self.AIParam[self.AIkey] == 'NO':
						if self.AIkey == "PCIPressure":
							if float(self.AIParam[self.AIkey]) > 0 or self.AIParam[self.AIkey] == '':
								AIError.append('!!!The PCI pressure is defined incorrectly.!!!\n')
#					cInpRimDescription = InpRimDescription()
#					print cInpRimDescription.createRimDescription(0, lstSnsInfo)
							if self.AIkey == "PCIRimWidth":
								if float(self.AIParam[self.AIkey]) > 0 or self.AIParam[self.AIkey] == '':
									AIError.append('!!!The PCIRimWidth is defined incorrectly.!!!\n')
				if self.AIkey == "RimWidth":
					if float(self.AIParam[self.AIkey]) < 2.5 or float(self.AIParam[self.AIkey]) > 18.75 or self.AIParam[self.AIkey] == '':
						AIError.append('!!!The RimWidth is defined incorrectly.!!!\n')
#				if self.AIkey == "Pressure":
#					if float(self.AIParam[self.AIkey]) < 0.5 or float(self.AIParam[self.AIkey]) > 15 or self.AIParam[self.AIkey] == '':
#						AIError.append('!!!The pressure is defined incorrectly.!!!\n')
				if self.AIkey == "Load":
#					if self.SimType == 'D103':
#						if float(self.AIParam[self.AIkey]) > 0 or self.AIParam[self.AIkey] == '':
#							AIError.append('!!!The load is defined incorrectly.!!!\n')
					if self.SimType == 'D101' or self.SimType == 'D102' or self.SimType == 'D104' or self.SimType == 'D203' or self.SimType == 'D204':
						if float(self.AIParam[self.AIkey]) == 0 or self.AIParam[self.AIkey] == '':
							AIError.append('!!!The load is defined incorrectly.!!!\n')
				if self.AIkey == "CamberAngle":
					if self.AIParam[self.AIkey] == '':
						AIError.append('!!!The CamberAngle is defined incorrectly.!!!\n')
				if self.AIkey == "SlipAngle":
					if self.AIParam[self.AIkey] == '':
						AIError.append('!!!The SlipAngle is defined incorrectly.!!!\n')
				if self.AIkey == "Velocity":
					if self.AIParam[self.AIkey] == '':
						AIError.append('!!!The Velocity is defined incorrectly.!!!\n')
			i = i + 1
		return AIError
	def ElsetMaterialInfoErrorCheck(self):
		EMError = []
		self.EMParam = lstSnsInfo["ElsetMaterialInfo"]
		for self.EMkey in self.EMParam.keys():
			if self.EMkey == "Calendered":
				for i in range(len(self.EMParam[self.EMkey])):
					try:
						if type(float(self.EMParam[self.EMkey][i]['Angle'])) != float:
							EMError.append('!!!CordAngle was defined incorrectly.!!! value : ' + str(self.EMParam[self.EMkey][i]['Angle']) + '\n')
					except:
						EMError.append('!!!CordAngle was defined incorrectly.!!! value : ' + str(self.EMParam[self.EMkey][i]['Angle']) + '\n')
		return EMError
##############################################################################################
###############################   PCI   ######################################################
##############################################################################################

class InpMaterial:
	def createMaterialInp(self, AnalysisConditionNo, lstSnsInfo):
		self.lstCompInpLines = []
		self.lstCompLocLines = []
		self.lstFEComp       = []
		self.lstFECord       = []
		self.lstCompInpLines.append('*****************************************************************************************************************************\n')
#		self.lstCompInpLines.append('*TREAD_MIN_HVSCALE_FACTOR(0~1)=0.20\n')
		self.lstCompInpLines.append('*SOLID_SECTION, (SOL, MAT)\n')
		self.lstCompLocLines.append('*****************************************************************************************************************************\n')
		self.strlstSnsInfo = lstSnsInfo["AnalysisInformation"]["SimulationCode"]
		self.strlstSnsInfo = self.strlstSnsInfo.split('-')[-2]
		
		read2dinp = open(str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"])+'-'+str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"])+'.inp', 'r')
		inp2dfile = read2dinp.readlines()
		read2dinp.close()
		
		#WhetherCompdofJFCcheck = 1
		for self.lstCompMaterial in lstSnsInfo["ElsetMaterialInfo"]["Mixing"]:
			if self.lstCompMaterial["Compound"] in self.lstFEComp:
				pass
			else:
				self.lstFEComp.append(self.lstCompMaterial["Compound"])
				self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCompMaterial["Compound"] + '.PYN\n')
			if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D204':
				if "Multiplier" not in self.lstCompMaterial:
					if self.lstCompMaterial["Elset"] == 'TRW':
						if '*ELSET, ELSET=TRW\n' in inp2dfile or '*ELSET, ELSET=TRW\r\n' in inp2dfile:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, 1.0\n')
						else:
							pass
					else:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, 1.0\n')
				else:
					if self.lstCompMaterial["Elset"] == 'TRW':
						if '*ELSET, ELSET=TRW\n' in inp2dfile or '*ELSET, ELSET=TRW\r\n' in inp2dfile:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						else:
							pass
					else:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
			elif self.strlstSnsInfo == 'D203': 
				if 'CTB' in self.lstCompMaterial["Elset"]:
					if "Multiplier" not in self.lstCompMaterial:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, 1.0\n')
					else:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
				else:
					if self.lstCompMaterial["Elset"] == 'TRW':
						if '*ELSET, ELSET=TRW\n' in inp2dfile or '*ELSET, ELSET=TRW\r\n' in inp2dfile:
							if "Multiplier" not in self.lstCompMaterial:
								self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, 1.0\n')
							else:
								self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						else:
							pass
					else:
						if "Multiplier" not in self.lstCompMaterial:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
			else:
				if "Multiplier" not in self.lstCompMaterial:
					if self.lstCompMaterial["Elset"] == 'TRW':
						if '*ELSET, ELSET=TRW\n' in inp2dfile or '*ELSET, ELSET=TRW\r\n' in inp2dfile:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							pass
					else:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, 1.0\n')
				else:
					if self.lstCompMaterial["Elset"] == 'TRW':
						if '*ELSET, ELSET=TRW\n' in inp2dfile or '*ELSET, ELSET=TRW\r\n' in inp2dfile:
							self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						else:
							pass
					else:
						self.lstCompInpLines.append('{0:>3}'.format(self.lstCompMaterial["Elset"]) + ',      ' + self.lstCompMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
		
		for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
			if 'C01' in self.lstCordMaterial["Elset"]:
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if checkCCT() == 'OK':
						if "Multiplier" not in self.lstCompMaterial:
							self.lstCompInpLines.append('{0:>3}'.format('CCT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
						else:
							self.lstCompInpLines.append('{0:>3}'.format('CCT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
					if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
						self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
				else:
					if checkCCT() == 'OK':
						if "Multiplier" not in self.lstCompMaterial:
							self.lstCompInpLines.append('{0:>3}'.format('CCT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							self.lstCompInpLines.append('{0:>3}'.format('CCT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'C02' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'C03' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'CH1' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')

			if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "PCR" or lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
				if 'BT2' in self.lstCordMaterial["Elset"]:
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						if "Multiplier" not in self.lstCompMaterial:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
						else:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
							self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
					else:
						if "Multiplier" not in self.lstCompMaterial:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
							self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
				if 'BT1' in self.lstCordMaterial["Elset"]:
					if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
						self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			else:
				if 'BT1' in self.lstCordMaterial["Elset"]:
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						if "Multiplier" not in self.lstCompMaterial:
							self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
						else:
							self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
					else:
						if "Multiplier" not in self.lstCompMaterial:
							self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
						self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
				if 'BT2' in self.lstCordMaterial["Elset"]:
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
							self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
						if "Multiplier" not in self.lstCompMaterial:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
						else:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
					else:
						if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
							self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
						if "Multiplier" not in self.lstCompMaterial:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
						else:
							if '{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
								self.lstCompInpLines.append('{0:>3}'.format('BTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')

			if 'BDC' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'SPC' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')

			if 'RFM' in self.lstCordMaterial["Elset"] or 'SRFM' in self.lstCordMaterial["Elset"] or 'PK1' in self.lstCordMaterial["Elset"] or 'PK2' in self.lstCordMaterial["Elset"] or 'FLI' in self.lstCordMaterial["Elset"]:
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if "Multiplier" not in self.lstCompMaterial:
						self.lstCompInpLines.append('{0:>3}'.format('SRTT') + ',     ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
					else:
						self.lstCompInpLines.append('{0:>3}'.format('SRTT') + ',     ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
				else:
					if "Multiplier" not in self.lstCompMaterial:
						self.lstCompInpLines.append('{0:>3}'.format('SRTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
					else:
						self.lstCompInpLines.append('{0:>3}'.format('SRTT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			elif 'CH2' in self.lstCordMaterial["Elset"]:
				self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'JFC1' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'JEC1' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
			if 'JCC1' in self.lstCordMaterial["Elset"]:
				if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
					self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
		
		if '*ELSET, ELSET=JBT\n' in inp2dfile or '*ELSET, ELSET=JBT\r\n' in inp2dfile:
			if "JLCType" in lstSnsInfo["VirtualTireParameters"]:
				if lstSnsInfo["VirtualTireParameters"]["JLCType"] != "":
					for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
						if 'JFC1' in self.lstCordMaterial["Elset"] or 'JEC1' in self.lstCordMaterial["Elset"] or 'JCC1' in self.lstCordMaterial["Elset"]:
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								if "Multiplier" not in self.lstCompMaterial:
									if '{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n' not in self.lstCompInpLines:
										self.lstCompInpLines.append('{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, 1.0\n')
								else:
									if '{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
										self.lstCompInpLines.append('{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ', 120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
								if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
									self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
							else:
								if "Multiplier" not in self.lstCompMaterial:
									if '{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n' not in self.lstCompInpLines:
										self.lstCompInpLines.append('{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, 1.0\n')
								else:
									if '{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n' not in self.lstCompInpLines:
										self.lstCompInpLines.append('{0:>3}'.format('JBT') + ',      ' + self.lstCordMaterial["Compound"] + ',  120.0, ' + str(float(self.lstCompMaterial["Multiplier"])/100.0) + '\n')
								if '*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n' not in self.lstCompLocLines:
									self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/' + self.lstCordMaterial["Compound"] + '.PYN\n')
							break

		self.lstCompLocLines.append('*INCLUDE, INP=/home/fiper/ISLM_MAT/ABW121A.COR\n')
		self.lstCompLocLines.append('*****************************************************************************************************************************\n')
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
			self.lstCompInpLines.append('BD1,  ABW121A, 120.0, 1.0\n')
		else:
			self.lstCompInpLines.append('BD1,  ABW121A,  120.0, 1.0\n')
		self.lstCompInpLines.append('*BELT_THICKNESS_SUBTRACTION,\n')
		self.lstCompInpLines.append(' BETWEEN_BELTS, 4.61E-04\n')
		self.lstCordInpLines = []
		self.lstCordInpLines.append('*CORD_FILE=/home/fiper/ISLM_MAT/CordDB_SLM_PCI_v2.txt\n')
##############################################################################################
###############################   PCI   ######################################################
##############################################################################################
		BDWidth               = BDWidthforPCI()
		self.BSD              = str(float(lstSnsInfo["VirtualTireParameters"]["BeadSetDistance"]))
		self.CarcassPeriphery = str(float(lstSnsInfo["VirtualTireParameters"]["CarcassPeriphery"]))
		self.InnerPeriphery   = str((lstSnsInfo["VirtualTireParameters"]["InnerPeriphery"]).split(' '))
		self.PCIRimWidth      = str(float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["PCIRimWidth"]))
		self.PCIPressure      = str(float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["PCIPressure"]))
		self.PCIType          = lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["PCIType"]
		self.LayoutType       = lstSnsInfo["VirtualTireBasicInfo"]["LayoutType"]

		if self.LayoutType == 'In-mold':
			if self.PCIType == 'YES':
				self.PCIType = 0
			else:
				self.PCIType = 1
				self.PCIPressure = 0
		else:
			self.PCIType = 1
			self.PCIPressure = 0

		if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
			self.lstCordInpLines.append('*IN_MOLDING_PCI_INFO, TYPE=' + str(self.PCIType) + ' ,LOWCURE=1, BSD=' + str(self.BSD) + ', PCIRIMW=' + str(self.PCIRimWidth) + ', BDWIDTH=' + str(BDWidth) + ', PCIPRS=' + str(self.PCIPressure) + '\n')
		else:
			self.lstCordInpLines.append('*IN_MOLDING_PCI_INFO, TYPE=' + str(self.PCIType) + ' ,LOWCURE=0, BSD=' + str(self.BSD) + ', PCIRIMW=' + str(self.PCIRimWidth) + ', BDWIDTH=' + str(BDWidth) + ', PCIPRS=' + str(self.PCIPressure) + '\n')
##############################################################################################
###############################   PCI   ######################################################
##############################################################################################
		self.lstCordInpLines.append('*REBAR_SECTION\n')
		self.moldOD          = float(lstSnsInfo["VirtualTireParameters"]["OverallDiameter"])/1000.0
		if ';' in list(lstSnsInfo["VirtualTireParameters"]["MainGrooveDepth"]):
			self.mainGrooveDepth = float(lstSnsInfo["VirtualTireParameters"]["MainGrooveDepth"].split(';')[0])/1000.0
		else:
			self.mainGrooveDepth = float(lstSnsInfo["VirtualTireParameters"]["MainGrooveDepth"])/1000.0
		if ';' in list(lstSnsInfo["VirtualTireParameters"]["UnderTreadGauge"]):
			self.underTreadGauge = float(lstSnsInfo["VirtualTireParameters"]["UnderTreadGauge"].split(';')[0])/1000.0
		else:
			self.underTreadGauge = float(lstSnsInfo["VirtualTireParameters"]["UnderTreadGauge"])/1000.0
		self.beltLiftRatio   = float(lstSnsInfo["VirtualTireParameters"]["BeltLiftRatio"])
		self.totbeltGauge    = 0.0
		self.totreinBeltGauge= 0.0
		self.beltDrumDia     = 0.0
		for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
			if 'JFC1' in self.lstCordMaterial["Elset"]:
				self.totreinBeltGauge = self.totreinBeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'JFC2' in self.lstCordMaterial["Elset"]:
				self.totreinBeltGauge = self.totreinBeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'JCC1' in self.lstCordMaterial["Elset"]:
				self.totreinBeltGauge = self.totreinBeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'BT1' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'BT2' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'BT3' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'BT4' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'BDC' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'SPC' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'CH1' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
			elif 'CH2' in self.lstCordMaterial["Elset"]:
				self.totbeltGauge     = self.totbeltGauge + float(self.lstCordMaterial["Gauge"])/1000
		self.beltDrumDia = ( self.moldOD - 2*(self.mainGrooveDepth+self.underTreadGauge+0.9*self.totreinBeltGauge)-1.25*self.totbeltGauge ) / self.beltLiftRatio - self.totbeltGauge
		self.beltDrumRadius = self.beltDrumDia/2*1000
		self.greenbelt1Angle = 0.0;	self.greenbelt1Width = 0.0
		self.greenbelt2Angle = 0.0;	self.greenbelt2Width = 0.0
		self.greenbelt3Angle = 0.0;	self.greenbelt3Width = 0.0
		self.greenbelt4Angle = 0.0;	self.greenbelt4Width = 0.0
		
		self.curedbelt1Angle = 0.0;	self.curedbelt1Width = 0.0
		self.curedbelt2Angle = 0.0;	self.curedbelt2Width = 0.0
		self.curedbelt3Angle = 0.0;	self.curedbelt3Width = 0.0
		self.curedbelt4Angle = 0.0;	self.curedbelt4Width = 0.0
		
		self.greenbeltDia    = 0.0
		self.greenreinbeltDia= 0.0
		
		self.beltfactor      = 0.0
		
		for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
			if 'BT1' in self.lstCordMaterial["Elset"]:
				if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
					self.beltfactor = 1.0
				else:
					if self.lstCordMaterial["Angle"] == 24.0: self.beltfactor = 1.022
					elif self.lstCordMaterial["Angle"] > 24.0 and self.lstCordMaterial["Angle"] < 27.0: self.beltfactor = 1.020
					elif self.lstCordMaterial["Angle"] == 27.0: self.beltfactor = 1.019
					elif self.lstCordMaterial["Angle"] > 27.0 and self.lstCordMaterial["Angle"] < 30.0: self.beltfactor = 1.018
					elif self.lstCordMaterial["Angle"] == 30.0: self.beltfactor = 1.017
					else: self.beltfactor = 1.016
				self.greenbeltDia    = self.beltDrumDia+float(self.lstCordMaterial["Gauge"])/1000
				self.greenbelt1Dia   = self.greenbeltDia*math.pi
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D204':
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "PCR":
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
					elif lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
				else:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "PCR":
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
					elif lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT1,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.beltDrumRadius) + '\n')
			elif 'BT2' in self.lstCordMaterial["Elset"]:
				if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
					self.beltfactor = 1.015
				else:
					if self.lstCordMaterial["Angle"] == 24.0: self.beltfactor = 1.022
					elif self.lstCordMaterial["Angle"] > 24.0 and self.lstCordMaterial["Angle"] < 27.0: self.beltfactor = 1.020
					elif self.lstCordMaterial["Angle"] == 27.0: self.beltfactor = 1.019
					elif self.lstCordMaterial["Angle"] > 27.0 and self.lstCordMaterial["Angle"] < 30.0: self.beltfactor = 1.018
					elif self.lstCordMaterial["Angle"] == 30.0: self.beltfactor = 1.017
					else: self.beltfactor = 1.016
					self.lstCordMaterial["Angle"] = self.lstCordMaterial["Angle"]
				self.greenbeltDia    = self.greenbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.greenbelt2Dia   = self.greenbeltDia*math.pi
				self.belt2DrumDia    = self.beltDrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.belt2DrumRadius = self.belt2DrumDia/2*1000
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "PCR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
					elif lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
				else:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "PCR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
					elif lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'R' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT2,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt2DrumRadius) + '\n')
			elif 'BT3' in self.lstCordMaterial["Elset"]:
				if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
					self.beltfactor = 1.015
				self.greenbeltDia    = self.greenbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.greenbelt3Dia   = self.greenbeltDia*math.pi
				self.belt3DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.belt3DrumRadius = self.belt3DrumDia/2*1000
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
				else:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "LTR":
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
					else:
						if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append(' BT3,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt3DrumRadius) + '\n')
			elif 'BT4' in self.lstCordMaterial["Elset"]:
				if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
					self.beltfactor = 1.015
				self.greenbeltDia    = self.greenbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.greenbelt4Dia   = self.greenbeltDia*math.pi
				self.belt4DrumDia    = self.belt3DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
				self.belt4DrumRadius = self.belt4DrumDia/2*1000
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
						self.lstCordInpLines.append(' BT4,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt4DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append(' BT4,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt4DrumRadius) + '\n')
				else:
					if format(self.lstCordMaterial["Direction"]) == 'L' or format(self.lstCordMaterial["Direction"]) == '':
						self.lstCordInpLines.append(' BT4,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt4DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append(' BT4,' + '   BT,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '{0:0.4f}'.format(self.belt4DrumRadius) + '\n')
				
		self.greenreinbeltDia = self.greenbeltDia
		if "JLCType" in lstSnsInfo["VirtualTireParameters"]:
			if lstSnsInfo["VirtualTireParameters"]["JLCType"] == 'JF3':
				for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
					if 'JFC1' in self.lstCordMaterial["Elset"]:
						read2dinp = open(str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"])+'-'+str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"])+'.inp', 'r')
						inp2dfile = read2dinp.readlines()
						read2dinp.close()
						if '*ELSET, ELSET=OJFC1\n' in inp2dfile or '*ELSET, ELSET=OJFC1\r\n' in inp2dfile:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('OJFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
							else:
								self.lstCordInpLines.append('OJFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
						else:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
							else:
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
			elif lstSnsInfo["VirtualTireParameters"]["JLCType"] == 'JE3':
				for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
					if 'JEC1' in self.lstCordMaterial["Elset"]:
						read2dinp = open(str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"])+'-'+str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"])+'.inp', 'r')
						inp2dfile = read2dinp.readlines()
						read2dinp.close()
						if '*ELSET, ELSET=OJEC1\n' in inp2dfile or '*ELSET, ELSET=OJEC1\r\n' in inp2dfile:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('OJEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
							else:
								self.lstCordInpLines.append('OJEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
						else:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
							else:
								self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
			elif lstSnsInfo["VirtualTireParameters"]["JLCType"] == 'JF535':
				for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
					if 'JFC1' in self.lstCordMaterial["Elset"]:
						read2dinp = open(str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"])+'-'+str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"])+'.inp', 'r')
						inp2dfile = read2dinp.readlines()
						read2dinp.close()
						if '*ELSET, ELSET=OJFC1\n' in inp2dfile or '*ELSET, ELSET=OJFC1\r\n' in inp2dfile:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.reinbelt1DrumDiaO   = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.reinbelt1DrumRadiusO= self.reinbelt1DrumDiaO/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
								self.lstCordInpLines.append('OJFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadiusO) + '\n')
							else:
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
								self.lstCordInpLines.append('OJFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.6, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadiusO) + '\n')
						else:
							self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
							self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
							self.reinbelt1DrumDiaO   = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])*1.6/1000
							self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
							self.reinbelt1DrumRadiusO= self.reinbelt1DrumDiaO/2*1000
							self.cordGauge           = float(self.lstCordMaterial["Gauge"])
							self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
							self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
							if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
							else:
								self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
					elif 'JEC1' in self.lstCordMaterial["Elset"]:
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.reinbelt2DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius+self.cordGauge) + '\n')
						else:
							self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius+self.cordGauge) + '\n')
			else:
				for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
					if 'JFC1' in self.lstCordMaterial["Elset"]:
						self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
						self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
						self.cordGauge           = float(self.lstCordMaterial["Gauge"])
						self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
					elif 'JFC2' in self.lstCordMaterial["Elset"]:
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.reinbelt2DrumDia    = self.reinbelt1DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							self.lstCordInpLines.append('JFC2,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append('JFC2,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
					elif 'JEC1' in self.lstCordMaterial["Elset"]:
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.reinbelt2DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
					elif 'JCC1' in self.lstCordMaterial["Elset"]:
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.reinbelt2DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							self.lstCordInpLines.append('JCC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
						else:
							self.lstCordInpLines.append('JCC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
			for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
				if 'BDC' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append(' BDC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' BDC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'SPC' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append(' SPC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' SPC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'CH1' in self.lstCordMaterial["Elset"]:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'V' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
						else:
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'V' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
				elif 'CH2' in self.lstCordMaterial["Elset"]:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'A' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
						else:
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'A' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
				elif 'PK1' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' PK1,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' PK1,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'PK2' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' PK2,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' PK2,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'FLI' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' FLI,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' FLI,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
		else:
			for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
				if 'JFC1' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia    = self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia1   = self.greenreinbeltDia*math.pi
					self.reinbelt1DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.reinbelt1DrumRadius = self.reinbelt1DrumDia/2*1000
					self.cordGauge           = float(self.lstCordMaterial["Gauge"])
					self.cordName            = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode             = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append('JFC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt1DrumRadius) + '\n')
				elif 'JFC2' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.reinbelt2DrumDia    = self.reinbelt1DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append('JFC2,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append('JFC2,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
				elif 'JEC1' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.reinbelt2DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append('JEC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
				elif 'JCC1' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.reinbelt2DrumDia    = self.belt2DrumDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.reinbelt2DrumRadius = self.reinbelt2DrumDia/2*1000
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append('JCC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
					else:
						self.lstCordInpLines.append('JCC1,' + '   RB,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.reinbelt2DrumRadius) + '\n')
				elif 'BDC' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append(' BDC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' BDC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'SPC' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
						self.lstCordInpLines.append(' SPC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' SPC,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'CH1' in self.lstCordMaterial["Elset"]:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'V' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
						else:
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'V' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH1_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH1_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
				elif 'CH2' in self.lstCordMaterial["Elset"]:
					if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
						self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
						self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
						self.cordGauge       = float(self.lstCordMaterial["Gauge"])
						self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
						self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
						if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'A' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
						else:
							if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
								if format(self.lstCordMaterial["Direction"]) == 'A' or format(self.lstCordMaterial["Direction"]) == '':
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
								else:
									if list(self.MatCode)[1] == 'S':
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
									else:
										self.lstCordInpLines.append(' CH2_L,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + ' -' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
										self.lstCordInpLines.append(' CH2_R,' + ' NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(abs(float(self.lstCordMaterial["Angle"]))) + ', ' + '0.0' + '\n')
				elif 'PK1' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' PK1,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' PK1,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'PK2' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' PK2,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' PK2,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				elif 'FLI' in self.lstCordMaterial["Elset"]:
					self.greenreinbeltDia= self.greenreinbeltDia+2.0*float(self.lstCordMaterial["Gauge"])/1000
					self.greenreinbeltDia2= self.greenreinbeltDia*math.pi
					self.cordGauge       = float(self.lstCordMaterial["Gauge"])
					self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
					self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
					if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203':
						self.lstCordInpLines.append(' FLI,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
					else:
						self.lstCordInpLines.append(' FLI,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
			

		self.cdd = 0.0
		if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
			if lstSnsInfo["VirtualTireParameters"]["OverType"] == "Tread Over Side":
				self.lstCDD = [[15.0,440.],[16.0,460.],[17.5,529.4],[18.0,526.],[20.0,571.5],[22.0,640.],[22.5,660.4],[24.0,686.],[24.5,711.2]]
			else:
				self.lstCDD = [[16.0,377.2],[17.5,407.4],[19.5,458.4],[20.0,483.8],[22.5,528.4],[24.5,576.1]]
			i = 0
			Temp = 0;PrevDiff = 10
			self.ActualRD = round(float(lstSnsInfo["VirtualTireParameters"]["RimDiameter"])/25.4,1)
			while i < len(self.lstCDD)-1:
				self.RDDiff     = math.fabs(self.ActualRD - self.lstCDD[i][0])
				self.nextRDDiff = math.fabs(self.ActualRD - self.lstCDD[i+1][0])
				if self.RDDiff == 0:
					self.cdd = self.lstCDD[i][1]/1000.0
				else:
					if self.RDDiff > 0 and self.RDDiff <= PrevDiff:
						self.cdd = self.lstCDD[i][1]/1000.0
						PrevDiff = self.RDDiff
				i = i + 1
		else:
			self.lstCDD = [[12.,337.],[13.,310.],[14.,335.],[15.,360.],[16.,385.],[17.,417.],[18.,442.],[19.,465.],[20.,490.],[21.,516.],[22.,542.],[23.,567.],[24.,592.],[26.,643.],[28.,694.]]
			for self.lstRimInch in self.lstCDD:
				tmplstRimInch = round(float(lstSnsInfo["VirtualTireParameters"]["RimDiameter"])/25.4,0)
				if tmplstRimInch == self.lstRimInch[0]:
					self.cdd             = self.lstRimInch[1]/1000.0
				
		for self.lstCordMaterial in lstSnsInfo["ElsetMaterialInfo"]["Calendered"]:
			if 'C01' in self.lstCordMaterial["Elset"]:
				self.cdd             = self.cdd + float(self.lstCordMaterial["Gauge"])/1000
				self.cdd1            = self.cdd*math.pi
				self.c1dr            = self.cdd/2*1000
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					if list(self.MatCode)[1] == 'S':
						self.lstCordInpLines.append(' C01,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c1dr) + '\n')
					else:
						self.lstCordInpLines.append(' C01,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c1dr) + '\n')
				else:
					if list(self.MatCode)[1] == 'S':
						self.lstCordInpLines.append(' C01,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c1dr) + '\n')
					else:
						self.lstCordInpLines.append(' C01,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c1dr) + '\n')
			elif 'C02' in self.lstCordMaterial["Elset"]:
				self.cdd             = self.cdd + 2*float(self.lstCordMaterial["Gauge"])/1000
				self.cdd2            = self.cdd*math.pi
				self.c2dr            = self.c1dr + float(self.lstCordMaterial["Gauge"])
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					self.lstCordInpLines.append(' C02,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c2dr) + '\n')
				else:
					self.lstCordInpLines.append(' C02,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c2dr) + '\n')
			elif 'C03' in self.lstCordMaterial["Elset"]:
				self.cdd             = self.cdd + 2*float(self.lstCordMaterial["Gauge"])/1000
				self.cdd3            = self.cdd*math.pi
				self.c3dr            = self.c2dr + float(self.lstCordMaterial["Gauge"])
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					self.lstCordInpLines.append(' C03,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c3dr) + '\n')
				else:
					self.lstCordInpLines.append(' C03,' + '   CC,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 0,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '{0:0.4f}'.format(self.c3dr) + '\n')
			elif 'SRFM' in self.lstCordMaterial["Elset"]:
				self.cdd             = self.cdd + 2*float(self.lstCordMaterial["Gauge"])/1000
				self.cdd4            = self.cdd*math.pi
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					self.lstCordInpLines.append('SRFM,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				else:
					self.lstCordInpLines.append('SRFM,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
			elif 'RFM' in self.lstCordMaterial["Elset"]:
				self.cdd             = self.cdd + 2*float(self.lstCordMaterial["Gauge"])/1000
				self.cdd4            = self.cdd*math.pi
				self.cordGauge       = float(self.lstCordMaterial["Gauge"])
				self.cordName        = ModifyCordName(self.lstCordMaterial["RawCode"])
				self.MatCode         = SearchCordDB(self.lstCordMaterial["MatCode"], self.lstCordMaterial["Compound"], float(self.lstCordMaterial["EPI"]))
				if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
					self.lstCordInpLines.append(' RFM,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				else:
					self.lstCordInpLines.append(' RFM,' + '   NA,' + '{0:>8}'.format(self.MatCode) + ', 120.0, 1.0, 1,' + '  ' + str(float(self.lstCordMaterial["Angle"])) + ', ' + '0.0' + '\n')
				
class InpRimDescription:
	def createRimDescription(self, AnalysisConditionNo, lstSnsInfo):
		self.lstInpLines = []
		self.rw          = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["RimWidth"])
		self.rd          = float(lstSnsInfo["VirtualTireParameters"]["RimDiameter"])
		self.rwDB        = []
		self.rdDB        = []
		if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
			if lstSnsInfo["VirtualTireParameters"]["BeadringType"] == "Tubeless":
				self.rwDB = [[4.5, 114.3],[5.25,133.5],[6.0,152.5],[6.75,171.5],[7.5,190.5],[8.25,209.5],[9.0,228.5],[9.75,247.5],[10.5,266.7],[11.0,279.4],[11.25,285.8],\
							[11.5,291.1],[11.75,298.5],[12.25,311.0],[12.5,317.5],[13.0,330.0],[13.25,336.6],[13.75,349.25],[14.0,355.5],[14.25,362.0],[14.75,374.7],[15.0,381.0],\
							[15.25,387.4],[15.75,400.1],[16.0,406.5],[16.25,412.8],[16.75,425.5],[17.0,432.0],[17.25,438.2],[17.75,450.85],[18.0,457.0],[18.75,476.25]]
				self.rdDB = [[17.5,444.5],[19.5,495.3],[22.5,571.5],[24.5,622.3],[26.5,673.1]]
			else:
				self.rwDB = [[4.5,114.3],[5.0,127.0],[5.5,139.5],[6.0,152.5],[6.5,165.0],[7.0,178.0],[7.5,190.5],[8.0,203.0],[8.5,216.0],[9.0,228.5],[9.5, 241.3],[10.0,254.0],[10.5,266.7],[11.0,279.4],[11.5,292.1],[12.0,304.8],[12.5,317.5],[13.0,330.2],[13.5,342.9],[14.0,355.6],[14.5,368.3]]
				self.rdDB = [[15.0,387.4],[18.0,461.8],[20.0,514.4],[24.0,616.0]]
		else:
			self.rwDB = [[2.5,63.5],[3.0,76.0],[3.5,89.0],[4.0,101.5],[4.5,114.5],[5.0,127.0],[5.5,139.5],[6.0,152.5],[6.5,165.0],[7.0,178.0],[7.5,190.5],[8.0,203.0],[8.5,216.0],\
						 [9.0,228.5],[9.5,241.5],[10.0,254.0],[10.5,266.5],[11.0,279.5],[11.5,292.0],[12.0,305.0],[12.5,317.5],[13.0,330.0],[13.5,343.0],[14.0,355.5]]
			self.rdDB = [[10.0,253.2],[12.0,304.0],[13.0,329.4],[14.0,354.8],[15.0,380.2],[16.0,405.6],[17.0,436.6],[18.0,462.0],[19.0,487.4],[20.0,512.8],[21.0,538.2],[22.0,563.6],[23.0,589.0],[24.0,614.4],[25.0,639.8],[26.0,665.2],[28.0,716.0],[30.0,766.8]]
		for self.rd_data in self.rdDB:

			tmplstRimInch = round(float(lstSnsInfo["VirtualTireParameters"]["RimDiameter"])/25.4,0)
			if self.rd_data[0] == tmplstRimInch:
				self.rd = self.rd_data[1]
		for self.rw_data in self.rwDB:
			if self.rw_data[0] == float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["RimWidth"]):
				self.rw = self.rw_data[1]
		if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
			if lstSnsInfo["VirtualTireParameters"]["BeadringType"] == "Tubeless":
				self.lstInpLines.append('*RIM_GEOM         =  ' + str(self.rd/2.0) + ', ' + str(self.rw/2.0) + ', /home/fiper/ISLM_RIM/RIM_TB_TUBELESS.GEOM\n')
			else:
				self.lstInpLines.append('*RIM_GEOM         =  ' + str(self.rd/2.0) + ', ' + str(self.rw/2.0) + ', /home/fiper/ISLM_RIM/RIM_TBTUBE.GEOM\n')
		else:
			self.lstInpLines.append('*RIM_GEOM         =  ' + str(self.rd/2.0) + ', ' + str(self.rw/2.0) + ', /home/fiper/ISLM_RIM/RIM_PCLT.GEOM\n')
		self.lstInpLines.append('*RIM_OR_HUB_REAL_MASS =1.00   (RIM=1.0, LAT100=0.05, NPT=1.0)\n')
		self.lstInpLines.append('*****************************************************************************************************************************\n')
		self.lstInpLines.append('*SURFACES_FOR_CONTACT_AND_LOAD=XTRD1001, TIREBODY, PRESS, RIC_L, RIC_R        (TREAD, TBODY, PRESS, RICL, RICR FOR TIRE  )\n')
		
class InpCondDescription:
# D101 : Footshape, D102 : RR, D103 : Dimension, D104 : Dynamic FootShape
# D201 : Static Inflation, D202 : Dynamic Profile, D203 : Force & Moment, D204 : Wear Sensitivity
# D103 = D201, D101 = D204
	def createCondDescription(self, AnalysisConditionNo, lstSnsInfo):
		self.strlstSnsInfo = lstSnsInfo["AnalysisInformation"]["SimulationCode"]
		self.strlstSnsInfo = self.strlstSnsInfo.split('-')[-2]
		self.lstInpLines = []
		self.lstInpLines.append('*****************************************************************************************************************************\n')
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D204':  # Static Foot shape, Wear Sensitivity
			self.lstInpLines.append('*SIMULATION_TYPE  = 0       ( 0:TIRE, 1:LAT100, 2:NPT)\n')
			self.lstInpLines.append('*SIMULATION_TIME  = 0.08, 1.50, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
			self.lstInpLines.append('*OUTPUT_CONTROL   = 0.01, 0.02    ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			self.lstInpLines.append('*****************************************************************************************************************************\n')
			self.lstInpLines.append('*INFLATION_TIME               = 0.01, 0.015,  0.0 (First Inflation End, Section Inflation End, Tire Velocity(kph) for Dyn. Profile)\n')
			self.lstInpLines.append('*SELF_CONTACT_ACTIVATION      = 0, 0  (INNER CAVITY ON, OFF (1, 0:DEFAULT) , TREAD KERF ON, OFF (1, 0:DEFAULT))\n')
			self.lstInpLines.append('*TEMPERATURE_ANALYSIS         = 0, 0.04, 25.0, 25.0   (OFF:0, ON:1), IF ON, (T_COMPUTATION_START_TIME, AIR_T, ROAD_T)\n')
			self.lstInpLines.append('*TEMPERATURE_OUT_IN           = 0, ../TEMP/C100_NB08.TEMPER   !(0:NO_IN_OUT, 1:OUT_TEMP, 2:READ_TEMP), IF 2 READ IN FILENAME\n')
			self.lstInpLines.append('*PRESSURE_VARIANCE            = 0, 10.0, 0.1D0, 0.05D0  (FOR TEMPERATURE OFF:0, ON:1), ( PRS_V VARIANCE START TIME-IF .LT. 3RD TIME SET TO 3RD TIME), RIM_ADDED_WIDTH, RIM_ADDED_DEPTH)\n')
		elif self.strlstSnsInfo == 'D102' or self.strlstSnsInfo == 'D104' or self.strlstSnsInfo == 'D105':    # RR, Dynamic Foot shape, Standing Wave
			self.lstInpLines.append('*SIMULATION_TYPE  = 0       ( 0:TIRE, 1:LAT100, 2:NPT)\n')
			if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
				self.lstInpLines.append('*SIMULATION_TIME  = 0.35, 1.02, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
			else:
				self.lstInpLines.append('*SIMULATION_TIME  = 0.25, 1.02, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
			self.lstInpLines.append('*OUTPUT_CONTROL   = 0.01, 0.05    ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			self.lstInpLines.append('*****************************************************************************************************************************\n')
			self.lstInpLines.append('*INFLATION_TIME               = 0.01, 0.015,  0.0 (First Inflation End, Section Inflation End, Tire Velocity(kph) for Dyn. Profile)\n')
			self.lstInpLines.append('*SELF_CONTACT_ACTIVATION      = 0, 0  (INNER CAVITY ON, OFF (1, 0:DEFAULT) , TREAD KERF ON, OFF (1, 0:DEFAULT))\n')
			self.lstInpLines.append('*TEMPERATURE_ANALYSIS         = 1, 0.04, 25.0, 25.0   (OFF:0, ON:1), IF ON, (T_COMPUTATION_START_TIME, AIR_T, ROAD_T)\n')
			self.lstInpLines.append('*TEMPERATURE_OUT_IN           = 0, ../TEMP/C100_NB08.TEMPER   !(0:NO_IN_OUT, 1:OUT_TEMP, 2:READ_TEMP), IF 2 READ IN FILENAME\n')	#0?? or 1??
			self.lstInpLines.append('*PRESSURE_VARIANCE            = 1, 0.04, 0.1D0, 0.05D0  (FOR TEMPERATURE OFF:0, ON:1), ( PRS_V VARIANCE START TIME-IF .LT. 3RD TIME SET TO 3RD TIME), RIM_ADDED_WIDTH, RIM_ADDED_DEPTH)\n')
		elif self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201':  # dimension , Static Inflation
			self.lstInpLines.append('*SIMULATION_TYPE  = 0       ( 0:TIRE, 1:LAT100, 2:NPT)\n')
			self.lstInpLines.append('*SIMULATION_TIME  = 0.0, 1.50, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
			self.lstInpLines.append('*OUTPUT_CONTROL   = 0.005, 0.020   ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			self.lstInpLines.append('*****************************************************************************************************************************\n')
			self.lstInpLines.append('*INFLATION_TIME               = 0.01, 0.015,  0.0 (First Inflation End, Section Inflation End, Tire Velocity(kph) for Dyn. Profile)\n')
			self.lstInpLines.append('*SELF_CONTACT_ACTIVATION      = 0, 0  (INNER CAVITY ON, OFF (1, 0:DEFAULT) , TREAD KERF ON, OFF (1, 0:DEFAULT))\n')
			self.lstInpLines.append('*TEMPERATURE_ANALYSIS         = 0, 0.04, 25.0, 25.0   (OFF:0, ON:1), IF ON, (T_COMPUTATION_START_TIME, AIR_T, ROAD_T)\n')
			self.lstInpLines.append('*TEMPERATURE_OUT_IN           = 0, ../TEMP/C100_NB08.TEMPER   !(0:NO_IN_OUT, 1:OUT_TEMP, 2:READ_TEMP), IF 2 READ IN FILENAME\n')
			self.lstInpLines.append('*PRESSURE_VARIANCE            = 0, 10.0, 0.1D0, 0.05D0  (FOR TEMPERATURE OFF:0, ON:1), ( PRS_V VARIANCE START TIME-IF .LT. 3RD TIME SET TO 3RD TIME), RIM_ADDED_WIDTH, RIM_ADDED_DEPTH)\n')
		elif self.strlstSnsInfo == 'D202':  # Dynamic Profile
			self.lstInpLines.append('*SIMULATION_TYPE  = 0       ( 0:TIRE, 1:LAT100, 2:NPT)\n')
			try : 
				if float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"]) > 0.0: 
					self.lstInpLines.append('*SIMULATION_TIME  = 0.25, 1.02, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
					self.lstInpLines.append('*OUTPUT_CONTROL   = 0.02, 0.005    ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			except: 			
				self.lstInpLines.append('*SIMULATION_TIME  = 0.0, 1.50, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
				self.lstInpLines.append('*OUTPUT_CONTROL   = 0.002, 0.005    ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			self.lstInpLines.append('*****************************************************************************************************************************\n')

			self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
			self.lstInpLines.append('*INFLATION_TIME               = 0.01, 0.015, ' + format(self.Velocity, '.1f') + ' (First Inflation End, Section Inflation End, Tire Velocity(kph) for Dyn. Profile)\n')
			self.lstInpLines.append('*SELF_CONTACT_ACTIVATION      = 0, 0  (INNER CAVITY ON, OFF (1, 0:DEFAULT) , TREAD KERF ON, OFF (1, 0:DEFAULT))\n')
			self.lstInpLines.append('*TEMPERATURE_ANALYSIS         = 0, 0.04, 25.0, 25.0   (OFF:0, ON:1), IF ON, (T_COMPUTATION_START_TIME, AIR_T, ROAD_T)\n')
			self.lstInpLines.append('*TEMPERATURE_OUT_IN           = 0, ../TEMP/C100_NB08.TEMPER   !(0:NO_IN_OUT, 1:OUT_TEMP, 2:READ_TEMP), IF 2 READ IN FILENAME\n')
			self.lstInpLines.append('*PRESSURE_VARIANCE            = 0, 10.0, 0.1D0, 0.05D0  (FOR TEMPERATURE OFF:0, ON:1), ( PRS_V VARIANCE START TIME-IF .LT. 3RD TIME SET TO 3RD TIME), RIM_ADDED_WIDTH, RIM_ADDED_DEPTH)\n')
		elif self.strlstSnsInfo == 'D203':    # Force & Moment
			self.lstInpLines.append('*SIMULATION_TYPE  = 0       ( 0:TIRE, 1:LAT100, 2:NPT)\n')
			self.lstInpLines.append('*SIMULATION_TIME  = 0.25, 1.02, 1.0 { PHYSICAL TIME, MASS_SCALE(>=1, DEFAULT=1.02), DT_RATIO( IF =1.0=>VARIABLE, IF < 1.0 => FIXED FOR FFT ) }\n')
			self.lstInpLines.append('*OUTPUT_CONTROL   = 0.01, 0.05    ( DEL_T FOR FRAME FRICVIEW OUTPUT, DEL_T FOR TIME HISTORY AVERAGING)\n')
			self.lstInpLines.append('*****************************************************************************************************************************\n')
			self.lstInpLines.append('*INFLATION_TIME               = 0.01, 0.015,  0.0 (First Inflation End, Section Inflation End, Tire Velocity(kph) for Dyn. Profile)\n')			
			self.lstInpLines.append('*SELF_CONTACT_ACTIVATION      = 0, 0  (INNER CAVITY ON, OFF (1, 0:DEFAULT) , TREAD KERF ON, OFF (1, 0:DEFAULT))\n')
			self.lstInpLines.append('*TEMPERATURE_ANALYSIS         = 0, 0.04, 25.0, 25.0   (OFF:0, ON:1), IF ON, (T_COMPUTATION_START_TIME, AIR_T, ROAD_T)\n')
			self.lstInpLines.append('*TEMPERATURE_OUT_IN           = 0, ../TEMP/C100_NB08.TEMPER   !(0:NO_IN_OUT, 1:OUT_TEMP, 2:READ_TEMP), IF 2 READ IN FILENAME\n')
			self.lstInpLines.append('*PRESSURE_VARIANCE            = 0, 10.0, 0.1D0, 0.05D0  (FOR TEMPERATURE OFF:0, ON:1), ( PRS_V VARIANCE START TIME-IF .LT. 3RD TIME SET TO 3RD TIME), RIM_ADDED_WIDTH, RIM_ADDED_DEPTH)\n')
		
		self.lstInpLines.append('*****************************************************************************************************************************\n')
		if lstSnsInfo["VirtualTireBasicInfo"]["ProductLine"] == "TBR":
			self.lstInpLines.append('*STIFFNESS        =  114.0, 38.0, 72.0  (KV, KL, KT)\n')
		else:
			self.lstInpLines.append('*STIFFNESS        =  24.6, 20.03, 30.0  (KV, KL, KT)\n')
		self.press       = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Pressure"])
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D102' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
			self.Load        = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"])
		else:
			self.Load        = 0
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D102' or self.strlstSnsInfo == 'D103':
			self.CamberAngle = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["CamberAngle"])
			self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
		elif self.strlstSnsInfo == 'D104':
			self.SlipAngle   = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["SlipAngle"])
			self.CamberAngle = 0
			self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
			self.Load        = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"])
		if self.strlstSnsInfo == 'D105':
			self.CamberAngle = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["CamberAngle"])
			self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
			self.Load        = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"])
		elif self.strlstSnsInfo == 'D201':
			self.CamberAngle = 0
			self.Velocity    = 0
		elif self.strlstSnsInfo == 'D202':
			self.CamberAngle = 0
			try: 			
				self.Load = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"])
				self.Velocity = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
			except:
				self.Velocity    = 0
		elif self.strlstSnsInfo == 'D203':
			self.SlipAngle   = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["SlipAngle"])
			self.CamberAngle = 0
			self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
		elif self.strlstSnsInfo == 'D204':
			self.SlipAngle   = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["SlipAngle"])
			self.CamberAngle = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["CamberAngle"])
			#self.Velocity    = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Velocity"])
			self.Velocity    = 60.0
		self.lstInpLines.append('*CONDITION_LOAD   =  ' + str(self.press) + ', '+ str(self.press) + ', '+ str(self.Load) + ', '+ str(self.Velocity) + '\n')
		if self.CamberAngle == 0:
			self.lstInpLines.append('*CAMBER_ANGLE     =  ' + str(self.CamberAngle) + '\n')
		else:
			self.lstInpLines.append('*CAMBER_ANGLE     =  ' + str(self.CamberAngle*-1) + '\n')
		#if self.strlstSnsInfo == 'D104' or self.strlstSnsInfo == 'D203':
		#	self.lstInpLines.append('*LATERAL_CONTROL  =  1, ' + str(self.SlipAngle) + '\n')
		#elif self.strlstSnsInfo == 'D204':
		#	self.Load        = float(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][AnalysisConditionNo]["Load"])
		#	if self.SlipAngle < 0:
		#		self.LateralLoad = round((0.1*cos(self.SlipAngle*(3.14/180))*9.81*self.Load),2)
		#		self.lstInpLines.append('*LATERAL_CONTROL  =  0, ' + str(self.LateralLoad) + '\n')
		#	elif self.SlipAngle > 0:
		#		self.LateralLoad = round((-0.1*cos(self.SlipAngle*(3.14/180))*9.81*self.Load),2)
		#		self.lstInpLines.append('*LATERAL_CONTROL  =  0, ' + str(self.LateralLoad) + '\n')
		#	else:
		#		self.lstInpLines.append('*LATERAL_CONTROL  =  1, 0.0\n')
		if self.strlstSnsInfo == 'D104' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
			self.lstInpLines.append('*LATERAL_CONTROL  =  1, ' + str(self.SlipAngle) + '\n')
		else:
			self.lstInpLines.append('*LATERAL_CONTROL  =  1, 0.0\n')
		self.lstInpLines.append('*ROTATION_CONTROL =  0, 0.0\n')
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D104' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D203' or self.strlstSnsInfo == 'D204':
			self.lstInpLines.append('*ROAD_GEOM        =  0.000 ( road=0, drum or disc.=diameter in meter: RR(1.707), CLEAT(2.50), Wear(3.048), LAT100(0.317) )\n')
		else:
			self.lstInpLines.append('*ROAD_GEOM        =  1.707 ( road=0, drum or disc.=diameter in meter: RR(1.707), CLEAT(2.50), Wear(3.048), LAT100(0.317) )\n')

class InpTireModel:
	def createTireModel(self, lstSnsInfo):
		self.strlstSnsInfo = lstSnsInfo["AnalysisInformation"]["SimulationCode"]
		self.strlstSnsInfo = self.strlstSnsInfo.split('-')[-2]

		self.lstInpLines=[]
		
		self.JobFolder   = '/home/fiper/ISLM/ISLM_JobFolder'
		self.DBLocation  = lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireDBLocation"]
		self.ProductCode = lstSnsInfo["VirtualTireBasicInfo"]["ProductCode"]
		self.VTCode      = lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"]
		self.HiddenRev   = lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"]
		self.SimCode     = lstSnsInfo["AnalysisInformation"]["SimulationCode"]

		#self.lstInpLines.append('*INCLUDE, INP=' + self.JobFolder + '/' + self.DBLocation + '/' + str(self.ProductCode) + '/' + self.VTCode + '-' + str(self.HiddenRev) + '/' + self.SimCode + '/' + str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"]) + '-' + str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"]) + '.axi' + '\n')
		#self.lstInpLines.append('*INCLUDE, INP=' + self.JobFolder + '/' + self.DBLocation + '/' + str(self.ProductCode) + '/' + self.VTCode + '-' + str(self.HiddenRev) + '/' + self.SimCode + '/' + str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"]) + '-' + str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"]) + '.trd' + '\n')
		self.lstInpLines.append('*INCLUDE, INP=' + os.getcwd() + '/' + str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"]) + '-' + str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"]) + '.axi' + '\n')
		self.lstInpLines.append('*INCLUDE, INP=' + os.getcwd() + '/' + str(lstSnsInfo["VirtualTireBasicInfo"]["VirtualTireID"]) + '-' + str(lstSnsInfo["VirtualTireBasicInfo"]["HiddenRevision"]) + '.trd' + '\n')
		self.lstInpLines.append('*****************************************************************************************************************************\n')
		self.lstInpLines.append('*STEEL_BEAD_ELSET_FOR_SUB_CYCLING=BD1\n')
		self.lstInpLines.append('*GROOVE_DEPTH_FOR_FPC  =0.001\n')
		self.lstInpLines.append('*RIM_FRICTION          =1.000\n')
		self.lstInpLines.append('*ROAD_FRICTION (UO, ZP, KP, ZS, KS, ALPHA, TAUC, BETA)\n')
		#if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202' or self.strlstSnsInfo == 'D204':
		if self.strlstSnsInfo == 'D101' or self.strlstSnsInfo == 'D103' or self.strlstSnsInfo == 'D201' or self.strlstSnsInfo == 'D202':
			self.lstInpLines.append('0.1, 0., 0., 0., 0., 0., 0., 0.\n')
		#elif self.strlstSnsInfo == 'D104':   # Dynamic Foot shape
		elif self.strlstSnsInfo == 'D104' or self.strlstSnsInfo == 'D204':   # Dynamic Foot shape
			self.lstInpLines.append('0.6, 0., 0., 0., 0., 0., 0., 0.\n')
		else:                                # RR, Force and Moment 
			self.lstInpLines.append('3.125, 0.44, 0.38, 0.34, 0.46, 8.68, 0.55, 2.94\n')
		self.lstInpLines.append('*****************************************************************************************************************************\n')


if __name__ == "__main__":

	CheckExecution.getProgramTime(str(sys.argv[0]), "Start")

	strJobDir = os.getcwd()
	for (path, dir, files) in os.walk(strJobDir):
		for dirname in dir:
			shutil.rmtree(dirname)
		for filename in files:
			if ''.join(list(filename.split('-')[-1])[0:2]) == 'IF' or ''.join(list(filename.split('-')[-1])[0:2]) == 'DP' or ''.join(list(filename.split('-')[-1])[0:2]) == 'FM' or ''.join(list(filename.split('-')[-1])[0:2]) == 'WS':
				os.remove(filename)
	lstSmartFileNames = glob.glob(strJobDir +'/*.sns')
	strSmartFileName = lstSmartFileNames[0]

	with open(strSmartFileName) as Sns_file:
		lstSnsInfo = json.load(Sns_file)
	print lstSnsInfo["AnalysisInformation"]["SimulationCode"]

	### Error Check ###
	cErrorCheck = ErrorCheck()
	if cErrorCheck.VirtualTireParametersErrorCheck() == []:
		if cErrorCheck.AnalysisInformationErrorCheck() == []:
			if cErrorCheck.ElsetMaterialInfoErrorCheck() == []:

				### Compound change ###
				ChangeCompd("Calendered")
				ChangeCompd("Mixing")
	
				### Create an input file ###
				i = 0
				while i < len(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"]):
					cInpCondDescription = InpCondDescription()
					cInpCondDescription.createCondDescription(i, lstSnsInfo)
	
					cInpRimDescription  = InpRimDescription()
					cInpRimDescription.createRimDescription(i, lstSnsInfo)
	
					cInpMaterial        = InpMaterial()
					cInpMaterial.createMaterialInp(i, lstSnsInfo)
	
					cInpTireModel       = InpTireModel()
					cInpTireModel.createTireModel(lstSnsInfo)
	
					strInpLine = ''.join(cInpCondDescription.lstInpLines + cInpRimDescription.lstInpLines + cInpMaterial.lstCompInpLines+ cInpMaterial.lstCordInpLines + cInpMaterial.lstCompLocLines + cInpTireModel.lstInpLines)
					createInpFile(strJobDir, strInpLine, i, lstSnsInfo)
	
					del cInpCondDescription, cInpRimDescription, cInpMaterial, cInpTireModel
	
					if len(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"]) > 1: 
						IndivSimName= str(lstSnsInfo["AnalysisInformation"]["AnalysisCondition"][i]["Task"])
						inpName = str(lstSnsInfo["AnalysisInformation"]["SimulationCode"]) + '-' + IndivSimName + '.inp'
						os.makedirs(IndivSimName)
						shutil.copy(strJobDir + '/' + inpName, IndivSimName + '/' + inpName)
					i = i + 1
			else:
				print '!!!There is an error in the ElsetMaterial information.!!!'
				EMErrorList = cErrorCheck.ElsetMaterialInfoErrorCheck()
				EMErrors = ''.join(EMErrorList)
				PreSMARTStatus = open('PreError.tmp', 'w')
				PreSMARTStatus.write(EMErrors)
				PreSMARTStatus.close()
		else:
			print '!!!There is an error in the Analysis information.!!!'
			AIErrorList = cErrorCheck.AnalysisInformationErrorCheck()
			AIErrors = ''.join(AIErrorList)
			PreSMARTStatus = open('PreError.tmp', 'w')
			PreSMARTStatus.write(AIErrors)
			PreSMARTStatus.close()
	else:
		if cErrorCheck.AnalysisInformationErrorCheck() == []:
			print '!!!There is an error in the Virtual Tire Parameters.!!!'
			VTErrorList = cErrorCheck.VirtualTireParametersErrorCheck()
			VTErrors = ''.join(VTErrorList)
			PreSMARTStatus = open('PreError.tmp', 'w')
			PreSMARTStatus.write(VTErrors)
			PreSMARTStatus.close()
		else:
			print '!!!There is an error in the Virtual Tire Parameters.!!!'
			print '!!!There is an error in the Analysis information.!!!'
			VTErrorList = cErrorCheck.VirtualTireParametersErrorCheck()
			AIErrorList = cErrorCheck.AnalysisInformationErrorCheck()
			VTErrors = ''.join(VTErrorList)
			AIErrors = ''.join(AIErrorList)
			PreSMARTStatus = open('PreError.tmp', 'w')
			PreSMARTStatus.write(VTErrors)
			PreSMARTStatus.write(AIErrors)
			PreSMARTStatus.close()

	CheckExecution.getProgramTime(str(sys.argv[0]), "End")