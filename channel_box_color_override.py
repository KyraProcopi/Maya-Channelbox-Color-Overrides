from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import cmds, OpenMayaUI

#Global Variables 
main_channelbox_name = "mainChannelBox"
node_data_code = "main_channelbox_name = " + """'mainChannelBox'"""

def channelColorData():
    if cmds.objExists("channelColorData"):
        print("Node Exists")
        channelBoxColorsData = "channelColorData"
        return channelBoxColorsData
    else:
        channelBoxColorsData = cmds.scriptNode(n="channelColorData", st=1)
        cmds.setAttr("channelColorData.sourceType", 1)
        return channelBoxColorsData 

def channelBoxColorOverride():
    #Find pyside widget
    channelbox_widget = wrapInstance(int(OpenMayaUI.MQtUtil.findControl(main_channelbox_name)),QtWidgets.QWidget)
    selected_attributes = cmds.channelBox(main_channelbox_name, q=True, sma=True)
   
    if selected_attributes==None:
        print("Please select attributes in channel box")
        
    else:
        #Color Editor 
        cmds.colorEditor()
        if cmds.colorEditor(query=True, result=True):
            values = cmds.colorEditor(query=True, rgb=True)
            #Change channel BG box color
            for selected_attribute in selected_attributes:
                cmds.channelBox(
                main_channelbox_name,
                edit=True,
                attrRegex=(selected_attribute),
                attrBgColor=values
                )
                color_data_code = ("cmds.channelBox(" +
                    "main_channelbox_name," +
                    "edit=True," +
                    """attrRegex='{}',""".format(selected_attribute) +
                    """attrBgColor={})""".format(values)) 
            return color_data_code 
        
        else:
            print('Editor was dismissed')
                      
#Plug Code intro Script Node
channelColorData()  
color_data = channelBoxColorOverride()
    
if color_data != None:
    try:
        code += "\n" + color_data
        cmds.scriptNode("channelColorData", edit=True, bs=code)
        
    except:
        code = node_data_code
        cmds.scriptNode("channelColorData", edit=True, bs=code)
