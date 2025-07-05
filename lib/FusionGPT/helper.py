import subprocess
import sys
import os

from sqlite3 import connect

def install(package):
    """
    Note: This function is kept for compatibility but should not be used during add-in startup
    as it can cause Fusion 360 to show "Multiple instances" error.
    """
    print(f"Warning: Automatic installation of {package} is disabled to prevent Fusion 360 startup issues.")
    print(f"Please install {package} manually if needed, or use the mock AI responses.")

def freeze():
    subprocess.check_call([sys.executable, "-m", "pip", "freeze"])

def checkSqlite() -> bool:
    try:
        conn = connect(os.path.join(os.path.dirname(__file__),"fusionGPT.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keys'")
        result = cursor.fetchone() is not None
        conn.close()
        return result
    except:
        return False

def initSqlite():
    try:
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
    except Exception as e:
        print(f"Error initializing SQLite database: {e}")