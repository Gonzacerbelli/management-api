from flask import Flask, request, Response
from flask_cors import CORS
import json
import logging
import jwt

from database import db_session
from config import get_env_vars


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.before_request
def check_authentication():
    try:
        if request.path not in get_env_vars("PUBLIC_ROUTES"):
            print('llego')
            if request.headers.get('Authorization') is None:
                return Response(json.dumps({"error": 'Missing authorization token'}), status=401, mimetype='application/json')

            access_token = request.headers.get('Authorization')
            jwt.decode(access_token.split(" ")[1], get_env_vars("JWT_PUBLIC_KEY"), options={
                       "verify_signature": True}, algorithms=["RS256"])
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=401, mimetype='application/json')


@app.teardown_appcontext
def shutdown_session(Error=None):
    db_session.remove()


if __name__ == '__main__':
    logging.basicConfig()
    app.run(debug=True)
