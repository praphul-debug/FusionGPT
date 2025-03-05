import os
from sqlite3 import connect
from .helper import install, checkSqlite, initSqlite

try:
    from openai import OpenAI
except:
    install('openai')
    from openai import OpenAI

class FusionGPT:

    def __init__(self):
        self.api = None
        self.sqlite = None
        self.cursor = None
        self.path = os.path.dirname(__file__)
        if not checkSqlite():
            initSqlite()
        self.sqlite = connect(os.path.join(self.path,"fusionGPT.db"))
        self.cursor = self.sqlite.cursor()
        if not self.__checkOpenAIKey():
            print("OpenAI API Key not found. Please add it using the 'setOpenAIKey' command.")
        if not self.__checkOpenAIKeyValid():
            print("OpenAI API Key invalid. Please add a valid key using the 'setOpenAIKey' command.")

    def __checkOpenAIKey(self) -> bool:
        self.cursor.execute("SELECT value FROM keys WHERE name='OPENAI_API_KEY'")
        key = self.cursor.fetchone()
        if key is None:
            return False
        else:
            self.api = OpenAI(api_key=key[0])
        return True

    def __checkOpenAIKeyValid(key: str) -> bool:
        openai = OpenAI(api_key=key)
        try:
            models = openai.models.list().to_dict()
            if len(models) > 0:
                return True
            else:
                return False
        except:
            return False
