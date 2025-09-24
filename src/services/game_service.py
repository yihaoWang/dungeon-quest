import json
import time
from datetime import datetime
from typing import Dict, Any
from .llm_service import LLMService
from .vector_service import VectorService
from ..models.game_state import GameState, Language
from ..utils.logger import setup_logger
from ..localization import Messages

class GameService:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.llm_service = LLMService()
        self.vector_service = VectorService()
        self.previous_events = {}

    async def process_player_action(self, game_state: GameState, action: str) -> Dict[str, Any]:
        start_time = time.time()
        self.logger.info(f"🚀 [TIMING] Start processing action: {action} for game {game_state.game_id}")

        try:
            # Step 1: Search relevant events
            search_start = time.time()
            relevant_events = await self._search_relevant_events(game_state, action)
            search_time = time.time() - search_start
            self.logger.info(f"⏱️ [TIMING] RAG search took: {search_time:.3f}s")

            # Step 2: Generate game event
            llm_start = time.time()
            game_event = await self._generate_game_event(game_state, action, relevant_events)
            llm_time = time.time() - llm_start
            self.logger.info(f"⏱️ [TIMING] LLM generation took: {llm_time:.3f}s")

            # Step 3: Update previous event memory
            narrative = game_event.get("narrative", "")
            turn = game_event.get("turn", game_state.turn_count + 1)
            self.previous_events[game_state.game_id] = f"[Turn {turn}] {narrative}"

            # Step 4: Store in RAG
            store_start = time.time()
            await self._store_event_in_rag(game_state, game_event)
            store_time = time.time() - store_start
            self.logger.info(f"⏱️ [TIMING] RAG storage took: {store_time:.3f}s")

            total_time = time.time() - start_time
            self.logger.info(f"✅ [TIMING] Total processing took: {total_time:.3f}s")

            return game_event
        except Exception as e:
            self.logger.error(f"Failed to process action: {e}")
            return self._get_fallback_event(game_state, action)

    async def _search_relevant_events(self, game_state: GameState, action: str) -> list:
        try:
            search_start = time.time()
            relevant_events = []

            # Get previous event and build query
            previous_event = self.previous_events.get(game_state.game_id, "")
            if previous_event:
                relevant_events.append({"content": previous_event, "similarity": 1.0})
                
            query = f"{action} following {previous_event}" if previous_event else f"{action} combat battle adventure"

            vector_start = time.time()
            self.logger.info(f"🔍 [DEBUG] Searching with contextual query: '{query}'")

            results = await self.vector_service.semantic_search(
                query=query,
                content_type="game_event",
                limit=2,
                similarity_threshold=0.3,
                game_id=game_state.game_id
            )
            self.logger.info(f"🔍 [DEBUG] Vector search found {len(results)} results with threshold 0.3")

            if not results:
                self.logger.info(f"🔍 [DEBUG] Trying search with action only: '{action}'")
                results = await self.vector_service.semantic_search(
                    query=action,
                    content_type="game_event",
                    limit=2,
                    similarity_threshold=0.3,
                    game_id=game_state.game_id
                )
                self.logger.info(f"🔍 [DEBUG] Action-only search found {len(results)} results")

            relevant_events.extend(results)
            vector_time = time.time() - vector_start
            self.logger.info(f"🔍 [TIMING] Vector search took: {vector_time:.3f}s")

            total_search_time = time.time() - search_start
            self.logger.info(f"📊 [TIMING] Total search took: {total_search_time:.3f}s, found {len(relevant_events)} events")

            return relevant_events
        except Exception as e:
            self.logger.error(f"RAG search failed: {e}")
            return []

    def _get_prompt_by_language(self, game_state: GameState, action: str, context: str) -> str:
        language_instruction = Messages.get_language_instruction(game_state.language)

        inventory_str = ", ".join(game_state.player.inventory) if game_state.player.inventory else "empty"

        return f"""Based on the game state and historical events below, generate a game event responding to the player's action.

Game State:
- Player: {game_state.player.name}
- HP: {game_state.player.hp}/{game_state.player.max_hp}
- Level: {game_state.player.level}
- Experience: {game_state.player.experience}
- Turn: {game_state.turn_count + 1}
- Inventory: {inventory_str}

Player Action: {action}

Relevant Historical Events:
{context}

Generate JSON response:
{{
  "turn": {game_state.turn_count + 1},
  "narrative": "narrative text",
  "effects": {{
    "player_hp_change": 0,
    "player_exp_gain": 0,
    "item_gain": null
  }},
  "suggested_actions": ["action1", "action2", "action3"]
}}

Requirements:
- Narrative should be vivid, suspenseful, and immersive, fitting the game context.
- Every **third turn (3, 6, 9)** MUST feature a monster encounter, regardless of player action.
- Effects should be reasonable, considering player level and action.
- For combat, always include some randomness (success, failure, critical hit, enemy counterattack).
- Suggested_actions must provide 3 contextual and meaningful choices.
- Exploration should frequently lead to new dangers, often triggering combat.
- 70% of encounters should involve monsters (goblins, skeletons, orcs, treasure guardians, dragons).
- Turn escalation:
  - Turns 1–3: light encounters, basic monsters.
  - Turns 4–6: stronger monsters, minor traps, rare loot.
  - Turns 7–9: elite monsters, ambushes, treasure guardians.
  - Turn 8–9 must foreshadow or introduce the **final boss**.
  - Turn 10: epic conclusion (victory, defeat, or narrow escape).
- Make battles cinematic: emphasize sound, movement, and environment.
- Keep pacing fast and exciting — avoid long pauses without conflict.
- IMPORTANT: Respond {language_instruction}
"""

    async def _generate_game_event(self, game_state: GameState, action: str, relevant_events: list) -> Dict[str, Any]:
        try:
            context = self._build_context(game_state, relevant_events)
            prompt = self._get_prompt_by_language(game_state, action, context)

            client = self.llm_service.get_client()
            response = await client.chat.completions.create(
                model="gpt-5-nano",
                messages=[{"role": "user", "content": prompt}]
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            self.logger.error(f"LLM generation failed: {e}")
            return self._get_fallback_event(game_state, action)

    def _build_context(self, game_state: GameState, relevant_events: list) -> str:
        if not relevant_events:
            return Messages.get_context_no_events(game_state.language)

        context_parts = []
        for event in relevant_events:
            if isinstance(event, dict):
                content = str(event.get('content', ''))
                similarity = event.get('similarity', 0)
                context_parts.append(f"- {content} (similarity: {similarity:.2f})")
            else:
                # Handle case where event is not a dict
                context_parts.append(f"- {str(event)}")

        return "\n".join(context_parts)

    async def _store_event_in_rag(self, game_state: GameState, game_event: Dict[str, Any]):
        try:
            turn = game_event.get('turn', game_state.turn_count + 1)
            narrative = game_event.get('narrative', '')
            effects = game_event.get('effects', {})

            doc_id = f"{game_state.game_id}_turn_{turn}"
            content = f"[Turn {turn}] {narrative}"

            if effects:
                hp_change = effects.get('player_hp_change', 0)
                exp_gain = effects.get('player_exp_gain', 0)
                content += f" Status changes: HP{hp_change:+d}, EXP{exp_gain:+d}"

            metadata = {
                "game_id": game_state.game_id,
                "turn": turn,
                "player_name": game_state.player.name,
                "hp_after": max(0, game_state.player.hp + effects.get('player_hp_change', 0)),
                "exp_after": game_state.player.experience + effects.get('player_exp_gain', 0),
                "created_at": datetime.utcnow().isoformat()
            }

            await self.vector_service.store_knowledge(
                content_type="game_event",
                content_id=doc_id,
                title=f"Turn {turn} - {game_state.player.name}",
                content=content,
                metadata=metadata
            )

            self.logger.info(f"Stored game event in RAG: {doc_id}")

        except Exception as e:
            self.logger.error(f"Failed to store event in RAG: {e}")

    def _get_fallback_event(self, game_state: GameState, action: str) -> Dict[str, Any]:
        fallback_events = Messages.get_fallback_events(game_state.language)
        default_narrative = Messages.get_default_narrative(game_state.language)
        default_suggested_actions = Messages.get_default_suggested_actions(game_state.language)

        for keyword, event in fallback_events.items():
            if keyword in action.lower():
                return {
                    "turn": 0,
                    "narrative": event["narrative"],
                    "effects": event["effects"],
                    "suggested_actions": event["suggested_actions"]
                }

        return {
            "turn": 0,
            "narrative": default_narrative,
            "effects": {"player_hp_change": 0, "player_exp_gain": 5, "item_gain": None},
            "suggested_actions": default_suggested_actions
        }
