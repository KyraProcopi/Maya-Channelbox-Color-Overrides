from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import cmds, OpenMayaUI

#Global Variables 
main_channelbox_name = "mainChannelBox"
node_data_code = "main_channelbox_name = " + """'mainChannelBox'"""

def channelColorData():
    if cmds.objExists("channelColorData"):
        channelBoxColorsData = "channelColorData"
        return channelBoxColorsData
    else:
        channelBoxColorsData = cmds.scriptNode(n="channelColorData", st=1)
        cmds.setAttr("channelColorData.sourceType", 1)
        return channelBoxColorsData 

def get_existing_data():
    if cmds.objExists("channelColorData"):
        get_existing_data = cmds.scriptNode("channelColorData", bs=True, q=True)
        return get_existing_data 

#Change channel BG box color
def channelBoxColorOverride():
    #Find pyside widget
    channelbox_widget = wrapInstance(int(OpenMayaUI.MQtUtil.findControl(main_channelbox_name)),QtWidgets.QWidget)
    selected_attributes = cmds.channelBox(main_channelbox_name, q=True, sma=True)
   
    def color_change(selected_attribute):
        cmds.channelBox(
        main_channelbox_name,
        edit=True,
        attrRegex=(selected_attribute),
        attrBgColor=values
        )
        color_data = ("cmds.channelBox(" +
            "main_channelbox_name," +
            "edit=True," +
            """attrRegex='{}',""".format(selected_attribute) +
            """attrBgColor={})""".format(values)+ """\n""") 
        color_data_code = str(color_data)
        print(color_data_code)
        return color_data_code  
   
    if selected_attributes==None:
        print("Please select attributes in channel box")
        
    else:
        #Color Editor 
        cmds.colorEditor()
        if cmds.colorEditor(query=True, result=True):
            values = cmds.colorEditor(query=True, rgb=True)  
            #Loop through 
            color_output = str()
            color_data = color_output.join(color_change(attr)for attr in selected_attributes)
            return color_data

        else:
            print('Editor was dismissed')
                      
#Plug Code intro Script Node
channelColorData()  
color_data = channelBoxColorOverride()

if isinstance(color_data, str):
    try:
        code += "\n" + color_data
        cmds.scriptNode("channelColorData", edit=True, bs=code)
        
    except:
        if get_existing_data != ():
            code = str(get_existing_data()) + "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)
        else:  
            code = node_data_code + "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)