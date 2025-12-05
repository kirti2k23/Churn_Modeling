import logging
from datetime import datetime
import os

Log_File = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_path = os.path.join(os.getcwd(),"Logs")
os.makedirs(log_path, exist_ok = True)

Log_File_Path = os.path.join(log_path,Log_File)

logging.basicConfig(
    filename= Log_File_Path,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

if __name__ == "__main__":
    logging.info("Logging started")