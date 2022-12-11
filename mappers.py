def client_mapper(client_data):
    return {
        "id": client_data.id,
        "name": client_data.name,
        "email": client_data.email,
        "document": client_data.document,
        "phone": client_data.phone,
        "address": client_data.address,
        "city": client_data.city,
        "birthday": str(client_data.birthday),
        "sex": client_data.sex,
    }


def visit_mapper(visit_data, client_data):
    return {
        "id": visit_data.id,
        "date": str(visit_data.date),
        "client": client_mapper(client_data)
    }

    
def product_mapper(product_data):
    return {
        "id": product_data.id,
        "name": product_data.name,
        "description": product_data.description,
        "type": product_data.type,
        "category": product_data.category,
        "laboratory": product_data.laboratory,
        "size": product_data.size,
        "unit": product_data.unit,
        "price": product_data.price,
        "stock": product_data.stock,
        "image_url": product_data.image_url
    }
