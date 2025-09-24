import uuid
from typing import Dict, Optional
from .models.game_state import GameState, Player, GameStatus, GameResponse, Language
from .services.game_service import GameService
from .utils.logger import setup_logger


class GameController:
    def __init__(self):
        self.games: Dict[str, GameState] = {}
        self.game_service = GameService()
        self.logger = setup_logger(__name__)

    def create_new_game(self, player_name: str = "Adventurer", language: Language = Language.EN) -> str:
        game_id = str(uuid.uuid4())
        game_state = GameState(
            game_id=game_id,
            player=Player(name=player_name),
            language=language
        )
        self.games[game_id] = game_state
        self.logger.info(f"Created new game {game_id} for player {player_name} in {language}")
        return game_id

    def get_game(self, game_id: str) -> Optional[GameState]:
        return self.games.get(game_id)

    async def process_action(self, game_id: str, action: str) -> Optional[GameResponse]:
        game_state = self.get_game(game_id)
        if not game_state or game_state.status != GameStatus.ACTIVE:
            return None

        game_event = await self.game_service.process_player_action(game_state, action)

        self.apply_game_effects(game_state, game_event)

        narrative = game_event.get("narrative", "Something happened...")

        game_state.story_history.append(f"Player: {action}")
        game_state.story_history.append(f"Game: {narrative}")

        available_actions = game_event.get("suggested_actions", self.get_suggested_actions(game_state))

        return GameResponse(
            game_id=game_id,
            narrative=narrative,
            player_state=game_state.player,
            available_actions=available_actions,
            game_status=game_state.status
        )

    def apply_game_effects(self, game_state: GameState, game_event: Dict):
        effects = game_event.get("effects", {})
        turn = game_event.get("turn", 0)

        if turn > 0:
            game_state.turn_count = turn

        # End game at turn 10
        if game_state.turn_count >= 10:
            game_state.status = GameStatus.COMPLETED

        hp_change = effects.get("player_hp_change", 0)
        if hp_change != 0:
            game_state.player.hp = max(0, min(
                game_state.player.hp + hp_change,
                game_state.player.max_hp
            ))
            if game_state.player.hp == 0:
                game_state.status = GameStatus.GAME_OVER

        exp_gain = effects.get("player_exp_gain", 0)
        if exp_gain > 0:
            game_state.player.experience += exp_gain
            if game_state.player.experience >= game_state.player.level * 100:
                game_state.player.level += 1
                game_state.player.max_hp += 10
                game_state.player.hp = game_state.player.max_hp
                self.logger.info(f"Player leveled up to {game_state.player.level}")

        item_gain = effects.get("item_gain")
        if item_gain and item_gain not in game_state.player.inventory:
            game_state.player.inventory.append(item_gain)

    def get_suggested_actions(self, game_state: GameState) -> list:
        if game_state.player.hp <= 20:
            return ["rest", "use healing item", "explore carefully"]
        elif game_state.player.level < 3:
            return ["explore", "attack monster", "search for items"]
        else:
            return ["explore deeper", "face boss", "use special ability"]