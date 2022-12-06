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
