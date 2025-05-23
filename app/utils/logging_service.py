from    config import config

import  json
import  sys
from    pathlib import Path
from    typing import Dict, Any, Optional
from    datetime import datetime

import  logging
from    logging.handlers import RotatingFileHandler



class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            **getattr(record, "metadata", {})
        }
        return json.dumps(log_entry, ensure_ascii=False)

class LoggingService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._configure_logging()
    
    def _configure_logging(self):
        LOG_DIR = Path(config.LOGGING_DIR)
        LOG_DIR.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=config.SERVER_LOG_LEVEL.upper(),
            handlers=[
                RotatingFileHandler(
                    LOG_DIR/"application.log",
                    maxBytes=config.LOGGING_MAX_SIZE*1024*1024,
                    backupCount=config.LOGGING_BACKUP_COUNT,
                    encoding=config.LOGGING_ENCODING
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Handler JSON
        json_handler = RotatingFileHandler(
            LOG_DIR/"structured_logs.json",
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        json_handler.setFormatter(JSONFormatter())
        
        # Appliquer à tous les loggers existants et futurs
        root_logger = logging.getLogger()
        root_logger.addHandler(json_handler)
        
        # Configurer le encoding pour stdout/stderr
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    def get_logger(self, name: str) -> logging.Logger:
        """Retourne un logger configuré"""
        return logging.getLogger(name)
    
    def log_structured(self,
                     level: int,
                     message: str,
                     module: str,
                     metadata: Optional[Dict[str, Any]] = None):
        """
        Log structuré avec métadonnées
        """
        logger = self.get_logger(module)
        extra = {"metadata": metadata} if metadata else {}
        
        if level == logging.DEBUG:
            logger.debug(message, extra=extra)
        elif level == logging.INFO:
            logger.info(message, extra=extra)
        elif level == logging.WARNING:
            logger.warning(message, extra=extra)
        elif level == logging.ERROR:
            logger.error(message, extra=extra)
        elif level == logging.CRITICAL:
            logger.critical(message, extra=extra)