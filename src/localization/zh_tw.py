FALLBACK_EVENTS = {
    "attack": {
        "narrative": "你向哥布林揮劍，成功擊中！牠憤怒地咆哮，準備反擊。",
        "effects": {"player_hp_change": -5, "player_exp_gain": 15, "item_gain": None},
        "suggested_actions": ["再次攻擊", "防禦", "使用特殊技能"]
    },
    "explore": {
        "narrative": "當你探索陰暗的走廊時，一個骷髏戰士從陰影中現身，骨頭發出可怕的響聲！",
        "effects": {"player_hp_change": 0, "player_exp_gain": 5, "item_gain": None},
        "suggested_actions": ["攻擊骷髏", "逃跑", "準備戰鬥"]
    },
    "rest": {
        "narrative": "你坐下休息，但突然聽到附近的咆哮聲。一個獸人發現了你！",
        "effects": {"player_hp_change": 10, "player_exp_gain": 0, "item_gain": None},
        "suggested_actions": ["與獸人戰鬥", "嘗試躲藏", "嘗試談判"]
    }
}

DEFAULT_NARRATIVE = "遠方有神秘的影子在移動。前方潛伏著危險的東西！"

DEFAULT_SUGGESTED_ACTIONS = ["調查威脅", "準備戰鬥", "搜尋敵人"]

LANGUAGE_INSTRUCTION = "in Traditional Chinese"

CONTEXT_NO_EVENTS = "無相關歷史事件"