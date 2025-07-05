import os
from sqlite3 import connect,Connection,Cursor
from .helper import checkSqlite, initSqlite

# Removed automatic openai installation to prevent Fusion 360 startup issues
# The add-in will use mock AI responses if openai is not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not available. Using mock AI responses.")

class FusionGPT:

    api:OpenAI
    sqlite:Connection
    cursor:Cursor
    path:str

    def __init__(self):
        self.api                    = None
        self.sqlite                 = None
        self.cursor                 = None
        self.path                   = os.path.dirname(__file__)
        if not checkSqlite():
            initSqlite()
        self.sqlite                 = connect(os.path.join(self.path,"fusionGPT.db"))
        self.cursor                 = self.sqlite.cursor()
        
        # Only attempt to set up OpenAI if the library is available
        if OPENAI_AVAILABLE:
            if not self.__checkOpenAIKey():
                print("OpenAI API Key not found. Using mock AI responses.")
            elif not self.__checkOpenAIKeyValid():
                print("OpenAI API Key invalid. Using mock AI responses.")
        else:
            print("OpenAI library not installed. Using mock AI responses for testing.")

    def __checkOpenAIKey(self) -> bool:
        if not OPENAI_AVAILABLE:
            return False
            
        self.cursor.execute("SELECT value FROM keys WHERE name='OPENAI_API_KEY'")
        key = self.cursor.fetchone()
        if key is None:
            return False
        else:
            self.api = OpenAI(api_key=key[0])
        return True

    def __checkOpenAIKeyValid(self) -> bool:
        if not OPENAI_AVAILABLE or self.api is None:
            return False
            
        try:
            models = self.api.models.list().to_dict()
            if len(models) > 0:
                return True
            else:
                return False
        except:
            return False