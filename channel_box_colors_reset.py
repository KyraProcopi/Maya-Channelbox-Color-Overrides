#Global Variables 
main_channelbox_name = "mainChannelBox"
node_data_code = "main_channelbox_name = " + """'mainChannelBox'"""

code = node_data_code
cmds.scriptNode("channelColorData", edit=True, bs=code)