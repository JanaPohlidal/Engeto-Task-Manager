from src.Task_manager_Pohlidalova import (
    odstranit_ukol_db,
    pridat_ukol_save_task_to_database
)

def test_odstranit_ukol_uspesne_odstraneni(prepare_testing_db_and_table_ukoly):

    conn = prepare_testing_db_and_table_ukoly
    task_data = {"nazev": "Integration test task", "popis": "Description of the task for the integration test."}
    pridat_ukol_save_task_to_database(conn, task_data)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly")
    result = cursor.fetchone()
    count_before = result['count']
    cursor.close()
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nazev FROM ukoly WHERE nazev = %s", (task_data["nazev"],))
    result = cursor.fetchone()
    task_id = result['id']
    task_name = result['nazev']
    cursor.close()

    assert task_name == task_data["nazev"], f"Úkol s názvem '{task_data['nazev']}' nebyl nalezen v databázi"
    
    success = odstranit_ukol_db(conn, task_id)

    assert success == True, f"Odstranění úkolu s ID {task_id} by mělo být úspěšné"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    task_exists = result['count']
    cursor.close()
    
    assert task_exists == 0, f"Úkol s ID {task_id} stále existuje v databázi po odstranění"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly")
    result = cursor.fetchone()
    count_after = result['count']
    cursor.close()
    
    assert count_after == count_before - 1, f"Očekával jsem {count_before - 1} úkolů, ale mám {count_after}"


def test_odstranit_ukol_neexistujici_id(prepare_testing_db_and_table_ukoly):

    conn = prepare_testing_db_and_table_ukoly
    task_data = {"nazev": "Integration test task", "popis": "Description of the task for the integration test."}
    pridat_ukol_save_task_to_database(conn, task_data)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT MAX(id) as max_id FROM ukoly")
    result = cursor.fetchone()
    max_id_result = result['max_id']
    cursor.close()

    nonexistent_id = (max_id_result + 1000) if max_id_result is not None else 1000

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly")
    result = cursor.fetchone()
    count_before = result['count']
    cursor.close()

    success = odstranit_ukol_db(conn, nonexistent_id)

    assert success == False, f"Odstranění neexistujícího ID {nonexistent_id} by mělo vrátit False"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly")
    result = cursor.fetchone()
    count_after = result['count']
    cursor.close()
    
    assert count_before == count_after, f"Počet úkolů se neměl změnit. Před: {count_before}, Po: {count_after}"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nazev FROM ukoly WHERE nazev = %s", (task_data["nazev"],))
    result = cursor.fetchone()
    cursor.close()
    
    assert result is not None, "Existující úkol byl neočekávaně odstraněn"
        

