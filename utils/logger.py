import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """Set up the application logger."""
    log_dir = os.path.join(app.root_path, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'roadfix.log')
    
    # Create a rotating file handler (max 5MB, keep 5 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    
    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Set the log level based on environment
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    file_handler.setLevel(log_level)
    
    # Add handler to the app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    
    app.logger.info("RoadFix LK startup completed. Logging is configured.")
    return app.logger
