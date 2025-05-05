import logging  
import json  
from datetime import datetime  
import os  
  
def setup_logging(log_level=logging.INFO, log_file=None):  
    """  
    Configure le système de logging avec formatage avancé  
    """  
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  
      
    # Configuration de base  
    logging.basicConfig(  
        level=log_level,  
        format=log_format  
    )  
      
    # Ajout d'un handler de fichier si spécifié  
    if log_file:  
        file_handler = logging.FileHandler(log_file)  
        file_handler.setFormatter(logging.Formatter(log_format))  
        logging.getLogger().addHandler(file_handler)  
  
class JSONLogger:  
    """  
    Logger qui produit des logs au format JSON pour intégration avec des outils d'analyse  
    """  
    def __init__(self, name, log_dir="logs"):  
        self.logger = logging.getLogger(name)  
          
        # Création du répertoire de logs si nécessaire  
        os.makedirs(log_dir, exist_ok=True)  
          
        # Fichier de log JSON  
        log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.json")  
          
        # Handler pour le fichier JSON  
        self.json_handler = logging.FileHandler(log_file)  
        self.json_handler.setFormatter(logging.Formatter("%(message)s"))  
        self.logger.addHandler(self.json_handler)  
      
    def log(self, level, message, **kwargs):  
        """  
        Enregistre un message avec des métadonnées supplémentaires au format JSON  
        """  
        log_data = {  
            "timestamp": datetime.now().isoformat(),  
            "level": logging.getLevelName(level),  
            "message": message,  
            **kwargs  
        }  
          
        self.json_handler.emit(logging.LogRecord(  
            name=self.logger.name,  
            level=level,  
            pathname="",  
            lineno=0,  
            msg=json.dumps(log_data),  
            args=(),  
            exc_info=None  
        ))  
          
        # Log également au format standard  
        if level == logging.DEBUG:  
            self.logger.debug(message)  
        elif level == logging.INFO:  
            self.logger.info(message)  
        elif level == logging.WARNING:  
            self.logger.warning(message)  
        elif level == logging.ERROR:  
            self.logger.error(message)  
        elif level == logging.CRITICAL:  
            self.logger.critical(message)