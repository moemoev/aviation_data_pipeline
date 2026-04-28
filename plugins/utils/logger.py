import logging

def setup_logger(name: str = "ETL") -> logging.Logger:
    """
    Setup logger for ETL logging
    """
    logger = logging.getLogger(name)


    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

    return logger