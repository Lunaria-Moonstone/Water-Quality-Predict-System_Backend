# import env
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))

from flask import Flask
from flask_cors import CORS # Cross Range

from routes.user import user_route
from routes.sample import sample_route
from conn.connection_pool import connection_pool 
from utils.logging import LoggingHandler

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(user_route)
app.register_blueprint(sample_route)

logging_handler = LoggingHandler()
app.logger.addHandler(logging_handler.getHandler())

conn = connection_pool.get_conn()

if __name__ == '__main__':
	app.run(port=8091)