from flask import jsonify


class Responses:

    @staticmethod
    def ok(**response_body_values):
        ok_message_template = {
            "status": "ok"
        }
        ok_message_template.update(response_body_values)
        return jsonify(ok_message_template), 200

    @staticmethod
    def _error(message: str, status_code: int):
        return jsonify({
            "status": "error",
            "message": message
        }), status_code

    @staticmethod
    def invalid_json_format():
        return Responses._error("Invalid JSON format", 400)

    @staticmethod
    def invalid_request_body_data_type():
        return Responses._error("Expected JSON data in request body", 400)

    @staticmethod
    def pilaf_not_found():
        return Responses._error("User with the given id hasn't been found", 404)

    @staticmethod
    def not_authorized():
        return Responses._error(
            "You should authorize or reauthorize first to use this request", 401
        )
