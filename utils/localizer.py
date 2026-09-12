"""
# utils/localizer.py

이 모듈은 본 현지화 파일 구조를 따르는 모든 프로그램에 범용적으로 사용 가능한 현지화 유틸리티를 제공합니다.

특히 디스코드 봇 개발에 있어, 명령어의 이름과 설명, 그리고 임베드 메시지의 내용 등 다양한 문자열을 다국어로 지원할 수 있도록 설계되었습니다.

---

현지화 파일 구조는 다음과 같습니다:
    localization/
        en-US.json
        ko.json
        ...
"""

import json
import random
from pathlib import Path
from functools import cache


DEFAULT_LOCALE = "en-US"
DIRECTORY = Path(__file__).resolve().parent.parent / "localization"

data: dict[str, dict[str, str | list[str]]] = {}


def reload() -> None:
    """
    localization 디렉토리의 JSON 파일을 다시 불러옵니다.
    """
    data.clear()
    
    for file in DIRECTORY.glob("*.json"):
        with file.open("r", encoding="utf-8") as f:
            data[file.stem] = json.load(f)
    
    all.cache_clear()

@cache
def all(key: str) -> dict[str, str]:
    """
    모든 로케일에 대한 특정 키의 현지화 문자열을 반환합니다.
    
    EX)
        from utils import localizer
        print(localizer.all("large_name"))
        
        > {'en-US': 'Emoji Enlarger', 'ko': '이모지 확대'}
    """
    result: dict[str, str] = {}
    
    for locale, content in data.items():
        if key not in content: continue
        
        value = content[key]
        
        if isinstance(value, str):
            result[locale] = value
    
    return result

def get(key: str, locale: str | None = None, **kwargs) -> str:
    """
    특정 로케일에 대한 현지화 문자열을 반환합니다.
    
    locale 값은 nextcord.Interaction.locale 값과 동일한 형식이어야 합니다.
    locale 값이 None일 경우 DEFAULT_LOCALE 값이 사용됩니다.
    
    EX)
        from utils import localizer
        print(localizer.get("large_name", "ko"))
        
        > 이모지 확대
        
        ---
        
        from utils import localizer
        print(localizer.get("large_name"))
        
        > Emoji Enlarger
    """
    locale = locale if locale in data else DEFAULT_LOCALE
        
    content = data[locale]
    
    if key not in content:
        content = data[DEFAULT_LOCALE]
    
    if key not in content:
        raise KeyError(f"Localization key not found: {key}")
    
    value = content[key]
    
    if isinstance(value, list):
        value = random.choice(value)
    
    return value.format(**kwargs)

reload() # 최초 로딩 시 localization 디렉토리의 JSON 파일을 불러옵니다.