import os
import platform

if platform.system()=='Windows':
    os.system('color')

cc_red='\33[91m'
cc_green='\33[92m'
cc_yellow='\33[93m'
cc_darkblue='\33[94m'
cc_pink='\33[95m'
cc_lightblue='\33[96m'
cc_default='\033[0m'

def clear():
    if platform.system()=='Windows':
        os.system('cls')
    else:
        os.system('clear')
