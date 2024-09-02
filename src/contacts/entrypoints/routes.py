import json
from flask import Response, request

from src.contacts.service_layer.services import ContactService, validate_request_with_schema, transform_request_for_db
from src.contacts.service_layer import unit_of_work


def init_views(app):
    @app.route('/contacts', methods=['POST'])
    def add_contact():
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        error = None
        error = validate_request_with_schema(request.json)

        if not error:
            transform_request_for_db(request.json)
            new_contact = service.add(
                request.json["first_name"],
                request.json["last_name"],
                request.json["birthday"],
                request.json["email_address"]
            )
            print(f'Ready to be sent in response: {new_contact}')
    
            return Response(response=json.dumps(new_contact), status=201)
        else:
            return Response(response="Payload validation failed", status=422)

    

    @app.route('/contacts/<int:id>', methods=['GET'])
    def get_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        existing_contact = service.get_by_id(id)

        return Response(response=json.dumps(existing_contact), status=200)


    @app.route('/contacts', methods=['GET'])
    def get_all_contacts():
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        all_contacts = service.get_all_contacts()

        return Response(response=json.dumps(all_contacts), status=200)
    

    @app.route('/contacts/<int:id>', methods=['PUT'])
    def update_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        updated_contact = service.update(id, request.json)

        return Response(response=json.dumps(updated_contact), status=201)
    

    @app.route('/contacts/<int:id>', methods=['DELETE'])
    def delete_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        service.delete_by_id(id)

        return Response(status=204)