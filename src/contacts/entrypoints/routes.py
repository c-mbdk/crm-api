import json
import traceback
from flask import Response, jsonify, request
from marshmallow import ValidationError

from src.contacts.service_layer.services import ContactService, validate_request_with_schema, transform_request_for_db
from src.contacts.service_layer import unit_of_work
from src.contacts.utils.exceptions import ErrorResponse, InvalidRecord, RecordExists, BadRequestException


def init_views(app):
    @app.route('/contacts', methods=['POST'])
    def add_contact():
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        try:
            validate_request_with_schema(request.json)

            transform_request_for_db(request.json)

            new_contact = service.add(
                    request.json["first_name"],
                    request.json["last_name"],
                    request.json["birthday"],
                    request.json["email_address"]
                )
            
            return Response(response=json.dumps(new_contact), status=201)


        except ValidationError as e:
            raise ValidationError(e.messages)
        
        except RecordExists:
            raise RecordExists(request.json["email_address"])

        # error = None
        # error = validate_request_with_schema(request.json)

        # if not error:
        #     try:
        #         transform_request_for_db(request.json)
        #         new_contact = service.add(
        #             request.json["first_name"],
        #             request.json["last_name"],
        #             request.json["birthday"],
        #             request.json["email_address"]
        #         )
        #         print(f'Ready to be sent in response: {new_contact}')
        
        #         return Response(response=json.dumps(new_contact), status=201)
        #     except RecordExists as e:
        #         return {"message": str(e)}, 400
        
        # else:
        #     raise ValidationError(error)

    

    @app.route('/contacts/<int:id>', methods=['GET'])
    def get_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        try:
            existing_contact = service.get_by_id(id)
            return Response(response=json.dumps(existing_contact), status=200)
    
        except InvalidRecord:
            raise InvalidRecord(id)

    @app.route('/contacts', methods=['GET'])
    def get_all_contacts():
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        all_contacts = service.get_all_contacts()

        return Response(response=json.dumps(all_contacts), status=200)
    

    @app.route('/contacts/<int:id>', methods=['PUT'])
    def update_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        try:
            updated_contact = service.update(id, request.json)

            return Response(response=json.dumps(updated_contact), status=201)
    
        except InvalidRecord:
            raise InvalidRecord(id)
    

    @app.route('/contacts/<int:id>', methods=['DELETE'])
    def delete_contact(id):
        service = ContactService(unit_of_work.SqlAlchemyUnitOfWork(session_factory=unit_of_work.DEFAULT_SESSION_FACTORY))

        try:
            service.delete_by_id(id)

            return Response(status=204)
        
        except InvalidRecord:
            raise InvalidRecord(id)
    
def register_error_functions(app):
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    @app.route("/<string:path>")
    def unavailable(path):
        raise BadRequestException("Invalid path")
    

    @app.errorhandler(RecordExists)
    def handle_record_exists(exc):

        app.logger.error(f"RecordExists - {exc}")
        
        return ErrorResponse(status_code=exc.status_code, data=exc.message)
    
    @app.errorhandler(ValidationError)
    def handle_validation_failure(error):

        app.logger.error(f"Validation Error - {error}")

        return ErrorResponse(status_code=422, data={'errors': error.messages})
    
    @app.errorhandler(InvalidRecord)
    def handle_invalid_record(exc):

        app.logger.error(f"InvalidRecord - {exc}")

        return ErrorResponse(status_code=exc.status_code, data=exc.message)
    
    @app.errorhandler(BadRequestException)
    def handle_bad_request(exc):

        app.logger.error(f"BadRequestException - {exc}")

        return ErrorResponse(status_code=exc.status_code, data=exc.message)