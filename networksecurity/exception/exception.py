import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name {self.filename} line number {self.lineno} error message {self.error_message}"
    
if __name__=="__main__":
    try:
        logger.logging.info("Logging starte")
        a=1/0
        print("THis will not be printed",a)
        logger.logging.info("Logging COmpleted")
    except Exception as e:
        logger.logging.info("Something went wrong")
        raise NetworkSecurityException(e,sys)
