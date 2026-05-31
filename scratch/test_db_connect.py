from sqlalchemy import create_engine, text
import urllib

SQL_SERVER_CONFIG = {
    'server': 'localhost',
    'database': 'TechShopWebsite2',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'yes',
}

params = urllib.parse.quote(
    f"DRIVER={{{SQL_SERVER_CONFIG['driver']}}};"
    f"SERVER={SQL_SERVER_CONFIG['server']};"
    f"DATABASE={SQL_SERVER_CONFIG['database']};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
url = f"mssql+pyodbc:///?odbc_connect={params}"
print('URL pattern:', url[:120])

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT @@VERSION'))
        print('SQLAlchemy current config: OK')
except Exception as e:
    print('SQLAlchemy current config FAILED:', str(e)[:100])

# Thu dung localhost
params2 = urllib.parse.quote(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=TechShopWebsite2;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
url2 = f"mssql+pyodbc:///?odbc_connect={params2}"
try:
    engine2 = create_engine(url2)
    with engine2.connect() as conn:
        result = conn.execute(text('SELECT @@VERSION'))
        print('localhost: OK')
except Exception as e:
    print('localhost: FAILED')
