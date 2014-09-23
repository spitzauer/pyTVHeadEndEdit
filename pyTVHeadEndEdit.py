import os, sys, argparse
g_ChannelDir  = "channels"
g_ChannelFile = "channels.csv"
g_ChannelKeys = {"name" : "", "icon" : "", "tags" : "", "dvr_extra_time_pre" : "", "dvr_extra_time_post" : "", "channel_number" : ""}

def dprint(str):
    if _debug_:
        print("DEBUG:   " + str)


def eprint(str):
    print("ERROR:   " + str)
    sys.exit(-1)


def wprint(str):
    print("WARNING: " + str)


def readChannels():
    ChannelFiles = os.listdir(g_ChannelDir)
    ChannelDict = {}
    for ChannelFile in ChannelFiles:
        dprint("open file: " + g_ChannelDir + os.sep + ChannelFile)
        ChannelFileFH = open(g_ChannelDir + os.sep + ChannelFile)
        ChannelFileContent = ChannelFileFH.readlines()
        ChannelFileFH.close()
        Line = ""
        for ChannelFileLine in ChannelFileContent:
            Line = Line + ChannelFileLine.replace("\n", "")
        for ChannelKey in g_ChannelKeys:
            KeyValue = ""
            ChannelKeyStr = "\"" + ChannelKey + "\": "
            if Line.find(ChannelKeyStr) != -1:
                temp , Content = Line.split(ChannelKeyStr)
                if Content.find(",") == -1:
                    KeyValue = Content[:Content.find("}")]
                else:
                    if Content.find("[") != -1:
                        if Content.find(",") < Content.find("["):
                            KeyValue = Content[:Content.find(",")]
                        else:
                            KeyValue = Content[Content.find("[")+1:Content.find("]")]
                            KeyValue = KeyValue.replace("	", "")
                    else:
                        KeyValue = Content[:Content.find(",")]
            g_ChannelKeys[ChannelKey] = KeyValue.replace("\"", "")
        ChannelFileContent = g_ChannelKeys["name"] + ";" + g_ChannelKeys["icon"] + ";" + g_ChannelKeys["tags"] + ";" + \
                             g_ChannelKeys["dvr_extra_time_pre"] + ";" + g_ChannelKeys["dvr_extra_time_post"] + ";" + g_ChannelKeys["channel_number"]
        ChannelDict.update({ChannelFile : ChannelFileContent})
    return ChannelDict


def readChannelFile():
    ChannelFileFH = open(g_ChannelFile)
    ChannelFileContent = ChannelFileFH.readlines()
    ChannelFileFH.close()
    ChannelFileDict = {}
    i = 0
    for ChannelFileLine in ChannelFileContent:
        if ChannelFileLine.find("#") != 0:
            if ChannelFileLine.count(";") == 4:
                i = i + 1
                ChannelName, ChannelIcon, ChannelTags, ChannelPre, ChannelPost = ChannelFileLine.split(";")
                ChannelPost = ChannelPost.replace("\n", "")
                ChannelFileDict.update({ChannelName : ChannelIcon + ";" + ChannelTags + ";" + ChannelPre + ";" + ChannelPost + ";" + str(i)})
            else:
                eprint(g_ChannelFile + " has at least one syntax error. (One line must have four \";\")")
    return ChannelFileDict


def printChannels(p_dChannelDict):
    ChannelSort = {}
    for Channel in p_dChannelDict:
        ChannelData = "\n===============================================================================" + \
                      "\nChannel File Name: " + Channel + " " + \
                      "\n-------------------------------------------------------------------------------" + \
                      "\nChannel Name:          " + getChannelKeyValue(p_dChannelDict[Channel], "name") + " " + \
                      "\nChannel Icon:          " + getChannelKeyValue(p_dChannelDict[Channel], "icon") + " " + \
                      "\nChannel Tags:          " + getChannelKeyValue(p_dChannelDict[Channel], "tags") + " " + \
                      "\nChannel DVR Pre Time:  " + getChannelKeyValue(p_dChannelDict[Channel], "dvr_extra_time_pre") + " " + \
                      "\nChannel DVR Post Time: " + getChannelKeyValue(p_dChannelDict[Channel], "dvr_extra_time_post") + " " + \
                      "\nChannel Number:        " + getChannelKeyValue(p_dChannelDict[Channel], "channel_number") + " "
        ChannelFile = Channel
        if len(ChannelFile) == 1:
            ChannelFile = "00000" + ChannelFile
        elif len(ChannelFile) == 2:
            ChannelFile = "0000" + ChannelFile
        elif len(ChannelFile) == 3:
            ChannelFile = "000" + ChannelFile
        elif len(ChannelFile) == 4:
            ChannelFile = "00" + ChannelFile
        elif len(ChannelFile) == 5:
            ChannelFile = "0" + ChannelFile
        ChannelSort.update({ChannelFile : ChannelData})
    for channel in sorted(ChannelSort):
        print(ChannelSort[channel])


def printChannelsCsv(p_dChannelDict):
    ChannelSort = {}
    i = 0
    for Channel in p_dChannelDict:
        ChannelData = getChannelKeyValue(p_dChannelDict[Channel], "name") + ";" + getChannelKeyValue(p_dChannelDict[Channel], "icon") + ";" + \
              getChannelKeyValue(p_dChannelDict[Channel], "tags") + ";" + getChannelKeyValue(p_dChannelDict[Channel], "dvr_extra_time_pre") + ";" + \
              getChannelKeyValue(p_dChannelDict[Channel], "dvr_extra_time_post")
        if getChannelKeyValue(p_dChannelDict[Channel], "channel_number") == "0":
            i = i + 1
            ChannelSort.update({"z_" + str(i) : ChannelData})
        else:
            ChannelNumber = getChannelKeyValue(p_dChannelDict[Channel], "channel_number")
            if len(ChannelNumber) == 1:
                ChannelNumber = "00000" + ChannelNumber
            elif len(ChannelNumber) == 2:
                ChannelNumber = "0000" + ChannelNumber
            elif len(ChannelNumber) == 3:
                ChannelNumber = "000" + ChannelNumber
            elif len(ChannelNumber) == 4:
                ChannelNumber = "00" + ChannelNumber
            elif len(ChannelNumber) == 5:
                ChannelNumber = "0" + ChannelNumber
            ChannelSort.update({ChannelNumber : ChannelData})
    for channel in sorted(ChannelSort):
        print(ChannelSort[channel])


def getChannelKeyValue(p_sChannelContent, p_sKey):
    if p_sChannelContent.count(";") != 5:
        eprint("Wrong input format in getChannelKeyValue")
    g_ChannelKeys["name"], g_ChannelKeys["icon"], g_ChannelKeys["tags"], g_ChannelKeys["dvr_extra_time_pre"], g_ChannelKeys["dvr_extra_time_post"], g_ChannelKeys["channel_number"] = p_sChannelContent.split(";")
    return g_ChannelKeys[p_sKey]


def insertChannelFiles(p_dChannelDict, p_dChannelsFile):
    dprint("If channel files are missing add them from the csv file data.")
    for ChannelsLine in p_dChannelsFile:
        ChannelFound = 0
        MaxFileName = 0
        for Channel in p_dChannelDict:
            if MaxFileName < int(Channel):
                MaxFileName = int(Channel)
            if getChannelKeyValue(p_dChannelDict[Channel], "name") == ChannelsLine:
                ChannelFound = ChannelFound + 1
        if ChannelFound == 0:
            MaxFileName = MaxFileName + 1
            dprint("Write Channel File \"" + g_ChannelDir + os.sep + str(MaxFileName) + "\"")
            ChannelIcon, ChannelTags, ChannelPre, ChannelPost, ChannelNumber = p_dChannelsFile[ChannelsLine].split(";")
            ChannelFileContent = ChannelsLine + ";" + ChannelIcon + ";" + ChannelTags + ";" + ChannelPre + ";" + ChannelPost + ";" + ChannelNumber
            p_dChannelDict.update({str(MaxFileName) : ChannelFileContent})
            writeChannelFile(g_ChannelDir + os.sep + str(MaxFileName), ChannelsLine, ChannelIcon, ChannelTags, ChannelPre, ChannelPost, ChannelNumber)


def parseChannelFiles(p_dChannelDict, p_sChannelsFileContent):
    Error = False
    for ChannelsLine in p_sChannelsFileContent:
        ChannelFound = 0
        for Channel in p_dChannelDict:
            if getChannelKeyValue(p_dChannelDict[Channel], "name") == ChannelsLine:
                ChannelFound = ChannelFound + 1
                dprint("Channel \"" + ChannelsLine + "\" is in File \"" + Channel + "\" defined.")
        if ChannelFound == 0:
            Error = 1
            wprint("Channel \"" + ChannelsLine + "\" not found in channel files.")
        if ChannelFound > 1:
            Error = 1
            wprint("Channel \"" + ChannelsLine + "\" found in " + str(ChannelFound) + " files.")
    return Error


def deleteChannelFiles(p_dChannelDict, p_dChannelFileDictKeys):
    dprint("Deleting channel files which are not defined in the csv file.")
    if parseChannelFiles(p_dChannelDict, p_dChannelFileDictKeys):
        eprint("Solve Warnings before deleting channel Files")
    else:
        ChannelDictDel = p_dChannelDict.copy()
        for Line in ChannelDictDel:
            ChannelDictDel[Line] = False
        for ChannelFileLine in p_dChannelDict:
            for ChannelsLine in p_dChannelFileDictKeys:
                if getChannelKeyValue(p_dChannelDict[ChannelFileLine], "name") == ChannelsLine:
                    ChannelDictDel[ChannelFileLine] = True
        for Line in ChannelDictDel:
            if ChannelDictDel[Line] == False:
                del p_dChannelDict[Line]
                os.remove(g_ChannelDir + os.sep + Line)


def writeChannelFile(p_sChannelFileName, p_sChannelName, p_sChannelIcon, p_sChannelTags, p_sChannelPre, p_sChannelPost, p_sChannelNumber):
    ChannelFileFH = open(p_sChannelFileName, "w")
    ChannelFileFH.write("{\n")
    ChannelFileFH.write("	\"name\": \"" + p_sChannelName + "\",\n")
    if p_sChannelIcon != "":
        ChannelFileFH.write("	\"icon\": \"" + p_sChannelIcon + "\",\n")
    if p_sChannelTags != "":
        ChannelFileFH.write("	\"tags\": [\n")
        CountTags = p_sChannelTags.count(",")
        if CountTags == 0:
            ChannelFileFH.write("		" + p_sChannelTags + "\n")
        else:
            Tags = p_sChannelTags.split(",")
            for x in range(0, CountTags):
                ChannelFileFH.write("		" + Tags[x] + ",\n")
            ChannelFileFH.write("		" + Tags[CountTags] + "\n")
        ChannelFileFH.write("	],\n")
    ChannelFileFH.write("	\"dvr_extra_time_pre\": " + p_sChannelPre + ",\n")
    ChannelFileFH.write("	\"dvr_extra_time_post\": " + p_sChannelPost + ",\n")
    ChannelFileFH.write("	\"channel_number\": " + p_sChannelNumber + "\n")
    ChannelFileFH.write("}\n")
    ChannelFileFH.close()


def changeChannelFiles(p_dChannels, p_dChannelFile):
    dprint("Update the channels files from the csv file.")
    for Files in p_dChannels:
        if getChannelKeyValue(p_dChannels[Files], "name").replace("\"", "") in p_dChannelFile:
            NewChannelValues = p_dChannelFile[getChannelKeyValue(p_dChannels[Files], "name").replace("\"", "")]
            ChannelNumber, ChannelIcon, ChannelTags = NewChannelValues.split(";")
            if ChannelIcon == "":
                ChannelIcon = getChannelKeyValue(p_dChannels[Files], "icon")
            if ChannelTags == "":
                ChannelTags = getChannelKeyValue(p_dChannels[Files], "tags")
            writeChannelFile(g_ChannelDir + os.sep + Files, getChannelKeyValue(p_dChannels[Files], "name"), ChannelIcon, ChannelTags, getChannelKeyValue(p_dChannels[Files], "dvr_extra_time_pre"), getChannelKeyValue(p_dChannels[Files], "dvr_extra_time_post"), ChannelNumber)
            ChannelFileFH = open(g_ChannelDir + os.sep + Files, "w")
            ChannelFileFH.write("{\n")
            ChannelFileFH.write("	\"name\": \"" + getChannelKeyValue(p_dChannels[Files], "name") + "\",\n")
            if ChannelIcon != "":
                ChannelFileFH.write("	\"icon\": \"" + ChannelIcon + "\",\n")
            if ChannelTags != "":
                ChannelFileFH.write("	\"tags\": [\n")
                CountTags = ChannelTags.count(",")
                if CountTags == 0:
                    ChannelFileFH.write("		" + ChannelTags + "\n")
                else:
                    Tags = ChannelTags.split(",")
                    for x in range(0, CountTags):
                        ChannelFileFH.write("		" + Tags[x] + ",\n")
                    ChannelFileFH.write("		" + Tags[CountTags] + "\n")
                ChannelFileFH.write("	],\n")
            ChannelFileFH.write("	\"dvr_extra_time_pre\": " + getChannelKeyValue(p_dChannels[Files], "dvr_extra_time_pre") + ",\n")
            ChannelFileFH.write("	\"dvr_extra_time_post\": " + getChannelKeyValue(p_dChannels[Files], "dvr_extra_time_post") + ",\n")
            ChannelFileFH.write("	\"channel_number\": " + ChannelNumber + "\n")
            ChannelFileFH.write("}\n")
            ChannelFileFH.close()


def sortChannelFiles(p_dDictChannels):
    wprint("TODO sortChannelFiles()")


parser = argparse.ArgumentParser(description="TVHeadEnd Channel Editor. With the help of an input csv file you can sort the channels in the channel folder.")
parser.add_argument("-i", "--input",     help="input csv file (default: \"channels.csv\")")
parser.add_argument("-d", "--directory", help="directory of the channel folder (default: \"channels\")")
parser.add_argument("-o", "--output",    help="csv output of the channels", action="store_true")
parser.add_argument("-p", "--print_",    help="print the channels", action="store_true")
parser.add_argument("-a", "--add",       help="add channels from csv file", action="store_true")
parser.add_argument("-r", "--remove",    help="remove unused channels from csv file", action="store_true")
parser.add_argument("-u", "--update",    help="update channels from csv file", action="store_true")
parser.add_argument("-s", "--sort",      help="sort channel files", action="store_true")
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
args = parser.parse_args()


_debug_ = args.verbosity
if args.input != None:
    g_ChannelFile = args.input
if os.path.isfile(g_ChannelFile) == False:
    eprint("File \"" + g_ChannelFile + "\" does not exist.")
if args.directory != None:
    g_ChannelDir = args.directory
if (os.path.isfile(g_ChannelDir) == True) and (os.path.exists(g_ChannelDir) == False):
    eprint("Directory \"" + g_ChannelDir + "\" does not exist.")
DictChannels = readChannels()
DictChannelFile = readChannelFile()

if (args.output == False) and (args.print_ == False) and (args.add == False) and (args.remove == False) and (args.update == False) and (args.sort == False):
    insertChannelFiles(DictChannels, DictChannelFile)
    deleteChannelFiles(DictChannels, DictChannelFile.keys())
    changeChannelFiles(DictChannels, DictChannelFile)
    sortChannelFiles(DictChannels)
else:
    if args.output == True:
        printChannelsCsv(DictChannels)
    
    if args.print_ == True:
        printChannels(DictChannels)
    
    if args.add == True:
        insertChannelFiles(DictChannels, DictChannelFile)
    
    if args.remove == True:
        deleteChannelFiles(DictChannels, DictChannelFile.keys())
    
    if args.update == True:
        changeChannelFiles(DictChannels, DictChannelFile)
    
    if args.sort == True:
        sortChannelFiles(DictChannels)
