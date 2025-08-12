from src.Task_manager_Pohlidalova import pridat_ukol_save_task_to_database 
    

def test_pridat_ukol_save_task_to_db(prepare_testing_db_and_table_ukoly):

    conn = prepare_testing_db_and_table_ukoly
    task_data = {"nazev": "Integration test task", "popis": "Description of the task for the integration test."}
    pridat_ukol_save_task_to_database(conn, task_data)

    cursor = conn.cursor()
    cursor.execute("SELECT nazev, popis, stav FROM ukoly WHERE nazev = %s", (task_data["nazev"],))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == "Integration test task"
    assert result[1] == "Description of the task for the integration test."
    assert result[2] == "Nezahájeno"
     
def test_pridat_ukol_with_long_nazev(prepare_testing_db_and_table_ukoly):

    conn = prepare_testing_db_and_table_ukoly
    long_name = "A" * 260
    task_data = {"nazev": long_name, "popis": "Description of the task for the integration test. Testing with very long 'nazev'."}
    pridat_ukol_save_task_to_database(conn, task_data)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ukoly WHERE nazev = %s", (long_name,))
    count = cursor.fetchone()[0]
    cursor.close()
    assert count == 0

  
