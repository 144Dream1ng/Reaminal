# utils/localizer.py
import json
import random
from pathlib import Path


class Localizer:
    def __init__(self, directory: str = "./localization"):
        self.directory = Path(directory)
        self.data = {}
        
        self.load_all()
    
    def load_all(self):
        for file in self.directory.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                self.data[file.stem] = json.load(f)
    
    def get(self, key: str) -> dict:
        return {lang: content.get(key) for lang, content in self.data.items()}
    
    def get_with_locale(self, key: str, locale) -> str:
        if locale not in self.data.keys(): locale = "en-US"
        msg = self.data[locale][key]
        
        if type(msg) == list:
            return random.choice(msg)
        else:
            return msg 

_instance = Localizer()
get = _instance.get
gwl = _instance.get_with_locale