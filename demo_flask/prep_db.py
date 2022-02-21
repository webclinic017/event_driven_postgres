import psycopg2

conn = psycopg2.connect(
    host="postgresdb",
    database="postgres",
    user="postgres",
    password="p@ssw0rd1"
)

conn.set_session(autocommit=True)

cursor = conn.cursor()

# Check if database already exists for container initialization vs restart
cursor.execute("SELECT datname FROM pg_database;")
available_dbs = cursor.fetchall()
for entry in available_dbs:
    if 'inventory' in entry:
        db_exists = True
        break
    else:
        db_exists = False

if db_exists:
    cursor.close()
    conn.close()

else:

    cursor.execute("CREATE DATABASE inventory;")

    cursor.close()

    conn.close()

    conn = psycopg2.connect(
        host="postgresdb",
        database="inventory",
        user="postgres",
        password="p@ssw0rd1"
    )

    conn.set_session(autocommit=True)

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255));")

    # Create notify function
    notification_function = """
                            CREATE OR REPLACE FUNCTION ping_me()
                            RETURNS TRIGGER
                            LANGUAGE PLPGSQL
                            AS
                            $$
                            BEGIN
                            NOTIFY test, 'new record';
                            RETURN NEW;
                            END;
                            $$;
                            """
    cursor.execute(notification_function)

    # Create trigger for notify function
    cursor.execute("CREATE TRIGGER new_widget AFTER INSERT ON widgets FOR EACH ROW EXECUTE PROCEDURE ping_me();")

    cursor.close()

    conn.close()
