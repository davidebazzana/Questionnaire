import psycopg2
import os

create_visit_table = "CREATE TABLE IF NOT EXISTS visit (id SERIAL PRIMARY KEY, ts TIMESTAMP NOT NULL DEFAULT now());"
create_result_table = "CREATE TABLE IF NOT EXISTS result (id SERIAL PRIMARY KEY, ts TIMESTAMP NOT NULL DEFAULT now(), personal TEXT NOT NULL, professional TEXT NOT NULL);"

def main():
    try:
        conn = psycopg2.connect(dbname='mollami-data', 
                                user='mollami@mollami-data-server', 
                                host='mollami-data-server.postgres.database.azure.com', 
                                password=os.environ.get("STATISTICS_DB_PASSWORD"), 
                                port='5432', 
                                sslmode='require')
    except:
        print("Unable to reach mollami-data-server.postgres.database.azure.com")
    print("Connected to mollami-data-server.postgres.database.azure.com...")
    cur = conn.cursor()
    cur.execute(create_result_table)
    cur.execute(create_visit_table)
    conn.commit()
    print("Initialized the database")
    conn.close()
    print("Connection closed")

if __name__ == "__main__":
    main()
