from src.Task_manager_Pohlidalova import (
    aktualizovat_ukol_db, 
    vypis_seznam_ukolu,
    pridat_ukol_save_task_to_database
)

def test_aktualizovat_ukol_uspesna_aktualizace(prepare_testing_db_and_table_ukoly):
    conn = prepare_testing_db_and_table_ukoly
    task_data = {"nazev": "Integration test task", "popis": "Description of the task for the integration test."}
    pridat_ukol_save_task_to_database(conn, task_data)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE nazev = %s", (task_data["nazev"],))
    result = cursor.fetchone()
    task_id = result['id']
    original_status = result['stav']
    cursor.close()

    assert original_status == "Nezahájeno", f"Očekával jsem výchozí stav 'Nezahájeno', ale dostal jsem '{original_status}'"
    
    success = aktualizovat_ukol_db(conn, task_id, "Probíhá")
    assert success == True, "Aktualizace na stav 'Probíhá' by měla být úspěšná"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    updated_status = result['stav']
    cursor.close() 

    assert updated_status == "Probíhá", f"Očekával jsem stav 'Probíhá', ale dostal jsem '{updated_status}'"
    
    success = aktualizovat_ukol_db(conn, task_id, "Hotovo")
    assert success == True, "Aktualizace na stav 'Hotovo' by měla být úspěšná"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    final_status = result['stav']
    cursor.close()        
    assert final_status == "Hotovo", f"Očekával jsem stav 'Hotovo', ale dostal jsem '{final_status}'"


def test_aktualizovat_ukol_neexistujici_id (prepare_testing_db_and_table_ukoly):

    conn = prepare_testing_db_and_table_ukoly

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

    success = aktualizovat_ukol_db(conn, nonexistent_id, "Probíhá")
    assert success == False, f"Aktualizace neexistujícího ID {nonexistent_id} by měla vrátit False"

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ukoly")
    result = cursor.fetchone()
    count_after = result['count']
    cursor.close()
        
    assert count_before == count_after, "Počet úkolů v databázi se neměl změnit"