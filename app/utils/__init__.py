from utils.logging_utils import setup_logging  
import logging  
import os  
  
# Configuration globale du logging  
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")  
os.makedirs(log_dir, exist_ok=True)  
log_file = os.path.join(log_dir, "mcp_server.log")  
  
setup_logging(  
    log_level=logging.INFO if not os.getenv("DEBUG") else logging.DEBUG,  
    log_file=log_file  
)