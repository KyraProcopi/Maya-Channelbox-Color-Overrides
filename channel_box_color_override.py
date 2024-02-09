from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import cmds, OpenMayaUI

#Global Variables 
main_channelbox_name = "mainChannelBox"
node_data_code = "main_channelbox_name = " + """'mainChannelBox'"""

#Change channel BG box color
def channelBoxColorOverride(code):
    
    #Find pyside widget
    channelbox_widget = wrapInstance(int(OpenMayaUI.MQtUtil.findControl(main_channelbox_name)),QtWidgets.QWidget)
    selected_attributes = cmds.channelBox(main_channelbox_name, q=True, sma=True)
    
    #Script Node
    if cmds.objExists("channelColorData"):
        channelBoxColorsData = "channelColorData"
    else:
        channelBoxColorsData = cmds.scriptNode(n="channelColorData", st=1)
        cmds.setAttr("channelColorData.sourceType", 1)
    
    #Change Color
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

        else:
            print('Editor was dismissed')
                      
    #Plug Code intro Script Node 
    if cmds.objExists("channelColorData"):
        code = cmds.scriptNode("channelColorData", bs=True, q=True)
    
    if color_data != None:
        try:
            code += "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)
            
        except:
            code = node_data_code + "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)
                          
#Select Script Node
def channelColorData(code):
    if cmds.objExists("channelColorData"):
        print("Node Exists")
        channelBoxColorsData = "channelColorData"
        cmds.select("channelColorData")
        return channelBoxColorsData
    else:
        print("Script node has not been created. Please apply color overrides to create script node")

#Get Exsiting data         
def get_existing_data(code):
    if cmds.objExists("channelColorData"):
        code = cmds.scriptNode("channelColorData", bs=True, q=True)
        print("Exisiting Override Data retrieved") 
        return code
    else:
        print("No existing data")        

#Reset Overrides
def reset(code):
    if cmds.objExists("channelColorData"):
        code = node_data_code
        cmds.scriptNode("channelColorData", edit=True, bs=code)
        print("Overrides restored to default. Please close Maya and re-open")
    
    else:
        print("Script node has not been created. Please apply color overrides to create script node")
                

#UI
cmds.window(menuBar=True, width=255, h=50, s=False)
cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )
cmds.button('Change Color', c=channelBoxColorOverride)
cmds.button('Select Script Node', c=channelColorData)
cmds.button('Get Existing Data', c=get_existing_data)
cmds.button('Reset All Overrides',c=reset)
cmds.showWindow()
