import logging
import logging.config
import os.path
import time


class Logger():
    def __init__(self,save_dir='./',log_step=1,level='INFO'):

        self.log_step=log_step

        log_path=os.path.join(save_dir,'log.txt')
        #
        if not os.path.exists(log_path):
            os.makedirs(save_dir,exist_ok=True)
            self.log_file=open(log_path,'w+')
        self.log_file=open(log_path,'a+')

    def preprocess_msg(self,msg):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg = f"[{time_str}] {msg}\n"
        return msg
    def print(self,msg):
        msg=self.preprocess_msg(msg)
        print(msg)

    def write_log(self,msg):

        msg=self.preprocess_msg(msg)
        self.log_file.write(msg)
        self.log_file.flush()

    def print_write_log(self,msg):
        msg=self.print(msg)
        self.write_log(msg)
