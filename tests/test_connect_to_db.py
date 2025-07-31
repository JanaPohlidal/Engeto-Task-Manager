from src.Task_manager_Pohlidalova import connect_to_db

def test_connct_to_db_db_exists(prepare_testing_db_db_exists):
    conn = connect_to_db()
    assert conn is not None
    assert conn.is_connected()

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()[0]
    assert current_db == prepare_testing_db_db_exists
    conn.close()
    

def test_connect_to_db_db_nonexistent(prepare_testing_db_db_nonexistent):
    conn = connect_to_db()
    assert conn is not None
    assert conn.is_connected()

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()[0]
    assert current_db == prepare_testing_db_db_nonexistent
    conn.close()




