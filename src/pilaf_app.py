import os

from flask import Flask, request

from pilaf_session_model import PilafSessionModel
from pilaf_model import PilafModel
from responses import Responses

app = Flask(__name__)
model = PilafModel(
    db_host=os.getenv("POSTGRES_HOST", "localhost"),
    db_port=int(os.getenv("POSTGRES_PORT", 5432)),
    db_user=os.getenv("POSTGRES_USER", "postgres"),
    db_password=os.getenv("POSTGRES_PASSWORD", ""),
    db_name=os.getenv("POSTGRES_DB", "postgres"),
)
sessions_model = PilafSessionModel(
    db_host=os.getenv("POSTGRES_HOST", "localhost"),
    db_port=int(os.getenv("POSTGRES_PORT", 5432)),
    db_user=os.getenv("POSTGRES_USER", "postgres"),
    db_password=os.getenv("POSTGRES_PASSWORD", ""),
    db_name=os.getenv("POSTGRES_DB", "postgres"),
    cache_db_host=os.getenv("REDIS_HOST", "localhost"),
    cache_db_port=int(os.getenv("REDIS_PORT", 6379))
)


@app.post("/auth")
def authorize():
    if request.is_json:
        auth_data = request.get_json()
        if PilafSessionModel.is_auth_data_valid(auth_data):
            auth_key = sessions_model.authorize(auth_data)
            return Responses.ok(auth_key=auth_key)
        return Responses.invalid_json_format()
    return Responses.invalid_request_body_data_type()


@app.post("/add_pilaf")
def add_pilaf():
    auth_key = request.headers.get("XAuthKey")
    if auth_key and sessions_model.is_authorized(auth_key):
        if request.is_json:
            pilaf_data = request.get_json()
            if PilafModel.isPilafDataValid(pilaf_data):
                pilaf_id = model.setPilaf(pilaf_data)
                return Responses.ok(pilaf_id=pilaf_id)
            return Responses.invalid_json_format()
        return Responses.invalid_request_body_data_type()
    return Responses.not_authorized()


@app.get("/get_pilaf/<pilaf_id>")
def get_pilaf(pilaf_id):
    auth_key = request.headers.get("XAuthKey")
    if auth_key and sessions_model.is_authorized(auth_key):
        pilaf_data = model.get_user_data(pilaf_id)
        if pilaf_data:
            return Responses.ok(pilaf_data=pilaf_data)
        return Responses.user_not_found()
    return Responses.not_authorized()


# @app.put("/update_user/<user_id>")
# def update_user(user_id):
#     auth_key = request.headers.get("XAuthKey")
#     if auth_key and sessions_model.is_authorized(auth_key):
#         if request.is_json:
#             new_user_data = request.get_json()
#             if UsersModel.is_user_data_valid(new_user_data):
#                 user_changed = model.set_user_data(new_user_data, user_id)
#                 if user_changed:
#                     return UsersResponses.ok(message="Successfully changed")
#                 return UsersResponses.user_not_found()
#             return UsersResponses.invalid_json_format()
#         return UsersResponses.invalid_request_body_data_type()
#     return UsersResponses.not_authorized()


@app.delete("/delete_pilaf/<pilaf_id>")
def delete_pilaf(pilaf_id):
    auth_key = request.headers.get("XAuthKey")
    if auth_key and sessions_model.is_authorized(auth_key):
        deleted = model.deletePilaf(pilaf_id)
        if deleted:
            return Responses.ok(message="Successfully deleted")
        return Responses.pilaf_not_found()
    return Responses.not_authorized()

