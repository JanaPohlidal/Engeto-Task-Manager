"""
Projekt: Task Manager
Task manager pro pridavani, zobrazeni a odstraneni ukolu
Pripravila: Jana Pohlidalova
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
def connect_to_db():
    #Creates and returns a connection to the MySQL server and creates database if it does not exist.
        
    try:
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        if not all([db_user, db_password, db_name]):
             print ("Error: Database username, password and db name are not set in environment variables.")
             return None
        
        conn = mysql.connector.connect(
             host = db_host,
             user = db_user,
             password = db_password,
             database = db_name
        )
        if conn.is_connected():
             print(f"Successfully connected to database {db_name}.")
             return conn
        
    except mysql.connector.Error as e:
        print(f"Error while connecting to the MySQL server: {e}")
        if e.errno == 1049:
                print(f"Databse {db_name} does not exist. Attempting to create it...")
                server_conn = None
                conn = None
                try:
                    server_conn = mysql.connector.connect(
                        host = db_host,
                        user = db_user,
                        password = db_password
                    )
                    if server_conn.is_connected():
                        cursor = server_conn.cursor()
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                        print(f"Database {db_name} successfully created")
                        cursor.close()
                        
                        conn = mysql.connector.connect(
                            host = db_host,
                            user = db_user,
                            password=db_password,
                            database=db_name
                        )
                        if conn.is_connected():
                            print("Successfully connected to the MySQL server.")
                            return conn
                        else:
                             print ("Failed to connect after creating database.")
                             if conn:
                                  conn.close()
                             return None
                    else:
                         print(f"Error: Unable to connect to the MySQL server to create the database")
                         return None
                except mysql.connector.Error as server_e:
                     print(f"Error while creating MySQL database {db_name}: {server_e}")
                     if conn and conn.is_connected():
                          conn.close()
                     return None
                finally:
                     if server_conn and server_conn.is_connected():
                          server_conn.close()
                 
        else:
            print(f"Error while connecting to MySQL database {db_name}: {e}")
            return None

def create_ukoly_table_if_not_exists(conn):
    if not conn or not conn.is_connected():
        print("Error: No database connection available.")
        return None    
    
    try:
        cursor = conn.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(50) DEFAULT 'Nezahájeno'           
                )
            """
    
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'ukoly' is ready for use.")
        cursor.close()
        return True
    
    except mysql.connector.Error as e:
         print(f"Error while creating table 'ukoly': {e}")
         return False


def hlavni_menu():
        
        conn = connect_to_db()
        
        while True:
            print("\nSprávce úkolů - Hlavní menu")
            print("1. Přidat úkol")
            print("2. Zobrazit všechny úkoly")
            print("3. Aktualizovat úkol")
            print("4. Odstranit úkol")
            print("5. Konec programu")

            volba_menu = input("\nVyberte možnost (1-4): ")

            if volba_menu == "1":
                task_data = pridat_ukol_get_data_from_user()
                if task_data:
                     create_ukoly_table_if_not_exists(conn)
                     pridat_ukol_save_task_to_database(conn, task_data)
            elif volba_menu == "2":
                zobrazit_ukoly(conn)
            elif volba_menu == "3":
                aktualizovat_ukol(conn)
            elif volba_menu == "4":
                odstranit_ukol()
            elif volba_menu == "5":
                print("Konec programu.")
                break
            else:
                print("Neplatná volba! Zadejte číslo 1-4.")

def pridat_ukol_get_data_from_user():
    """
    Prompts the user for a task name and description.
    Returns a dictionary with the task data, or None if the input is canceled.
    This function only handles user input, not database operations.
    """

    nazev_ukolu = input("Zadejte název úkolu: ")
    while nazev_ukolu == "":
          print("Název úkolu nemůže být prázdný! Zkuste to znovu.")
          nazev_ukolu = input("Zadejte název úkolu: ")
    
    popis_ukolu = input("Zadejte popis úkolu: ")
    while popis_ukolu == "":
          print("Popis úkolu nemůže být prázdný! Zkuste to znovu.")
          popis_ukolu = input("Zadejte popis úkolu: ")

    return {
         "nazev": nazev_ukolu,
         "popis": popis_ukolu         
        }
    

def pridat_ukol_save_task_to_database(conn, task_data):
    if not conn or not conn.is_connected():
         print ("Error: No database connection available to save the task.")
         return
    
    try:
         cursor = conn.cursor()
         SQLquery = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
         values = (task_data["nazev"], task_data["popis"])
         cursor.execute(SQLquery, values)
         conn.commit()
         print(f"Úkol {task_data['nazev']} byl úspěšně přidán do databáze.")
    except mysql.connector.Error as e:
         print(f"Chyba při ukládání úkolu do databáze: {e}")
    finally:
         cursor.close()
       

def zobrazit_ukoly(conn):
    if not conn or not conn.is_connected():
         print ("Error: No database connection available to show the tasks.")
         return
    
    while True:
         print("\n--- Zobrazení úkolů ---")
         print("1. Zobrazit aktivní úkoly (Nezahájeno, Probíhá)")
         print("2. Zobrazit dokončené úkoly")
         print("3. Zobrazit všechny úkoly")
         print("4. Zpět do hlavního menu")
        
         volba_filtru = input("Vyberte možnost (1-4): ")
         
         SQLquery = ""
         params = None
         nadpis = ""

         if volba_filtru == "1":
            SQLquery = "SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN (%s, %s)"
            params = ('Nezahájeno', 'Probíhá')
            nadpis = "--- Seznam aktivních úkolů (Nezahájeno, Probíhá) ---"
         elif volba_filtru == "2":
            SQLquery = "SELECT id, nazev, popis, stav FROM ukoly WHERE stav = %s"
            params = ('Hotovo',)
            nadpis = "--- Seznam dokončených úkolů ---"
         elif volba_filtru == "3":
            SQLquery = "SELECT id, nazev, popis, stav FROM ukoly"
            nadpis = "--- Seznam všech úkolů ---"
         elif volba_filtru == "4":
            return
         else:
            print("Neplatná volba, zkuste to znovu.")
            continue  
            
         try:
            cursor = conn.cursor()
            if params:
                cursor.execute(SQLquery, params)
            else:
                cursor.execute(SQLquery, params)

            ukoly = cursor.fetchall()

            print(f"\n{nadpis}")

            if not ukoly:
                print("Žádné úkoly k zobrazení")
            else:
                print(f"{'ID':<5}{'Název':<30}{'Stav':<15}{'Popis'}")
                print("-" * 80)
                for ukol in ukoly:
                    id, nazev, popis, stav = ukol
                    print(f"{id:<5}{nazev:<30}{stav:<15}{popis}")
                    print("-" * 80)
            
         except mysql.connector.Error as e:
            print(f"Chyba při ukládání úkolu do databáze: {e}")
         finally:
            cursor.close()

def aktualizovat_ukol(conn):
    if not conn or not conn.is_connected():
        print ("Error: No database connection available to show the tasks.")
        return 
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nazev, stav FROM ukoly")
        ukoly = cursor.fetchall()

        if not ukoly:
            print("\nV databázi nejsou žádné úkoly, které by bylo možné aktualizovat.")
            return
        
        print("\n--- Seznam všech úkolů ---")
        print(f"{'ID':<5}{'Název':<30}{'Stav'}")
        print("-" * 50)
        for ukol in ukoly:
            print(f"{ukol['id']:<5}{ukol['nazev']:<30}{ukol['stav']}")
        print("-" * 50)

        valid_ids = {ukol['id'] for ukol in ukoly}

    except mysql.connector.Error as e:
        print (f"Chyba při načítání úkolů: {e}")
        return
    finally:
        cursor.close()

    selected_id = None
    while True:
        input_id = input("Zadejte ID úkolu, který chcete aktualizovat (nebo 'q' pro zpět): ")
        if input_id.lower() == 'q':
            return
        
        try:
            selected_id = int(input_id)
            if selected_id in valid_ids:
                break
            else:
                print("Chyba: Zadané ID neexistuje. Zkuste to znovu.")
        except ValueError:
            print("Chyba: Musíte zadat platné číslo ID.")
    
    new_status = None
    while True:
        print("\nVyberte nový stav úkolu:")
        print("1. Probíhá")
        print("2. Hotovo")

        selected_status_change = input("Zadejte volbu 1 nebo 2: ")

        if selected_status_change == "1":
            new_status = 'Probíhá'
            break
        elif selected_status_change == "2":
            new_status = "Hotovo"
            break
        else:
            print ("Neplatna volba. Zadejte 1 nebo 2.")

    try:
        cursor = conn.cursor()
        SQL_query = "UPDATE ukoly SET stav = %s WHERE id = %s"
        cursor.execute(SQL_query, (new_status, input_id))
        conn.commit()
        print(f"\nÚkol s ID {selected_id} byl úspěšně aktualizován na stav '{new_status}'.")
    except mysql.connector.Error as e:
        print(f"Chyba při aktualizaci úkolu v databázi: {e}")
    finally:
        cursor.close()

    
def odstranit_ukol():
    if len(ukoly) == 0:
          print("\nSeznam úkolů je prázdný. Není co odstranit.")
          return
    i = 0
    print("\nSeznam úkolů:")
    for ukol in ukoly:
        print(f"{i+1}. {ukol["nazev"]} - {ukol["popis"]}")
        i = i + 1

    try:   
        vstup = input("\nZadejte číslo úkolu, který chcete odstranit: ")
        cislo = int(vstup)

        if 1 <= cislo <= len(ukoly):
            odstraneny_ukol = ukoly.pop(cislo - 1)
            print(f"Úkol '{odstraneny_ukol['nazev']}' byl odstraněn.")

        else:
            if len(ukoly) == 1:
                print(f"Neplatné číslo! V seznamu máte pouze {len(ukoly)} úkol.")
            else:
                print(f"Neplatné číslo! Zadejte číslo mezi 1 a {len(ukoly)}.")

    except ValueError:
         print(f"Chyba: {vstup} není platné číslo.")
            
if __name__ == "__main__":
     hlavni_menu()

     
                
                