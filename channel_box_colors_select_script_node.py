from maya import cmds

def channelColorData():
    if cmds.objExists("channelColorData"):
        print("Node Exists")
        channelBoxColorsData = "channelColorData"
        return channelBoxColorsData
    else:
        channelBoxColorsData = cmds.scriptNode(n="channelColorData", st=1)
        cmds.setAttr("channelColorData.sourceType", 1)
        return channelBoxColorsData
        
channelColorData()
cmds.select("channelColorData")        
        