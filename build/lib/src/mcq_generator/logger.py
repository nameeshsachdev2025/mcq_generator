#file for saving the logs 
import logging,os
from datetime import datetime
Log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"#.log is a type of file
log_path=os.path.join(os.getcwd(),"logs")#cwd is current working directory ,making new dir and joining path for the folder
os.makedirs(log_path,exist_ok=True)

Log_file_path=os.path.join(log_path,Log_file)

logging.basicConfig(level=logging.INFO,#level is ,till where we want the info ,like all the warnings etc 
        filename=Log_file_path,
        format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s -%(message)s"
)
