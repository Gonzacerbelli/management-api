from flask import Flask, request, Response
from flask_cors import CORS
from sqlalchemy import or_, and_
from datetime import datetime
import json
import logging
import jwt
import time

from database import db_session, Users, Clients, Visits, Products
from config import get_env_vars
from mappers import *


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.before_request
def check_authentication():
    try:
        if request.path not in get_env_vars("PUBLIC_ROUTES"):
            if request.headers.get('Authorization') is None:
                return Response(json.dumps({"error": 'Missing authorization token'}), status=401, mimetype='application/json')

            access_token = request.headers.get('Authorization')
            jwt.decode(access_token.split(" ")[1], get_env_vars("JWT_PUBLIC_KEY"), options={
                       "verify_signature": True}, algorithms=["RS256"])
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=401, mimetype='application/json')


@app.route("/signup", methods=["POST"])
def signup():
    try:
        response = None

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = Users.query.filter(
            or_(Users.username == username, Users.email == email)).first()

        if (existing_user):
            response = Response('User with username {} or email {} already exists'.format(
                username, email), status=409, mimetype='application/json')
        else:
            user = Users(email=email, password=password, username=username)

            db_session.add(user)
            db_session.commit()

            user_registered = Users.query.filter(
                or_(Users.username == username, Users.email == email)).first()

            response = Response('User with username {} and email {} created successfully'.format(
                user_registered.username, user_registered.email), status=201, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/signin", methods=["POST"])
def signin():
    try:
        response = None

        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = Users.query.filter(
            and_(Users.username == username, Users.password == password)).first()

        if (existing_user):
            access_token = jwt.encode({
                "exp": int(time.time()+3600),
                "email": existing_user.email,
                "username": existing_user.username
            }, get_env_vars("JWT_PRIVATE_KEY"), algorithm='RS256')

            response = Response(json.dumps(
                {"access_token": access_token, "type": "Bearer"}), status=200, mimetype='application/json')
        else:
            response = Response('Invalid credentials or non-existent user',
                                status=401, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


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
        response = None
        client_data = Clients.query.get(id)
        if client_data is None:
            response = Response('Client with id {} does not exist'.format(
                id), status=404, mimetype='application/json')
        else:
            response = Response(json.dumps(client_mapper(
                client_data)), status=200, mimetype='application/json')
        return response
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/client/<id>", methods=["PUT"])
def update_client(id):
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

        client_data = Clients.query.get(id)
        if client_data is None:
            response = Response('Client with id {} does not exist'.format(
                id), status=200, mimetype='application/json')
        else:
            Clients.query.filter_by(id=id).update(dict(
                name=name, email=email, document=document, phone=phone, address=address, city=city, birthday=birthday, sex=sex))
            db_session.commit()
            response = Response('Client with id {} updated successfully'.format(
                id), status=200, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/client/<id>", methods=["DELETE"])
def delete_client(id):
    try:
        response = None
        client_data = Clients.query.get(id)
        if client_data is None:
            response = Response('Client with id {} does not exist'.format(
                id), status=200, mimetype='application/json')
        else:
            db_session.delete(client_data)
            db_session.commit()
            response = Response('Client with id {} deleted successfully'.format(
                id), status=200, mimetype='application/json')

        return response

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


@app.route("/visits", methods=["POST"])
def create_visits():
    try:
        response = None
        client_id = request.form.get("client_id")
        date = datetime.strptime(request.form.get(
            "datetime"), '%d/%m/%Y %H:%M:%S')
        client = Clients.query.filter_by(id=client_id).first()

        if client is None:
            response = Response("Client with id {} does not exist".format(
                client_id), status=404, mimetype='application/json')
        elif Visits.query.filter_by(date=date).all():
            response = Response("Visit on {} already exists".format(
                date), status=404, mimetype='application/json')
        else:
            visit = Visits(client_id=client_id, date=date)
            db_session.add(visit)
            db_session.commit()
            response = Response("{}'s visit at {} created successfully".format(
                client.name, date), status=201, mimetype='application/json')
        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/visit/<id>", methods=["PUT"])
def update_visit(id):
    try:
        response = None
        client_id = request.form.get("client_id")
        date = datetime.strptime(request.form.get(
            "datetime"), '%d/%m/%Y %H:%M:%S')
        client = Clients.query.filter_by(id=client_id).first()

        if client is None:
            response = Response("Client with id {} does not exist".format(
                client_id), status=404, mimetype='application/json')
        visit = Visits.query.get(id)
        if visit is None:
            response = Response("Visit with id {} does not exist".format(
                id), status=404, mimetype='application/json')
        else:
            Visits.query.filter_by(id=id).update(dict(
                date=date, client_id=client_id))
            db_session.commit()
            response = Response("Visit with id {} updated successfully".format(
                id), status=200, mimetype='application/json')
        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/visit/<id>", methods=["DELETE"])
def delete_visit(id):
    try:
        response = None
        visit = Visits.query.get(id)
        if visit is None:
            response = Response('Visit with id {} does not exist'.format(
                id), status=200, mimetype='application/json')
        else:
            db_session.delete(visit)
            db_session.commit()
            response = Response('Visit with id {} deleted successfully'.format(
                id), status=200, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/visit/<id>", methods=["GET"])
def get_visit(id):
    try:
        response = None
        visit_data = Visits.query.get(id)
        if visit_data is None:
            response = Response('Visit with id {} does not exist'.format(
                id), status=404, mimetype='application/json')
        else:
            client_data = Clients.query.get(visit_data.client_id)
            response = Response(json.dumps(visit_mapper(
                visit_data, client_data)), status=200, mimetype='application/json')
        return response
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/visits", methods=["GET"])
def get_visits():
    try:
        date_from = datetime.strptime(request.args.get("from"), '%d/%m/%Y')
        date_to = datetime.strptime(request.args.get("to"), '%d/%m/%Y')
        visits = Visits.query.filter(
            Visits.date.between(date_from, date_to)).all()
        response = []
        for visit in visits:
            client_data = Clients.query.get(visit.client_id)
            response.append(visit_mapper(visit, client_data))
        return Response(json.dumps(response), status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/products", methods=["POST"])
def create_products():
    try:
        name = request.form.get("name")
        description = request.form.get("description")
        type = request.form.get("type")
        category = request.form.get("category")
        laboratory = request.form.get("laboratory")
        size = request.form.get("size")
        unit = request.form.get("unit")
        price = request.form.get("price")
        stock = bool(int(request.form.get("stock")))
        image_url = request.form.get("image_url")

        product = Products(name=name, description=description, type=type, category=category,
                           laboratory=laboratory, size=size, unit=unit, price=price, stock=stock, image_url=image_url)
        db_session.add(product)
        db_session.commit()

        return Response("Product {} created successfully".format(name), status=201, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    try:
        response = None
        name = request.form.get("name")
        description = request.form.get("description")
        type = request.form.get("type")
        category = request.form.get("category")
        laboratory = request.form.get("laboratory")
        size = request.form.get("size")
        unit = request.form.get("unit")
        price = request.form.get("price")
        stock = bool(int(request.form.get("stock")))
        image_url = request.form.get("image_url")

        product = Products.query.get(id)
        if product is None:
            response = Response('Product with id {} does not exist'.format(
                id), status=200, mimetype='application/json')
        else:
            Products.query.filter_by(id=id).update(dict(name=name, description=description, type=type, category=category,
                                                        laboratory=laboratory, size=size, unit=unit, price=price, stock=stock, image_url=image_url))
            db_session.commit()
            response = Response('Product with id {} updated successfully'.format(
                id), status=200, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    try:
        response = None
        product = Products.query.get(id)
        if product is None:
            response = Response('Product with id {} does not exist'.format(
                id), status=200, mimetype='application/json')
        else:
            db_session.delete(product)
            db_session.commit()
            response = Response('Product with id {} deleted successfully'.format(
                id), status=200, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    try:
        response = None
        product_data = Products.query.get(id)
        if product_data is None:
            response = Response('Product with id {} does not exist'.format(
                id), status=404, mimetype='application/json')
        else:
            response = Response(json.dumps(product_mapper(
                product_data)), status=200, mimetype='application/json')
        return response
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/products", methods=["GET"])
def get_products():
    try:
        response = []
        in_stock = int(request.args.get("stock")
                       ) if request.args.get("stock") else None
        if in_stock is not None:
            products_data = Products.query.filter_by(stock=in_stock).all()
        else:
            products_data = Products.query.all()

        for product in products_data:
            response.append(product_mapper(product))

        return Response(json.dumps(response), status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.teardown_appcontext
def shutdown_session(Error=None):
    db_session.remove()


if __name__ == '__main__':
    logging.basicConfig()
    app.run(debug=True)
