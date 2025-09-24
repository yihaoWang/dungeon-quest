FALLBACK_EVENTS = {
    "attack": {
        "narrative": "You strike at the goblin, landing a solid hit! It snarls and prepares to counter-attack.",
        "effects": {"player_hp_change": -5, "player_exp_gain": 15, "item_gain": None},
        "suggested_actions": ["attack again", "defend", "use special ability"]
    },
    "explore": {
        "narrative": "As you explore the dark corridor, a skeleton warrior emerges from the shadows, bones rattling menacingly!",
        "effects": {"player_hp_change": 0, "player_exp_gain": 5, "item_gain": None},
        "suggested_actions": ["attack skeleton", "flee", "prepare for battle"]
    },
    "rest": {
        "narrative": "You sit down to rest, but suddenly hear growling nearby. An orc has spotted you!",
        "effects": {"player_hp_change": 10, "player_exp_gain": 0, "item_gain": None},
        "suggested_actions": ["fight the orc", "try to hide", "negotiate"]
    }
}

DEFAULT_NARRATIVE = "A mysterious shadow moves in the distance. Something dangerous lurks ahead!"

DEFAULT_SUGGESTED_ACTIONS = ["investigate threat", "prepare for battle", "search for enemies"]

LANGUAGE_INSTRUCTION = "in English"

CONTEXT_NO_EVENTS = "No relevant historical events"

SUGGESTED_ACTIONS_BY_SITUATION = {
    "low_hp": ["rest", "use healing item", "explore carefully"],
    "low_level": ["explore", "attack monster", "search for items"],
    "high_level": ["explore deeper", "face boss", "use special ability"]
}