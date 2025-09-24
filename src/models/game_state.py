from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum


class GameStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    GAME_OVER = "game_over"


class Language(str, Enum):
    EN = "en"
    ZH_TW = "zh_tw"


class Player(BaseModel):
    name: str = "Adventurer"
    hp: int = 100
    max_hp: int = 100
    experience: int = 0
    level: int = 1
    inventory: List[str] = []
    location: str = "entrance"


class GameState(BaseModel):
    game_id: str
    player: Player
    status: GameStatus = GameStatus.ACTIVE
    turn_count: int = 0
    story_history: List[str] = []
    current_scene: str = ""
    language: Language = Language.EN


class PlayerAction(BaseModel):
    action: str
    game_id: str


class GameResponse(BaseModel):
    game_id: str
    narrative: str
    player_state: Player
    available_actions: List[str]
    game_status: GameStatus