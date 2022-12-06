from flask import current_app as app
from flask import request, Response
import json
from datetime import datetime

from database import db_session, Clients
from mappers import client_mapper


@app.route("/clients", methods=["POST"])
def create_client():
    try:
        response = None

        name = request.form.get("name")
        email = request.form.get("email")
        document = int(request.form.get("document"))
        phone = int(request.form.get("phone"))
        address = request.form.get("address")
        city = request.form.get("city")
        birthday = datetime.strptime(request.form.get("birthday"), '%d/%m/%Y')
        sex = request.form.get("sex")

        existing_client = Clients.query.filter_by(document=document).first()

        if (existing_client):
            response = Response('Client with document {} already exists'.format(
                document), status=409, mimetype='application/json')
        else:
            client = Clients(name=name, email=email, document=document, phone=phone,
                             address=address, city=city, birthday=birthday, sex=sex)

            db_session.add(client)
            db_session.commit()

            client_registered = Clients.query.filter_by(
                document=document).first()

            response = Response('Client with document {} created successfully'.format(
                client_registered.document), status=201, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/client/<id>", methods=["GET"])
def get_client(id):
    try:
        return Response(json.dumps(client_mapper(Clients.query.get(id))), status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/clients", methods=["GET"])
def get_clients():
    try:
        clients = Clients.query.all()
        response = []
        for client in clients:
            response.append(client_mapper(client))
        return Response(json.dumps(response), status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')