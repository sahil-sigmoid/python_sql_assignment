import psycopg2
import logging
from config import config
from sqlalchemy import create_engine
class Connection:
    def start_connection(self):
        try:
            conn = psycopg2.connect(
                database="pythonAssignment", user='postgres', password='12345qwerty@SS', host='127.0.0.1', port='5432'
            )
            return conn
        except:
            logging.error("error in connection")
            raise Exception("Database can not connected")
        finally:
            logging.info(" Database connected successfully")

    def get_engine(self):
        try:
            params = config()
            engine = create_engine(**params)
            return engine
        except:
            logging.error("Error in engine creation")
        finally:
            logging.info("Engine successfully created")

