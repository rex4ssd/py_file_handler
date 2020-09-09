

import os
import shutil
import glob
import datetime
import sys
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from os import remove, close
from collections import Counter
from operator import itemgetter
import time 

# get file encoding
import chardet  
# for inspect, func name
import inspect

# get dos output
import subprocess
# for regular expression
import re

# all func 20191017
# ..................................................................
# def showError(sMsg, iErrorCode):
# def buildFileDateInfo(sPath):
# def runParseTxt(sXmlPath, inParameter, sPath):
# def findFileExtention(fNmae, fExt):
# def findListFileExtention(fNmae, ListfExt):
# def makeFileExtenInfoEx(lsitStr):
# def runFindSpecFileExtention(sXmlPath, inParameter, sPath, bBrife):
# def runGetFileEncoding(sXmlPath, inParameter, sPath):
# def runGetLibFunc(sXmlPath, inParameter, sPath):
#X def reverseData(rawData, dLen):
# def Decrypt_By_MFC(fPath):
# def runDecrypt_Log(sXmlPath, inParameter, sPath): 
# def runXMLItem(testName, xmlPath, inPara, sPath):
# def parseXML(sXmlPath):
# def convertNoToItem(No):
# def showXMLTable():
# def makeXMLlistTable(sXmlPath):
# def parseArgv(lArgv, xmlPath):
# ..................................................................
# 
def showError(sMsg, iErrorCode):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    global g_ErrorCode
    g_ErrorCode = iErrorCode
    print('[{:<5}]showError, {} ..\n '.format(g_ErrorCode, sMsg))
    return 0
# 
# 
def buildFileDateInfo(sPath):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    try:
        # build from file info 
        file_paths = []  # List which will store all of the full filepaths.
        listFileInfo =[]
        # Walk the tree.
        os.chdir(sPath)
        for root, directories, files in os.walk(sPath):
            for fileName in files:            
                filePath = os.path.join(root, fileName)
                relativefilePath = os.path.relpath(filePath)
                
                # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, filePath, relativefilePath))

                # tupleFileInfo[0] = file name
                # tupleFileInfo[1] = file path
                fileTimeInfo = os.path.getmtime(filePath)
                fileSizeInfo = os.path.getsize(filePath)
                
                # save filePath, Time, Size
                tupleFileInfo = (relativefilePath, fileTimeInfo, fileSizeInfo) 
                listFileInfo.append(tupleFileInfo)  # Add it to the list.            
                # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, relativefilePath, fileTimeInfo))


        print('{:<10s}buildFileInfo  ..'.format('End'))
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))  

    return listFileInfo

# ....................................................................
# Rex 20191014
# remove path, keep file name only
# path/test.dll -> test.ll
def runParseTxt(sXmlPath, inParameter, sPath):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    try:
        tree = ET.parse(sXmlPath)
        root = tree.getroot()   
      
        for neighbor in root.iter('PATHObjects'):
            FolderPath = neighbor.find('Folder_Path').text

        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # txtPath = os.path.join(dir_path, "path.txt")
        
        ## Open file
        fp = open(sPath, "r")
        line = fp.readline()

        ## 用 while 逐行讀取檔案內容，直至檔案結尾
        while line:
            line = fp.readline()
            base=os.path.basename(line)
            # print('{}'.format(line))
            if(len(base) > 0):
                print('{}'.format(base))

        fp.close()

    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))    
    return 0

# find single file extension
def findFileExtention(fNmae, fExt):
    extension = os.path.splitext(fNmae)[1]
    if(extension.find(fExt) > -1):
        # print('extension = {}, fExt = {}'.format(extension, fExt))
        # find it
        return 0
    else:
        # find nothing
        return 1

# find many file's extension
def findListFileExtention(fNmae, ListfExt):
    # get file path extension
    extension = os.path.splitext(fNmae)[1]
    for fExt in ListfExt:
        if(extension.find(fExt) > -1):
            # find it
            # print('extension = {}, fExt = {}'.format(extension, fExt))
            return 0
    # find nothing            
    return 1            

# split string by ","
def makeFileExtenInfoEx(lsitStr):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    try:
        listFileExtenInfo = []
        for val in lsitStr.split(","):
            # if(len(val) == findLength):
            print("Found: " + val)
            listFileExtenInfo.append(val)

        return listFileExtenInfo
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))    


def runFindSpecFileExtention_Brief(sXmlPath, inParameter, sPath, bBrife):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    runFindSpecFileExtention(sXmlPath, inParameter, sPath, bBrife)


def runFindSpecFileExtention(sXmlPath, inParameter, sPath, bBrife):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    try:
        # 
        # sExtendName = ".txt,.ini,.dll,.exe,.lib,.log"
        sExtendName = inParameter
        lFileExt = makeFileExtenInfoEx(sExtendName)
        # 
        listFileFrom = buildFileDateInfo(sPath)

        # sort by date 
        listFileFrom = sorted(listFileFrom,  key=itemgetter(1)) # order by modify date 

        iIndex = 0
        iFileInfoSize = len(listFileFrom)
        while iFileInfoSize > 0:
            iFileInfoSize -= 1

            if(findListFileExtention( listFileFrom[iFileInfoSize][0], lFileExt) ==0): 
            # listFileFrom[iFileInfoSize][0] = file name
            # listFileFrom[iFileInfoSize][1] = modify date
                sFullPathSrc = os.path.join(sPath, listFileFrom[iFileInfoSize][0])     
                local_time = time.ctime(listFileFrom[iFileInfoSize][1]) 
                fSize = listFileFrom[iFileInfoSize][2]

                # get file encoding
                # with open(sFullPathSrc, 'rb') as rawdata:
                #     result = chardet.detect(rawdata.read())     
                if(int(bBrife) == 0):
                    print('{}, {:<10f}KB, {:<120s}'.format(local_time,  fSize/1000, sFullPathSrc))
                elif(int(bBrife) == 1):
                    # show file name only
                    fName = os.path.basename(listFileFrom[iFileInfoSize][0])
                    print('{:<4d}, {:<50s}'.format(iIndex, fName))

                iIndex += 1
        print('{:<10s}runFindSpecFileExtention..'.format('End'))
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))          
    return 0

# REX 20191014
# detect file encoding
def runGetFileEncoding(sXmlPath, inParameter, sPath):
    print('{} go'.format( inspect.currentframe().f_code.co_name))

    try:
        # sExtendName = ".ini"
        sExtendName = inParameter
        lFileExt = makeFileExtenInfoEx(sExtendName)
        # 
        listFileFrom = buildFileDateInfo(sPath)

        # sort by date 
        # listFileFrom = sorted(listFileFrom,  key=itemgetter(1)) # order by modify date 

        # sort by name
        listFileFrom = sorted(listFileFrom,  key=itemgetter(0)) # order by modify date 

        iIndex = 0
        iFileInfoSize = len(listFileFrom)
        while iFileInfoSize > 0:
            iFileInfoSize -= 1

            if(findListFileExtention( listFileFrom[iFileInfoSize][0], lFileExt) ==0): 
                # listFileFrom[iFileInfoSize][0] = file name
                # listFileFrom[iFileInfoSize][1] = modify date
                sFullPathSrc = os.path.join(sPath, listFileFrom[iFileInfoSize][0])     
                local_time = time.ctime(listFileFrom[iFileInfoSize][1])   

                with open(sFullPathSrc, 'rb') as rawdata:
                    rlt_Encode = chardet.detect(rawdata.read())
                # print(filename.ljust(45), result['encoding'])         

                print('{}, {:<110s}, {}'.format(local_time, sFullPathSrc, rlt_Encode['encoding']))

        print('{} End\n '.format( inspect.currentframe().f_code.co_name))
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))       
    return 0


# REX 20191022
# get function name from .lib file
def runGetLibFunc(sXmlPath, inParameter, sPath):
    print('{} go'.format( inspect.currentframe().f_code.co_name))

    try:
        # sExtendName = ".ini"
        sExtendName = inParameter
        lFileExt = makeFileExtenInfoEx(sExtendName)
        # 
        listFileFrom = buildFileDateInfo(sPath)

        # sort by name
        listFileFrom = sorted(listFileFrom,  key=itemgetter(0)) # order by modify date 

        # set VC Env
        sExe = os.path.join(dir_path, "vcvars32.bat")        
        sCmd = sExe 
        os.system(sCmd)                      

        iIndex = 0
        iFileInfoSize = len(listFileFrom)
        while iFileInfoSize > 0:
            iFileInfoSize -= 1

            if(findListFileExtention( listFileFrom[iFileInfoSize][0], lFileExt) ==0): 
                # listFileFrom[iFileInfoSize][0] = file name
                # listFileFrom[iFileInfoSize][1] = modify date
                (sFullPathSrc) = os.path.join(sPath, listFileFrom[iFileInfoSize][0])     

                # sExe = os.path.join(dir_path, "vcvars32.bat")        
                sCmd = 'lib /list ' + sFullPathSrc
                print(listFileFrom[iFileInfoSize][0])
                # var = os.system(sCmd)
                process  =  subprocess.Popen(sCmd, shell=True, stdout=subprocess.PIPE)
                stdout = process.communicate()[0]
                # object to string 
                getStr = str(stdout)

                # from 
                # ori = b'Microsoft (R) Library Manager Version 10.00.30319.01\r\nCopyright (C) Microsoft Corporation.  All rights reserved.\r\n\r\nDebug\\UIProcessMSG.obj\r\n'
                # to 
                # 0, UIProcessMSG.obj
                match =  re.findall(r'[A-Za-z]*.obj\b', getStr)                
                # print('ori = {}'.format(getStr))                    
                # print('var = {}'.format(match))

                iIndex = 0
                for elem in match:
                    # escape '\\.obj'
                    if(elem.find('\\') == -1):
                        print('{:>3}, {}'.format(iIndex,elem))
                        iIndex += 1
                        # newMatch.append( elem)

        print('{} End\n '.format( inspect.currentframe().f_code.co_name))
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))       
    return 0

# ..................................................................................................
# 
def Decrypt_By_MFC(fPath):
    print('{} go'.format( inspect.currentframe().f_code.co_name))
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sExe = os.path.join(dir_path, "VC_2017_Cmd.exe")        
        sCmd = sExe + ' 0 ' + fPath
        os.system(sCmd)        

        # print('fLen = {}'.format(fLen));
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))   

# REX 20191015
# runDecrypt Log, not ready
def runDecrypt_Log(sXmlPath, inParameter, sPath):
    print('{} go, sPath = {}'.format( inspect.currentframe().f_code.co_name, sPath))

    try:
        sExtendName = ".log,.txt"
        lFileExt = makeFileExtenInfoEx(sExtendName)
        # 
        listFileFrom = buildFileDateInfo(sPath)

        nPara = int(inParameter)
        if ( nPara > 0):
            iIndex = 0
            iFileInfoSize = len(listFileFrom)
            while iFileInfoSize > 0:
                iFileInfoSize -= 1

                if(findListFileExtention( listFileFrom[iFileInfoSize][0], lFileExt) ==0): 
                # listFileFrom[iFileInfoSize][0] = file name
                # listFileFrom[iFileInfoSize][1] = modify date
                    sFullPathSrc = os.path.join(sPath, listFileFrom[iFileInfoSize][0])     
                    local_time = time.ctime(listFileFrom[iFileInfoSize][1])   

                    Decrypt_By_MFC(sFullPathSrc)

                    print('{}, {:<70s}'.format(local_time, sFullPathSrc))
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))    

    print('{} End\n '.format( inspect.currentframe().f_code.co_name))
    return 0


def runXMLItem(testName, xmlPath, inPara, sPath):
    print('{} go, testName = {}'.format( inspect.currentframe().f_code.co_name, testName))
    try:
        # print('{:<10s}test name ..'.format(testName))
        if ( testName == 'FindSpecFileExtention'):
            runFindSpecFileExtention(xmlPath, inPara, sPath, 0)
        if ( testName == 'FindSpecFileExtention_Brief'):
            runFindSpecFileExtention_Brief(xmlPath, inPara, sPath, 1)            
        if ( testName == 'GetFileEncoding'):
            runGetFileEncoding(xmlPath, inPara, sPath)  
        if ( testName == 'GetLibFunc'):
            runGetLibFunc(xmlPath, inPara, sPath)              
        if ( testName == 'Decrypt_Log'):
            runDecrypt_Log(xmlPath, inPara, sPath)     
        if ( testName == 'ParseTxt'):
            runParseTxt(xmlPath, inPara, sPath)     
        if ( testName == 'Pause'):
            runPause()                                                
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))  

def parseXML(sXmlPath):

    ListCount = 0
    ListItem = ['']
    ListState = ['','','','','']

    tree = ET.parse(xmlPath)
    root = tree.getroot()     

    for child in root.iter('Item'):
        testName = child.get('Name')
        testState = child.get('Enabled')
        inParameter = child.get('Param', default = 'Empty')
        testFileType = child.get('FileType')
        testPath = child.get('Path', default = "Empty")
        
        if (testState == 'TRUE'):
            runXMLItem(testName, sXmlPath, inParameter, testPath)

            ListItem.insert(ListCount, testName)
            ListCount +=1

    print('\n-------------------------------------------------------------------\n')

    nfinishList = 1 
    for finishList in ListItem:
        if (finishList):
            print('finishList[{}]:{:>25}'.format(nfinishList, finishList))
            nfinishList += 1
        

    print('\n-------------------excellent you are---------------------------------\n')
    return 0

def convertNoToItem(No):
    global gXMLTable
    try:
        # print('No = {}, gXMLTable = {}'.format(int(No), len(gXMLTable)))
        if ( int(No) < len(gXMLTable) ):
            return gXMLTable[No]
        else:
            return 'NULL'
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))  

def showXMLTable():
    print('{} go'.format( inspect.currentframe().f_code.co_name))

    global gXMLTable
    ListState = ['','','','','']
    
    try:
        index = 1
        tableSize = len (gXMLTable)

        print ('{:.<4s}{:.<30s}, {:.<80s}, {}'.format('No','testName', 'testPath', 'testState'))
        while index < tableSize:
            # print ('{:<4d}{:<30s}, {:<80s}, {}'.format(ListCount, testName, testPath, testState))

            print('{:<4d}{:<30s}, {:<80s}, {}'.format
                (gXMLTable[index][0], 
                    gXMLTable[index][1],
                    gXMLTable[index][4],
                    gXMLTable[index][2]
                ))
            index += 1
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))          
    
    return 0

def makeXMLlistTable(sXmlPath):
    print('{} go, sXmlPath = {}'.format( inspect.currentframe().f_code.co_name, sXmlPath))
    # 0 for show all item
    ListCount = 1
    global gXMLTable
    gXMLTable= ['']
    ListState = ['','','','','']

    tree = ET.parse(xmlPath)
    root = tree.getroot()     
    try:
        for child in root.iter('Item'):

            testName = child.get('Name')
            testState = child.get('Enabled')
            testParam = child.get('Param')
            # testFileType = child.get('FileType')
            testPath = child.get('Path', default="empty")
    
            setItme =  (ListCount, testName, testState, testParam, testPath)
            gXMLTable.append(setItme)

            ListCount +=1
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))         
    
    return 0


def parseArgv(lArgv, xmlPath):
    # 0 for show all Item
    i = 1 

    try:
        # no paramter
        if(len(lArgv) == 1):
            parseXML(xmlPath)    
        # exist parameter       
        elif(len(lArgv) == 2):
            iArgv = int(lArgv[1])
            print('iArgv = {}'.format(iArgv))
            # para 1 = 0, show xml only
            if(iArgv > 0 ):                
                # para 1 > 0, run xml item
                # print("iArgv == 1\n")
                singleXMLItem = convertNoToItem(iArgv)

                if(singleXMLItem != 'NULL'):
                    print ('Item = {},'.format(singleXMLItem))                   
                    runXMLItem(singleXMLItem[1], xmlPath, singleXMLItem[3], singleXMLItem[4])
                else:
                    print('X, {}, iArgv = {} over context\n'.format( inspect.currentframe().f_code.co_name, iArgv))
            else:
                showXMLTable()

        print('O, {}'.format( inspect.currentframe().f_code.co_name))                     
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))   

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xmlPath = os.path.join(dir_path, "py_file.xml")

    sStartTime = datetime.datetime.now()
    print('StartTime:{}..'.format(sStartTime))
    print('version:{}\n'.format( sys.version))
    print('argv:{}\n'.format(sys.argv))
    
    try:
        makeXMLlistTable(xmlPath)
        # showXMLTable()
        parseArgv(sys.argv, xmlPath)

        sEndTime = datetime.datetime.now()      
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))   

    sys.exit(0)

# ................................................................................
# not ready
def reverseData(rawData, dLen):
    print('{} go, dLen = {}'.format( inspect.currentframe().f_code.co_name, dLen))

    try:
        # print('reverseData 23') 
        # newData = rawData
        newData = str.encode(rawData)
        # print('reverseData 231') 
        
        # read arrary ok
        # show invert(~) arrary ok 
        if(dLen > 0):
            print('a1 = {:x}, a2 = {:x}'.format(newData[1], newData[0]))
            print('a1 = {:x}, a2 = {:x}'.format(not newData[1],  not newData[0]))
        
            i = 0
            while (i < dLen ):
                print('going1, i = {}'.format(i))
                # error happend
                cpy[i] =  not newData[i]
                # print('going2, i = {}'.format(i))
                i = i + 1
                # print('going3, i = {}'.format(i))
        print('reverseData end') 
    except:             
        print ('{}, Unexpected error:{}'.format(inspect.currentframe().f_code.co_name, sys.exc_info()))   