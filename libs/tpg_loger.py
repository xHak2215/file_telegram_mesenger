import sys
import datetime
import traceback


def write_to_log_file(file, t):
    with open(file, 'a', buffering=1) as f:
        f.write(t+'\n')  

class logse:
    def __init__(self):
        self.file='log.log'
        self.level=2
        self.seve_log_file=True
        self.patern=f"{datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")} |{sys._getframe(1).f_locals['__file__']}| line:{traceback.extract_stack()[-2].lineno} |"
        
        # color
        self.color_green='\33[32m'
        self.color_red='\33[31m'
        self.color_yelow='\33[33m'
    
    def info(self, text, info_patern='info: ', end='\033[0m'):
        if self.level>=0:
            print(self.patern+f"{info_patern}{str(text)}{end}")
        
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"{info_patern}{str(text)}")    
                
    def warning(self, text, warning_patern=f"warning: ", end='\033[0m'):
        if self.level>=1:
            print(self.patern+f"{self.color_yelow}{warning_patern}{str(text)}{end}")
            
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"{warning_patern}{str(text)}")    
        
    def error(self, text, error_patern=f"ERROR: ", end='\033[0m'):
        if self.level>=2:
            print(self.patern+f"{self.color_red}{error_patern}{str(text)}{end}")
            
            if self.seve_log_file:
                write_to_log_file(self.file, self.patern+f"{error_patern}{str(text)}")