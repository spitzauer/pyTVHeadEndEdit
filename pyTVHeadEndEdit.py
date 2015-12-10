#!/usr/bin/env python3
import os, sys, argparse, json, csv, unicodedata


# Channel List can maybe also generated with the help of http://de.kingofsat.net/

g_sChannelDir          = "channel/config"
g_sTagsDir             = "channel/tag"
g_sServicesDir         = "input/dvb/networks"
g_sEnigma2FileWoExt    = "temp"
g_bDebug               = True
g_bTest                = False
#g_lProviderBlacklist   = ["AB SAT", "CANAL +", "CANAL+", "Canal+", "CL13", "Contactanos", "COSMO", "CPC1", "CPC2", "CPC3", "DIGITAL+", "Digital+", "GLOBECAST", "GlobeCast", "Groupe M6", "HOLLYW", "IMEDIA", "Orange TV", "ORS", "Persidera", "PRISA TV", "PRISAT TV", "RTVE", "Sogecable", "TCM", "TDA", "Telefonica Servicios Audiovisuales", "TQ1", "TQ2", "TQ5", "TQ6", "TQ7", "TQ8", "TSA", "TVE", "TXY"]


def uprint(str):
    try:
        print(str)
    except Exception as e:
        ascii = unicodedata.normalize('NFKD', str).encode('ascii','ignore')
        sys.stdout.buffer.write(ascii)
        print(" <- This string raised an exeption!")
def dprint(str):
    if g_bDebug:
        uprint("DEBUG:   " + str)
def eprint(str):
    uprint("ERROR:   " + str)
    sys.exit(-1)
def wprint(str):
    uprint("WARNING: " + str)
    #os.system("pause")



def GetTagsData(p_sTagsFileName):
    dprint("GetTagsData(\"" + p_sTagsFileName + "\")")
    
    for sRoot, sSubdirs, sFiles in os.walk(g_sTagsDir):
        for sFilename in sFiles:
            if sFilename == p_sTagsFileName:
                try:
                    with open(os.path.join(sRoot, sFilename), 'r', encoding="utf8") as fTagsData:
                        sTagsData = json.load(fTagsData)
                except Exception:
                    wprint("The Tag \"" + p_sTagsFileName + "\" file cannot be opened!")
                    sTag = "**ERROR** Tag File cannot be opened."
                    return sTag
                else:
                    if 'name' in sTagsData:
                        sTag = str(sTagsData['name'])
                    else:
                        wprint("The Tag \"" + p_sTagsFileName + "\" has no name element!")
                        sTag = "**ERROR** Name not Found."
                    return sTag

def GetServiceData(p_sServiceFileName):
    dprint("GetServiceData(\"" + p_sServiceFileName + "\")")
    
    for sRoot, sSubdirs, sFiles in os.walk(g_sServicesDir):
        for sFilename in sFiles:
            if sFilename == p_sServiceFileName:
                try:
                    with open(os.path.join(sRoot, sFilename), 'r', encoding="utf8") as fServiceData:
                        sServiceData = json.load(fServiceData)
                except Exception:
                    wprint("The Service \"" + p_sServiceFileName + "\" file cannot be opened!")
                    sName = "**ERROR** Service File cannot be opened."
                    sProvider = "**ERROR** Service File cannot be opened."
                    sServiceType = "**ERROR** Service File cannot be opened."
                    return sName, sProvider, sServiceType
                else:
                    if 'svcname' in sServiceData:
                        sName = str(sServiceData['svcname'])
                    else:
                        wprint("The Service \"" + p_sServiceFileName + "\" has no svcname element!")
                        sName = "**ERROR** Name not Found."
                    if 'provider' in sServiceData:
                        sProvider = str(sServiceData['provider'])
                    else:
                        wprint("The Service \"" + p_sServiceFileName + "\" has no provider element!")
                        sProvider = "**ERROR** Provider not Found."
                    if 'dvb_servicetype' in sServiceData:
                        sServiceType = str(sServiceData['dvb_servicetype'])
                    else:
                        wprint("The Service \"" + p_sServiceFileName + "\" has no service Type element!")
                        sServiceType = "**ERROR** Service Type not Found."
                    return sName, sProvider, sServiceType
                
    wprint("The Service \"" + p_sServiceFileName + "\" file not found!")
    sName = "**ERROR** Service File not Found."
    sProvider = "**ERROR** Service File not Found."
    sServiceType = "**ERROR** Service File not Found."
    
    return sName, sProvider, sServiceType

def GetChannelData(p_sChannelFileName):
    dprint("GetChannelData(\"" + p_sChannelFileName + "\")")
    
    try:
        with open(p_sChannelFileName, 'r', encoding="utf8") as fChannelData:
            sChannelData = json.load(fChannelData)
    except Exception:
        wprint("The Channel \"" + p_sChannelFileName + "\" file cannot be opened!")
        sNumber      = "**ERROR** Channel File cannot be opened."
        sName        = "**ERROR** Channel File cannot be opened."
        sProvider    = "**ERROR** Channel File cannot be opened."
        sTags        = "**ERROR** Channel File cannot be opened."
        sServiceType = "**ERROR** Channel File cannot be opened."
        sServiceFile = "**ERROR** Channel File cannot be opened."
        sPicon       = "**ERROR** Channel File cannot be opened."
    else:
        if 'number' in sChannelData:
            sNumber = str(sChannelData['number'])
        else:
            wprint("The Channel \"" + p_sChannelFileName + "\" has no number element!")
            sNumber = "**ERROR** Number not Found."
        if 'icon' in sChannelData:
            sPicon = str(sChannelData['icon'])
        else:
            wprint("The Channel \"" + p_sChannelFileName + "\" has no icon element!")
            sPicon = "**ERROR** Icon not Found."
        if 'services' in sChannelData:
            sServiceList = sChannelData['services']
            if len(sServiceList) == 0:
                wprint("The Channel \"" + p_sChannelFileName + "\" has 0 Service defined!")
                sName        = "**ERROR** Service has 0 elements."
                sProvider    = "**ERROR** Service has 0 elements."
                sServiceType = "**ERROR** Service has 0 elements."
            else:
                if len(sServiceList) > 1:
                    wprint("The Channel \"" + p_sChannelFileName + "\" has not 1 Service (" + str(len(sServiceList)) + ")!")
                    sServiceFile = "**ERROR** More Services found"
                else:
                    sServiceFile = sServiceList[0]
                sName, sProvider, sServiceType = GetServiceData(sServiceList[0]) # if more Services defined only the 1st one is used
        else:
            wprint("The Channel \"" + p_sChannelFileName + "\" has no services element!")
            sName        = "**ERROR** Service not Found."
            sProvider    = "**ERROR** Service not Found."
            sServiceFile = "**ERROR** Service not Found."
        if 'tags' in sChannelData:
            sTagsList = sChannelData['tags']
            if len(sTagsList) == 0:
                dprint("The Channel \"" + p_sChannelFileName + "\" has 0 Tags defined!")
                sTags = ""
            else:
                iBegin = 0
                for sTag in sTagsList:
                    iBegin = iBegin + 1
                    if iBegin == 1:
                        sTags = GetTagsData(sTag)
                    else:
                        sTags = sTags + "," + GetTagsData(sTag)
        else:
            dprint("The Channel \"" + p_sChannelFileName + "\" has no tags element!")
            sTags = ""
    
    return sNumber, sName, sProvider, sTags, sServiceType, sServiceFile, sPicon

def EditChannelNumberTags(p_sChannelFileName, p_iNumber, p_lTags):
    dprint("EditChannelNumber(\"" + p_sChannelFileName + "\", \"" + str(p_iNumber) + "\", <TAGS_LIST>)")
    for sTag in p_lTags:
        dprint("<TAGS_LIST> \"" + sTag + "\"")
    
    sChannelFileName = g_sChannelDir + "/" + p_sChannelFileName
    try:
        with open(sChannelFileName, 'r', encoding="utf8") as fChannelDataR:
            sChannelData = json.load(fChannelDataR)
    except Exception:
        wprint("The Channel \"" + sChannelFileName + "\" file cannot be opened!")
        return
    sChannelData['number'] = p_iNumber
    sChannelData['tags'] = p_lTags
    if p_iNumber == 0:
        sChannelData['enabled'] = False # I also disable the channel if Number is 0
    else:
        sChannelData['enabled'] = True
    with open(sChannelFileName, 'w', encoding="utf8") as fChannelDataW:
        json.dump(sChannelData, fChannelDataW, indent="\t", separators=(',', ': '))

def FindServiceFile(p_sServiceName, p_sServiceProvider):
    dprint("FindServiceFile(\"" + p_sServiceName + "\", \"" + p_sServiceProvider + "\")")
    
    i = 0
    for sRoot, sSubdirs, sFiles in os.walk(g_sServicesDir):
        for sFilename in sFiles:
            try:
                with open(os.path.join(sRoot, sFilename), 'r', encoding="utf8") as fServiceData:
                    sServiceData = json.load(fServiceData)
            except Exception:
                wprint("The Service \"" + sFilename + "\" file cannot be opened!")
            else:
                if ('svcname' in sServiceData):
                    if (p_sServiceName == str(sServiceData['svcname'])):
                        if (p_sServiceProvider.find("**ERROR**") == -1):
                            if ('provider' in sServiceData):
                                if (p_sServiceProvider == str(sServiceData['provider'])):
                                    dprint("Found Service File: " + sFilename)
                                    i = i + 1
                                    sServiceFile = sFilename
                        else:
                            dprint("Found Service File: " + sFilename + " without Provider")
                            i = i + 1
                            sServiceFile = sFilename
    if i == 0:
        wprint("The Service Name \"" + p_sServiceName + "\" and Provider \"" + p_sServiceProvider + "\" not found!")
        sServiceFile = "**ERROR**"
    if i > 1:
        wprint("The Service Name \"" + p_sServiceName + "\" and Provider \"" + p_sServiceProvider + "\" are found in " + str(i) + " files!")
        sServiceFile = "**ERROR**"
    
    return sServiceFile

def FindChannelFile(p_sServiceFileName):
    dprint("FindChannelFile(\"" + p_sServiceFileName + "\")")
    
    i = 0
    for sRoot, sSubdirs, sFiles in os.walk(g_sChannelDir):
        for sFilename in sFiles:
            try:
                with open(os.path.join(sRoot, sFilename), 'r', encoding="utf8") as fChannelData:
                    sChannelData = json.load(fChannelData)
            except Exception:
                wprint("The Service \"" + sFilename + "\" file cannot be opened!")
            else:
                if 'services' in sChannelData:
                    lServiceFiles = sChannelData['services']
                    for sServiceFile in lServiceFiles:
                        if p_sServiceFileName == sServiceFile:
                            dprint("Found Channel File: " + sFilename)
                            i = i + 1
                            sChannelFile = sFilename
    
    if i == 0:
        wprint("The Service File Name \"" + p_sServiceFileName + "\" not found!")
        sChannelFile = "**ERROR**"
    if i > 1:
        wprint("The Service File Name \"" + p_sServiceFileName + "\" is found in " + str(i) + " files!")
        sChannelFile = "**ERROR**"
    
    return sChannelFile

def FindTagsFile(p_sTagsName):
    dprint("FindTagsFile(\"" + p_sTagsName + "\")")
    
    lTagsFile = []
    lTagsName = p_sTagsName.split(',')
    for sTagsName in lTagsName:
        i = 0
        for sRoot, sSubdirs, sFiles in os.walk(g_sTagsDir):
            for sFilename in sFiles:
                try:
                    with open(os.path.join(sRoot, sFilename), 'r', encoding="utf8") as fTagsData:
                        sTagsData = json.load(fTagsData)
                except Exception:
                    wprint("The Tags \"" + sFilename + "\" file cannot be opened!")
                else:
                    if 'name' in sTagsData:
                        if sTagsName == str(sTagsData['name']):
                            dprint("Found Tags File: " + sFilename)
                            i = i + 1
                            lTagsFile.append(sFilename)
        
        if i == 0:
            wprint("The Tags Name \"" + sTagsName + "\" not found!")
        if i > 1:
            wprint("The Tags Name \"" + sTagsName + "\" is found in " + str(i) + " files!")
        
    return lTagsFile

def ExportChannelData(sCSVExport):
    i = 0
    
    for sRoot, sSubdirs, sFiles in os.walk(g_sChannelDir):
        for sFilename in sFiles:
            i = i + 1
    iMaxChannels = i
    i = 0
    with open(sCSVExport, 'w', newline='', encoding="utf8") as fCSVExport:
        wCSVExport = csv.writer(fCSVExport, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wCSVExport.writerow(['Number', 'Name', 'Provider', 'Tag', 'Channel File Name', 'Service File Name', 'Service Type', 'picon'])
        dChannel = {}
        for sRoot, sSubdirs, sFiles in os.walk(g_sChannelDir):
            for sFilename in sFiles:
                i = i + 1
                sNumber, sName, sProvider, sTags, sServiceType, sServiceFile, sPicon = GetChannelData(os.path.join(sRoot, sFilename))
                wCSVExport.writerow([sNumber, sName, sProvider, sTags, sFilename, sServiceFile, sServiceType, sPicon])
                uprint("Export Channel(" + str(i) + "/" + str(iMaxChannels) + "): " + sFilename + " " + sName + ", " + sProvider + " " + sTags + " (" + sNumber + ")" )
                if (sPicon.find("**ERROR**") == -1):
                    dChannel[sPicon] = [sNumber, sTags]
                else:
                    if sRow[0] == "0":
                        dprint("No Picon for \"" + sRow[1] + "\", \"" + sRow[2] + "\" defined in file \"" + sCSVImport + "\"!")
                    else:
                        wprint("No Picon for \"" + sRow[1] + "\", \"" + sRow[2] + "\" defined in file \"" + sCSVImport + "\"!")
    return dChannel

def ChangeChannelData(sCSVImport):
    i = 0
    with open(sCSVImport, 'r', encoding="utf8") as fCSVImport:
        wCSVImport = csv.reader(fCSVImport, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for sRow in wCSVImport:
            i = i + 1
    iMaxChannels = i - 1 # minus Header
    i = 0
    with open(sCSVImport, 'r', encoding="utf8") as fCSVImport:
        wCSVImport = csv.reader(fCSVImport, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dChannel = {}
        for sRow in wCSVImport:
            i = i + 1
            if i != 1: # remove Header
                sServiceFileName = FindServiceFile(sRow[1], sRow[2])
                if sServiceFileName != "**ERROR**":
                    sChannelFileName = FindChannelFile(sServiceFileName)
                    lTagsFileName = FindTagsFile(sRow[3])
                    uprint("Change Channel(" + str(i-1) + "/" + str(iMaxChannels) + "): " + sChannelFileName + " " + sRow[1] + ", " + sRow[2] + " " + sRow[3] + " (" + sRow[0] + ")" )
                    if sChannelFileName != sRow[4]:
                        dprint("Channel File Name Changed from \"" +  sRow[4] + "\" to \"" + sChannelFileName + "\".")
                    if sServiceFileName != sRow[5]:
                        dprint("Service File Name Changed from \"" +  sRow[5] + "\" to \"" + sServiceFileName + "\".")
                    EditChannelNumberTags(sChannelFileName, sRow[0], lTagsFileName)
                    if (sRow[7].find("**ERROR**") == -1):
                        dChannel[sRow[7]] = [sRow[0], sRow[3]]
                    else:
                        if sRow[0] == "0":
                            dprint("No Picon for \"" + sRow[1] + "\", \"" + sRow[2] + "\" defined in file \"" + sCSVImport + "\"!")
                        else:
                            wprint("No Picon for \"" + sRow[1] + "\", \"" + sRow[2] + "\" defined in file \"" + sCSVImport + "\"!")
                else:
                    uprint("Change Channel(" + str(i-1) + "/" + str(iMaxChannels) + "): Error, Service File with Channel Name " + sRow[1] + " and Channel Provider " + sRow[2] + " not found!")
    return dChannel

def CheckNumbers(sCSVImport):
    dprint("CheckNumbers(\"" + sCSVImport + "\")")
    lNumbers = []
    with open(sCSVImport, 'r', encoding="utf8") as fCSVImport:
        wCSVImport = csv.reader(fCSVImport, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for sRow in wCSVImport:
            lNumbers.append(sRow[0].rjust(9, "0"))
    lNumbers.sort()
    sOldNumber = "000000000"
    for sNumber in lNumbers:
        if sNumber != "000000000":
            if sNumber == sOldNumber:
                eprint("The Number \"" + sNumber + "\" is set at least twice in file \"" + sCSVImport + "\"")
            sOldNumber = sNumber

def Enigma2Ouput(p_sFileName, P_dChannels):
    dprint("Enigma2Ouput(\"" + p_sFileName + "\", <CHANNEL_DICT>)")
    for sPicon in P_dChannels:
        dprint("<CHANNEL_DICT> \"" + sPicon + "\" + \"" + P_dChannels[sPicon][0] + "\", \"" + P_dChannels[sPicon][1] + "\"")
    
    lTv = []
    lRadio = []
    for sPicon in P_dChannels:
        if P_dChannels[sPicon][0] != "0":
            if P_dChannels[sPicon][1].find("Radio") == -1:
                lTv.append(P_dChannels[sPicon][0].rjust(9, "0") + "@" + sPicon)
            else:
                lRadio.append(P_dChannels[sPicon][0].rjust(9, "0") + "@" + sPicon)
    lTv.sort()
    lRadio.sort()
    
    with open(p_sFileName + ".tv", "w", encoding="utf8") as fEnigma2Tv:
        fEnigma2Tv.write("#NAME Favourites (TV)\n")
        for sTv in lTv:
            sTvNew = sTv[sTv.find("@")+9:-4]
            sTvNew = sTvNew.replace("_", ":") + ":"
            dprint("Writing Service \"" + sTvNew + "\" (#" + sTv[0:sTv.find("@")] + ") to \"" + p_sFileName + ".tv\"")
            fEnigma2Tv.write("#SERVICE " + sTvNew + "\n")
    with open(p_sFileName + ".radio", "w", encoding="utf8") as fEnigma2Radio:
        fEnigma2Radio.write("#NAME Favourites (Radio)\n")
        for sRadio in lRadio:
            sRadioNew = sRadio[sRadio.find("@")+9:-4]
            sRadioNew = sRadioNew.replace("_", ":") + ":"
            dprint("Writing Service \"" + sRadioNew + "\" (#" + sRadio[0:sRadio.find("@")] + ") to \"" + p_sFileName + ".radio\"")
            fEnigma2Radio.write("#SERVICE " + sRadioNew + "\n")


#####################################
######      Main Programm      ######
#####################################
if g_bTest:
    #GetServiceData("b420f25fcf0e1c9a0ea493b4d5c1b46d")
    CheckNumbers("master.csv")
else:
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--export', metavar='csv-File', help="Export the TVHeadend Channels to a csv File")
    parser.add_argument('-c', '--change', metavar='csv-File', help="Change the TVHeadend Channel Numbers and Tags from a csv File")
    parser.add_argument('-o', '--output', metavar='enigma2-File', help="Output also the enigma2 File (without Extention)")
    parser.add_argument('-v', '--verbose', action="store_true", help="Debug output")
    args = parser.parse_args()
    if args.verbose:
        g_bDebug = True
    else:
        g_bDebug = False
    if (not args.export) and (not args.change):
        uprint("Export and Change in one step. But this makes no sense!")
        dChannels = ExportChannelData("temp.csv")
        CheckNumbers("temp.csv")
        ChangeChannelData("temp.csv")
        if (args.output):
            uprint("Export the TVHeadend Channels to Enigma2 files " + str(args.output) + ".tv / " + str(args.output) + ".radio")
            Enigma2Ouput(str(args.output), dChannels)
        else:
            uprint("Export the TVHeadend Channels to Enigma2 files temp.tv / temp.radio")
            Enigma2Ouput("temp", dChannels)
    if (args.export):
        uprint("Export the TVHeadend Channels to " + str(args.export))
        dChannels = ExportChannelData(args.export)
        if (args.output):
            uprint("Export the TVHeadend Channels to Enigma2 files " + str(args.output) + ".tv / " + str(args.output) + ".radio")
            Enigma2Ouput(str(args.output), dChannels)
    if (args.change):
        uprint("Change the TVHeadend Channel Numbers and Tags from " + str(args.change))
        CheckNumbers(args.change)
        dChannels = ChangeChannelData(args.change)
        if (args.output):
            uprint("Export the TVHeadend Channels to Enigma2 files " + str(args.output) + ".tv / " + str(args.output) + ".radio")
            Enigma2Ouput(str(args.output), dChannels)

