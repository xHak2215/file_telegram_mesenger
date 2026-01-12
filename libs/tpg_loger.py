# __ logse from https://github.com/xHak2215/tpg/blob/main/tpg/tpg.py __ #

import sys
from datetime import datetime
import os
import inspect


def write_to_log_file(file, t ,path_save_log):
    if path_save_log:
        path=os.path.join(path_save_log, file)
    else:
        path=file
    with open(path, 'a', buffering=1) as f:
        f.write(t+'\n')        

class logse:
    def __init__(self, file:str='log.log', level:int=2, seve_log_file:bool=True, path_save_log:str|None=None):
        self.file=file
        self.level=level
        self.seve_log_file=seve_log_file
        self.patern=f"{datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")} |{sys._getframe(1).f_locals['__file__']}| "
        self.path_save_log=path_save_log
        
        # color
        self.color_green='\33[32m'
        self.color_red='\33[31m'
        self.color_yelow='\33[33m'
    
    def info(self, text, info_patern=f"info: ", end='\033[0m'):
        if self.level>=0:
            print(self.patern+f"{self.color_green}line:{inspect.stack()[1][2]} |{info_patern}{str(text)}{end}")
        
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"line:{inspect.stack()[1][2]} |{info_patern}{str(text)}", self.path_save_log)    
                
    def warning(self, text, warning_patern=f"warning: ", end='\033[0m'):
        if self.level>=1:
            print(self.patern+f"{self.color_yelow}line:{inspect.stack()[1][2]} |{warning_patern}{str(text)}{end}")
            
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"line:{inspect.stack()[1][2]} |{warning_patern}{str(text)}", self.path_save_log)    
        
    def error(self, text, error_patern=f"ERROR: ", end='\033[0m'):
        if self.level>=2:
            print(self.patern+f"{self.color_red}line:{inspect.stack()[1][2]} |{error_patern}{str(text)}{end}")
            
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"line:{inspect.stack()[1][2]} |{error_patern}{str(text)}", self.path_save_log)
        
