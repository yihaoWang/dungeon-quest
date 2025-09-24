from typing import Dict, Any
from ..models.game_state import Language
from . import en, zh_tw

class Messages:
    LANGUAGE_MODULES = {
        Language.EN: en,
        Language.ZH_TW: zh_tw
    }

    @classmethod
    def _get_module(cls, language: Language):
        return cls.LANGUAGE_MODULES.get(language, cls.LANGUAGE_MODULES[Language.EN])

    @classmethod
    def get_fallback_events(cls, language: Language) -> Dict[str, Any]:
        return cls._get_module(language).FALLBACK_EVENTS

    @classmethod
    def get_default_narrative(cls, language: Language) -> str:
        return cls._get_module(language).DEFAULT_NARRATIVE

    @classmethod
    def get_language_instruction(cls, language: Language) -> str:
        return cls._get_module(language).LANGUAGE_INSTRUCTION

    @classmethod
    def get_context_no_events(cls, language: Language) -> str:
        return cls._get_module(language).CONTEXT_NO_EVENTS

    @classmethod
    def get_default_suggested_actions(cls, language: Language) -> list:
        return cls._get_module(language).DEFAULT_SUGGESTED_ACTIONS