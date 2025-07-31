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
             password=db_password,
             database=db_name
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
          


ukoly = []

def hlavni_menu():
        while True:
            connect_to_db()
            print("\nSprávce úkolů - Hlavní menu")
            print("1. Přidat nový úkol")
            print("2. Zobrazit všechny úkoly")
            print("3. Odstranit úkol")
            print("4. Konec programu")

            volba_menu = input("\nVyberte možnost (1-4): ")

            if volba_menu == "1":
                pridat_ukol()
            elif volba_menu == "2":
                zobrazit_ukoly()
            elif volba_menu == "3":
                odstranit_ukol()
            elif volba_menu == "4":
                print("Konec programu.")
                break
            else:
                print("Neplatná volba! Zadejte číslo 1-4.")

def pridat_ukol():
    nazev_ukolu = input("Zadejte název úkolu: ")
    while nazev_ukolu == "":
          print("Název úkolu nemůže být prázdný! Zkuste to znovu.")
          nazev_ukolu = input("Zadejte název úkolu: ")
    
    popis_ukolu = input("Zadejte popis úkolu: ")
    while popis_ukolu == "":
          print("Popis úkolu nemůže být prázdný! Zkuste to znovu.")
          popis_ukolu = input("Zadejte popis úkolu: ")
    
    ukoly.append({"nazev": nazev_ukolu, "popis": popis_ukolu})
    print(f"Úkol {nazev_ukolu} byl přidán.")
    

def zobrazit_ukoly():
     print("\nSeznam úkolů:")
     if len(ukoly) == 0:
          print("Žádné úkoly k zobrazení")
          return
    
     i = 0
     for ukol in ukoly:
          print(f"{i+1}. {ukol["nazev"]} - {ukol["popis"]}")
          i = i + 1
     

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

     
                
                