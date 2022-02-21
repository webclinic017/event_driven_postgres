import select
import time

import psycopg2
import psycopg2.extensions

running = True
while running:

    connecting = True
    connecting_retry = 0

    while connecting:
        try:
            conn = psycopg2.connect(
                host="postgresdb",
                database="inventory",
                user="postgres",
                password="p@ssw0rd1"
            )
        except:
            connecting_retry += 1
            if connecting_retry == 5:
                print('Total failure')
                connecting = False
                running = False
            else:
                time.sleep(5)
                continue

        else:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = conn.cursor()
            cursor.execute("LISTEN test;")

            print("Waiting for notifications on channel 'test'")

            listening = True

            while listening:
                if select.select([conn], [], [], 5) == ([], [], []):
                    pass
                else:
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
                if conn.closed == 0:
                    continue
                else:
                    try:
                        cursor.close()
                        conn.close()
                    except:
                        listening = False
                    else:
                        listening = False             


