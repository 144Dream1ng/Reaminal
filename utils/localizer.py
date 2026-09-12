# utils/localizer.py
import json
import random
from pathlib import Path
from functools import cache


class Localizer:
    DEFAULT_LOCALE = "en-US"
    
    def __init__(self, directory: str | Path | None = None):
        if directory is None:
            directory = Path(__file__).resolve().parent.parent / "localization"
        
        self.directory = Path(directory)
        self.data: dict[str, dict[str, str | list[str]]] = {}
        
        self.reload()
    
    def reload(self) -> None:
        self.data.clear()
        
        for file in self.directory.glob("*.json"):
            with file.open("r", encoding="utf-8") as f:
                self.data[file.stem] = json.load(f)
        
        self.all.cache_clear()
    
    @cache
    def all(self, key: str) -> dict[str, str]:
        result: dict[str, str] = {}
        
        for locale, content in self.data.items():
            if key not in content: continue
            
            value = content[key]
            if isinstance(value, str): result[locale] = value
        
        return result
    
    def get(self, key: str, locale: str | None, **kwargs) -> str:
        locale = locale or self.DEFAULT_LOCALE
        
        if locale not in self.data:
            locale = self.DEFAULT_LOCALE
        
        content = self.data[locale]
        
        if key not in content:
            content = self.data[self.DEFAULT_LOCALE]
        
        if key not in content:
            raise KeyError(f"Localization key not found: {key}")
        
        value = content[key]
        
        if isinstance(value, list):
            value = random.choice(value)
        
        return value.format(**kwargs)
    
    def default(self, key: str, **kwargs) -> str:
        return self.get(key, self.DEFAULT_LOCALE, **kwargs)