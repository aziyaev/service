class PilafDBCommands:
    CREATE_PILAF_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS pilaf (
        pilaf_id UUID PRIMARY KEY,
        pilaf_name VARCHAR(255) NOT NULL,
        pilaf_region VARCHAR(255) NOT NULL,
        pilaf_cost INTEGER NOT NULL
    );
    """
    GET_PILAF_COMMAND = """
    SELECT * FROM pilaf WHERE pilaf_id = %s;
    """
    INSERT_PILAF_COMMAND = """
    INSERT INTO pilaf (pilaf_id, pilaf_name, pilaf_region, pilaf_cost)
    VALUES (%s, %s, %s, %s);
    """
    UPDATE_PILAF_COMMAND = """
    UPDATE pilaf SET pilaf_name = %s, pilaf_region = %s, pilaf_cost = %s
    WHERE pilaf_id = %s;
    """
    DELETE_PILAF_COMMAND = """
    DELETE FROM pilaf WHERE pilaf_id = %s;
    """

    CREATE_PILAF_SESSION_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS sessions_history (
        session_id SERIAL PRIMARY KEY,
        session_key UUID NOT NULL,
        session_data TEXT NOT NULL
    );
    """
    INSERT_PILAF_SESSION_COMMAND = """
    INSERT INTO sessions_history (session_key, session_data)
    VALUES (%s, %s);
    """