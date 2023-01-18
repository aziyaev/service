from threading import Timer
from typing import Dict
from uuid import uuid4

import psycopg2
from redis.client import Redis

from pilaf_db_commands import PilafDBCommands


class PilafSessionModel:

    def __init__(
            self, db_host: str, db_port: int, db_user: str, db_password: str, db_name: str,
            cache_db_host: str, cache_db_port: int
    ):
        self.cache_db_client = Redis(host=cache_db_host, port=cache_db_port, decode_responses=True)
        self.db_connection = psycopg2.connect(
            host=db_host, port=db_port, user=db_user, password=db_password, dbname=db_name
        )
        with self.db_connection.cursor() as cursor:
            cursor.execute(PilafDBCommands.CREATE_PILAF_SESSION_TABLE_COMMAND)
        self.db_connection.commit()

    @staticmethod
    def is_auth_data_valid(auth_data: Dict) -> bool:
        got_all_fields = "login" in auth_data and \
                         "password" in auth_data
        if not got_all_fields:
            return False
        if len(auth_data) != 2:
            return False
        return \
            type(auth_data["login"]) is str and \
            type(auth_data["password"]) is str

    def authorize(self, auth_data: Dict) -> str:
        auth_cache_key = str(uuid4())
        auth_cache_data = f"login={auth_data['login']}&password={auth_data['password']}"
        self.cache_db_client.set(auth_cache_key, auth_cache_data, ex=120)
        archive_session_timer = Timer(90.0, self._archive_session, [auth_cache_key, auth_cache_data])
        archive_session_timer.start()
        return auth_cache_key

    def _archive_session(self, auth_key, auth_data):
        with self.db_connection.cursor() as cursor:
            cursor.execute(PilafDBCommands.INSERT_PILAF_SESSION_COMMAND, (auth_key, auth_data))
        self.db_connection.commit()

    def is_authorized(self, auth_key: str) -> bool:
        return self.cache_db_client.exists(auth_key) == 1