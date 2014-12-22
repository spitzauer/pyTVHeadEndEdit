#!/usr/bin/env python3
import os, sys, argparse
g_sChannelDir = "channel/config"
g_sChannelFile = "channels.csv"
g_sServicesDir = "input/dvb/networks"
g_sSvcnamePrefix = "\"svcname\": \""
g_sSvcnameSufix = "\""
g_sCheckCorrectService = "\"pid\":"
g_sNumberPrefix = "\"number\": "
g_sNumberSufix = ","

_debug_ = False

def dprint(str):
    if _debug_:
        print("DEBUG: " + str)
def eprint(str):
    print("ERROR: " + str)
    sys.exit(-1)
def wprint(str):
    print("WARNING: " + str)

def searchServices(p_sSearch):
    iNumOfServies = 0
    iNumOfFoundString = 0
    sFilenameReturn = ""
    for sRoot, sSubdirs, sFiles in os.walk(g_sServicesDir):
        for sFilename in sFiles:
            iNumOfServies = iNumOfServies + 1
            bFoundString = False
            with open(os.path.join(sRoot, sFilename), 'r') as fFile:
                sContent = fFile.read()
                if sContent.find(p_sSearch) > -1:
                    iNumOfFoundString = iNumOfFoundString + 1
                    bFoundString = True
                if (sContent.find(g_sCheckCorrectService) > -1) and (bFoundString):
                    sFilenameReturn = sFilename
    if iNumOfFoundString == 0:
         wprint("searchServices: Could not find String: " + p_sSearch)
    if iNumOfFoundString > 1:
         wprint("searchServices: Found String " + p_sSearch + " in " + str(iNumOfFoundString) + " files")
    dprint("searchServices: Found String " + p_sSearch + " in " + sFilenameReturn)
    dprint("searchServices: Number of Services: " + str(iNumOfServies))
    return sFilenameReturn

def searchChannel(p_sSearch):
    iNumOfChannel = 0
    sFilenameReturn = ""
    for sRoot, sSubdirs, sFiles in os.walk(g_sChannelDir):
        for sFilename in sFiles:
            iNumOfChannel = iNumOfChannel + 1
            with open(os.path.join(sRoot, sFilename), 'r') as fFile:
                sContent = fFile.read()
                if sContent.find(p_sSearch) > -1:
                    sFilenameReturn = os.path.join(sRoot, sFilename)
    dprint("searchChannel: Found String " + p_sSearch + " in " + sFilenameReturn)
    dprint("searchChannel: Number of Channel: " + str(iNumOfChannel))
    return sFilenameReturn

def editChannel(p_sFilename, p_iNumber):
    dprint("editChannel: Open channel file: " + p_sFilename)
    fChannelFile = open(p_sFilename, "r")
    dChannelFile = fChannelFile.readlines()
    fChannelFile.close()
    sOldChannelNumber = "ERROR"
    for sChannelLine in dChannelFile:
        iChannelNumberStart = sChannelLine.find(g_sNumberPrefix)
        if iChannelNumberStart > -1:
            iChannelNumberStart = iChannelNumberStart + len(g_sNumberPrefix)
            iChannelNumberEnd =  sChannelLine.find(g_sNumberSufix)
            sOldChannelNumber = sChannelLine[iChannelNumberStart:iChannelNumberEnd]
    if sOldChannelNumber == "ERROR":
        wprint("editChannel: Did not found string " + g_sNumberPrefix + " in file " + p_sFilename)
    if sOldChannelNumber != str(p_iNumber):
        dprint("editChannel: Change number from " + sOldChannelNumber + " to " + str(p_iNumber))
        fChannelFile = open(p_sFilename, "w")
        for sChannelLine in dChannelFile:
            if sChannelLine.find(g_sNumberPrefix) > -1:
                sChannelLine = sChannelLine.replace(sOldChannelNumber, str(p_iNumber))
            fChannelFile.write(sChannelLine)
        fChannelFile.close()
    else:
        dprint("editChannel: Already correct number: " + sOldChannelNumber)

def setChannelNumber():
    fChannelFile = open(g_sChannelFile)
    dChannelFile = fChannelFile.readlines()
    fChannelFile.close()
    iChannelNumber = 0
    for sChannelFileLine in dChannelFile:
        if sChannelFileLine.find("#") != 0: # "#" is the comment string (has to be at the first place in the line)
            if sChannelFileLine.count(";") == 4:
                iChannelNumber = iChannelNumber + 1
                sChannelName, sChannelIcon, sChannelTags, sChannelPre, sChannelPost = sChannelFileLine.split(";")
                sChannelPost = sChannelPost.replace("\n", "")
                editChannel(searchChannel(searchServices(g_sSvcnamePrefix + sChannelName + g_sSvcnameSufix)), iChannelNumber)
            else:
                eprint(g_sChannelFile + " has at least one syntax error. (One line must have four \";\")")

def resetChannelNumber():
    for sRoot, sSubdirs, sFiles in os.walk(g_sChannelDir):
        for sFilename in sFiles:
            editChannel(os.path.join(sRoot, sFilename), 0)

resetChannelNumber()
setChannelNumber()
