import logging

def configure_logger():
    # Configure the logger
    logging.basicConfig(
        filename='logs/app.log', 
        filemode='w', 
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )

    # Create and return a logger
    return logging.getLogger(__name__)