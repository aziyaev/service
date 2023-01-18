from uuid import uuid4
from typing import Dict

import psycopg2

from pilaf_db_commands import PilafDBCommands


class PilafModel:

    def __init__(self, db_host: str, db_port: int, db_user: str, db_password: str, db_name: str):
        self.db_connection = psycopg2.connect(
            host=db_host, port=db_port, user=db_user, password=db_password, dbname=db_name
        )
        with self.db_connection.cursor() as cursor:
            cursor.execute(PilafDBCommands.CREATE_PILAF_TABLE_COMMAND)
        self.db_connection.commit()

    @staticmethod
    def isPilafDataValid(pilaf_data: Dict) -> bool:
        got_all_fields = "name" in pilaf_data and \
                         "region" in pilaf_data and \
                         "cost" in pilaf_data
        if not got_all_fields:
            return False
        if len(pilaf_data) != 3:
            return False
        return \
            type(pilaf_data["name"]) is str and \
            type(pilaf_data["region"]) is str and \
            type(pilaf_data["cost"]) is int

    def checkPilafExistence(self, pilaf_id: str) -> bool:
        with self.db_connection.cursor() as cursor:
            cursor.execute(PilafDBCommands.GET_PILAF_COMMAND, (pilaf_id,))
            if cursor.rowcount == 0:
                return False
            return True

    def setPilaf(self, pilaf_data: Dict, pilaf_id: str):
        if not pilaf_id:
            pilaf_id = str(uuid4())
            command = PilafDBCommands.INSERT_PILAF_COMMAND
            value_tuple = (pilaf_id, pilaf_data["name"], pilaf_data["region"], pilaf_data["cost"])
        elif not self.checkPilafExistence(pilaf_id):
            return None
        else:
            command = PilafDBCommands.UPDATE_PILAF_COMMAND
            value_tuple = (pilaf_data["name"], pilaf_data["region"], pilaf_data["cost"], pilaf_id)
        with self.db_connection.cursor() as cursor:
            cursor.execute(command, value_tuple)
        self.db_connection.commit()
        return pilaf_id

    def getPilaf(self, pilaf_id: str) -> Dict:
        with self.db_connection.cursor() as cursor:
            cursor.execute(PilafDBCommands.GET_PILAF_COMMAND, (pilaf_id,))
            if cursor.rowcount == 0:
                return None
            pilaf_row = cursor.fetchone()
            return {
                "name": pilaf_row[1],
                "region": pilaf_row[2],
                "cost": pilaf_row[3]
            }

    def deletePilaf(self, pilaf_id: str) -> bool:
        if self.checkPilafExistence(pilaf_id):
            with self.db_connection.cursor() as cursor:
                cursor.execute(PilafDBCommands.DELETE_PILAF_COMMAND, (pilaf_id,))
            self.db_connection.commit()
            return True
        return False
