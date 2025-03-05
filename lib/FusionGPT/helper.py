import subprocess
import sys
import os

from sqlite3 import connect

def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def checkSqlite() -> bool:
    conn = connect(os.path.join(os.path.dirname(__file__),"fusionGPT.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keys'")
    if cursor.fetchone() is None:
        conn.close()
        return False
    conn.close()
    return True

def initSqlite():
    conn = connect(os.path.join(os.path.dirname(__file__),"fusionGPT.db"))
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE keys (
    id    INTEGER    PRIMARY KEY AUTOINCREMENT
                    UNIQUE,
    name  TEXT (255) UNIQUE,
    value TEXT)
    ''')
    conn.commit()
    conn.close()
