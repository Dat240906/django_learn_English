import psycopg2

try:
    conn = psycopg2.connect(
        dbname='jtytuonb',
        user='jtytuonb',
        password='13ouPM-o16WFlpCpgJ9RsFtj-ywPJW83',
        host='rain.db.elephantsql.com',
        port='5432',
    )
    print("Connected successfully!")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"Unable to connect. Error: {e}")
