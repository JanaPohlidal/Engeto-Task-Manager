from src.Task_manager_Pohlidalova import connect_to_db, create_ukoly_table_if_not_exists

def test_create_ukoly_table_db_exists(prepare_testing_db_db_exists):

    test_db_name = prepare_testing_db_db_exists
    conn = connect_to_db()
    assert conn is not None and conn.is_connected()

    table_created = create_ukoly_table_if_not_exists(conn)
    assert table_created is True

    cursor = conn.cursor()
    cursor.execute (f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'ukoly'
            """, (test_db_name,))
    table_exists = cursor.fetchone()[0] == 1
    cursor.close()

    if conn and conn.is_connected():
        conn.close()

    assert table_exists, "Table 'ukoly' was not created in the test database"


def test_create_ukoly_table_invalid_connection():
    invalid_connection = None
    table_created = create_ukoly_table_if_not_exists(invalid_connection)
    assert table_created is None or table_created is False, "Function shoud fail with invalid connection"