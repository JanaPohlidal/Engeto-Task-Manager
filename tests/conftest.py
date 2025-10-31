import pytest
import mysql.connector
import os
from dotenv import load_dotenv
from src.Task_manager_Pohlidalova import connect_to_db, create_ukoly_table_if_not_exists

load_dotenv()

@pytest.fixture
def prepare_testing_db_db_exists():
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    original_db_name = os.getenv("DB_NAME")
    test_db_name = "task_manager_test_db_exists"

    os.environ["DB_NAME"] = test_db_name

    test_conn = None
    cleanup_conn = None

    try:
        test_conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
            )
        cursor = test_conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        cursor.execute(f"CREATE DATABASE {test_db_name}")
        cursor.execute(f"USE {test_db_name}")
        cursor.close()
        test_conn.close()

        yield test_db_name

    except mysql.connector.Error as e:
        pytest.fail(f"Failed to prepare test database: {e}")

    finally:
        if test_conn and test_conn.is_connected():
            test_conn.close()
        
        try:
            cleanup_conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password
            )
            cursor = cleanup_conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
            cursor.close()
            cleanup_conn.close()

            if original_db_name is not None:
                os.environ["DB_NAME"] = original_db_name
            else:
                del os.environ["DB_NAME"]

        except mysql.connector.Error as e:
            print(f"Error: Failed to clean up test database {test_db_name}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred during database cleanup: {e}")


        
@pytest.fixture
def prepare_testing_db_db_nonexistent():
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    original_db_name = os.getenv("DB_NAME") 
    test_db_name = f"{original_db_name}_test_db_nonexistent"
    
    os.environ["DB_NAME"] = test_db_name

    test_conn = None
    cleanup_conn = None

    try:
        test_conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
            )
        cursor = test_conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        cursor.close()
        test_conn.close()
        
        yield test_db_name

    except mysql.connector.Error as e:
        pytest.fail(f"Failed to prepare test database: {e}")

    finally:
        if test_conn and test_conn.is_connected():
            test_conn.close()
        
        try:
            cleanup_conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password
            )
            cursor = cleanup_conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
            cursor.close()
            cleanup_conn.close()

            if original_db_name is not None:
                os.environ["DB_NAME"] = original_db_name
            else:
                del os.environ["DB_NAME"]

        except mysql.connector.Error as e:
            print(f"Error: Failed to clean up test database {test_db_name}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred during database cleanup: {e}")

@pytest.fixture
def prepare_testing_db_and_table_ukoly(prepare_testing_db_db_exists):
    conn = connect_to_db()
    create_ukoly_table_if_not_exists(conn)

    yield conn

    if conn and conn.is_connected():
        conn.close()
