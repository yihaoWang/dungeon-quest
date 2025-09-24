#!/usr/bin/env python3

import asyncio
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.vector_service import VectorService
from src.utils.logger import setup_logger

SAMPLE_MONSTERS = {
    # Boss Level
    "fire_dragon": {
        "name": "Fire Dragon",
        "description": "A massive red dragon that breathes scorching flames. Its scales shimmer like molten lava and its eyes burn with ancient fury. Known to hoard treasure in volcanic caves. This legendary beast can incinerate entire armies with a single breath.",
        "stats": {"hp": 500, "attack": 85, "defense": 60, "speed": 40},
        "abilities": ["Fire Breath", "Wing Attack", "Tail Swipe", "Intimidate"],
        "type": "boss",
        "element": "fire",
        "loot": ["Dragon Scale", "Fire Gem", "Ancient Coin"]
    },
    "ice_queen": {
        "name": "Ice Queen",
        "description": "An ancient sorceress trapped in eternal ice. Her beauty is matched only by her cruelty. She commands blizzards and can freeze enemies solid with a glance.",
        "stats": {"hp": 450, "attack": 70, "defense": 80, "speed": 30},
        "abilities": ["Blizzard", "Ice Prison", "Frost Nova", "Frozen Heart"],
        "type": "boss",
        "element": "ice",
        "loot": ["Ice Crown", "Frozen Tear", "Eternal Crystal"]
    },

    # Elite Level
    "shadow_wolf": {
        "name": "Shadow Wolf",
        "description": "A ghostly wolf that emerges from darkness. Its form flickers between solid and ethereal, making it difficult to target. Hunts in packs during moonless nights.",
        "stats": {"hp": 120, "attack": 45, "defense": 25, "speed": 70},
        "abilities": ["Shadow Strike", "Phase Step", "Howl"],
        "type": "elite",
        "element": "dark",
        "loot": ["Shadow Essence", "Wolf Fang"]
    },
    "stone_golem": {
        "name": "Stone Golem",
        "description": "A massive construct of ancient stone and magic. Its rocky hide deflects most attacks, and its fists can crush bones to powder. Created by forgotten wizards to guard sacred places.",
        "stats": {"hp": 200, "attack": 60, "defense": 80, "speed": 20},
        "abilities": ["Rock Slam", "Stone Skin", "Earthquake"],
        "type": "elite",
        "element": "earth",
        "loot": ["Stone Core", "Magic Rune", "Heavy Boulder"]
    },
    "lightning_eagle": {
        "name": "Lightning Eagle",
        "description": "A majestic bird wreathed in crackling electricity. Its piercing cry can summon thunderstorms, and its talons deliver shocking strikes.",
        "stats": {"hp": 100, "attack": 55, "defense": 30, "speed": 90},
        "abilities": ["Lightning Strike", "Thunder Call", "Wind Slash"],
        "type": "elite",
        "element": "lightning",
        "loot": ["Storm Feather", "Lightning Gem", "Wind Crystal"]
    },

    # Common Level
    "goblin_warrior": {
        "name": "Goblin Warrior",
        "description": "A small but fierce green-skinned humanoid wielding crude weapons. Despite their size, goblins are cunning fighters who use numbers and dirty tactics to their advantage.",
        "stats": {"hp": 60, "attack": 25, "defense": 15, "speed": 55},
        "abilities": ["Backstab", "Throw Rock", "Battle Cry"],
        "type": "common",
        "element": "none",
        "loot": ["Rusty Dagger", "Goblin Ear", "Small Coin"]
    },
    "skeleton_warrior": {
        "name": "Skeleton Warrior",
        "description": "The reanimated bones of a fallen soldier. These undead guardians fight with the muscle memory of their past lives, wielding ancient weapons with deadly precision.",
        "stats": {"hp": 80, "attack": 30, "defense": 20, "speed": 35},
        "abilities": ["Bone Strike", "Rattle", "Death Grip"],
        "type": "common",
        "element": "undead",
        "loot": ["Bone Fragment", "Rusty Armor", "Ancient Coin"]
    },
    "cave_spider": {
        "name": "Cave Spider",
        "description": "A venomous arachnid the size of a large dog. Its bite injects paralytic poison, and it can web enemies to immobilize them before striking.",
        "stats": {"hp": 40, "attack": 35, "defense": 10, "speed": 65},
        "abilities": ["Poison Bite", "Web Trap", "Leap Attack"],
        "type": "common",
        "element": "poison",
        "loot": ["Spider Silk", "Poison Gland", "Spider Leg"]
    },
    "orc_brute": {
        "name": "Orc Brute",
        "description": "A hulking green-skinned humanoid with immense physical strength. Orcs are savage warriors who prefer brute force over strategy.",
        "stats": {"hp": 100, "attack": 40, "defense": 25, "speed": 30},
        "abilities": ["Brutal Swing", "Rage", "Intimidate"],
        "type": "common",
        "element": "none",
        "loot": ["Orc Tooth", "Iron Club", "Leather Hide"]
    },
    "fire_imp": {
        "name": "Fire Imp",
        "description": "A mischievous demonic creature wreathed in flames. Small but agile, it delights in burning everything it touches.",
        "stats": {"hp": 50, "attack": 30, "defense": 15, "speed": 70},
        "abilities": ["Fireball", "Flame Dash", "Burn"],
        "type": "common",
        "element": "fire",
        "loot": ["Imp Horn", "Fire Essence", "Sulfur"]
    }
}

SAMPLE_ITEMS = {
    # Consumables
    "healing_potion": {
        "name": "Healing Potion",
        "description": "A glowing red liquid in a crystal vial. When consumed, it instantly restores health through magical regeneration. The potion tastes of mint and honey.",
        "type": "consumable",
        "effects": "Restores 50 HP instantly",
        "value": 25,
        "rarity": "common"
    },
    "mana_potion": {
        "name": "Mana Potion",
        "description": "A shimmering blue elixir that sparkles with arcane energy. Drinking it restores magical power and clarity of mind.",
        "type": "consumable",
        "effects": "Restores 30 MP instantly",
        "value": 30,
        "rarity": "common"
    },
    "strength_elixir": {
        "name": "Elixir of Strength",
        "description": "A thick, golden potion that enhances physical prowess. The drinker feels their muscles surge with temporary power.",
        "type": "consumable",
        "effects": "Increases attack by 15 for 5 turns",
        "value": 75,
        "rarity": "uncommon"
    },
    "phoenix_feather": {
        "name": "Phoenix Feather",
        "description": "A radiant feather from the legendary phoenix. It glows with the power of rebirth and can bring the dead back to life.",
        "type": "consumable",
        "effects": "Fully revives and heals to maximum HP",
        "value": 500,
        "rarity": "legendary"
    },

    # Weapons
    "rusty_sword": {
        "name": "Rusty Sword",
        "description": "An old, weathered blade showing signs of age and neglect. Despite its appearance, it still holds an edge.",
        "type": "weapon",
        "effects": "Increases attack by 5",
        "value": 10,
        "rarity": "common"
    },
    "fire_sword": {
        "name": "Flaming Sword",
        "description": "An enchanted blade wreathed in eternal flames. The fire never dies and burns hotter in battle. Forged by ancient fire mages in the volcanic depths.",
        "type": "weapon",
        "effects": "Increases attack by 30, adds fire damage",
        "value": 500,
        "rarity": "rare",
        "requirements": "Level 10+"
    },
    "ice_staff": {
        "name": "Staff of Eternal Ice",
        "description": "A crystalline staff that never melts, no matter how hot the environment. It channels the power of endless winter.",
        "type": "weapon",
        "effects": "Increases magic attack by 35, adds ice damage",
        "value": 600,
        "rarity": "rare",
        "requirements": "Intelligence 20+"
    },
    "dragon_slayer": {
        "name": "Dragon Slayer",
        "description": "A legendary sword forged from meteorite metal and dragon bone. Its blade can cut through the thickest dragon scales.",
        "type": "weapon",
        "effects": "Increases attack by 50, +100% damage vs dragons",
        "value": 2000,
        "rarity": "legendary",
        "requirements": "Level 25+, Strength 30+"
    },

    # Armor
    "leather_armor": {
        "name": "Leather Armor",
        "description": "Basic protection made from tanned animal hide. Lightweight and flexible, perfect for beginners.",
        "type": "armor",
        "effects": "Increases defense by 8",
        "value": 50,
        "rarity": "common"
    },
    "shadow_cloak": {
        "name": "Cloak of Shadows",
        "description": "A dark cloak that seems to absorb light around it. When worn, the wearer becomes one with the shadows, gaining the ability to move unseen.",
        "type": "armor",
        "effects": "Increases stealth by 25, reduces enemy accuracy by 15%",
        "value": 300,
        "rarity": "uncommon",
        "requirements": "Agility 15+"
    },
    "plate_mail": {
        "name": "Steel Plate Mail",
        "description": "Heavy armor crafted from reinforced steel plates. Provides excellent protection but limits mobility.",
        "type": "armor",
        "effects": "Increases defense by 25, reduces speed by 10",
        "value": 400,
        "rarity": "uncommon",
        "requirements": "Strength 18+"
    },
    "dragon_scale_armor": {
        "name": "Dragon Scale Armor",
        "description": "Armor crafted from the impenetrable scales of an ancient dragon. It provides unmatched protection and resistance to magical attacks.",
        "type": "armor",
        "effects": "Increases defense by 40, magic resistance +30%",
        "value": 1500,
        "rarity": "legendary",
        "requirements": "Level 20+, Constitution 25+"
    },

    # Accessories
    "ring_of_power": {
        "name": "Ring of Power",
        "description": "A simple gold band that radiates with inner energy. It enhances the wearer's natural abilities.",
        "type": "accessory",
        "effects": "Increases all stats by 5",
        "value": 200,
        "rarity": "uncommon"
    },
    "amulet_of_health": {
        "name": "Amulet of Health",
        "description": "A jade pendant carved with ancient healing runes. It continuously mends minor wounds and boosts vitality.",
        "type": "accessory",
        "effects": "Increases max HP by 50, HP regeneration +2 per turn",
        "value": 350,
        "rarity": "rare"
    },
    "boots_of_speed": {
        "name": "Boots of Speed",
        "description": "Enchanted boots that make the wearer swift as the wind. They leave no tracks and make no sound.",
        "type": "accessory",
        "effects": "Increases speed by 20, grants double movement",
        "value": 280,
        "rarity": "rare"
    }
}


class ChromaDBInitializer:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.vector_service = None

    async def initialize(self, force_reset: bool = False, skip_api_check: bool = False):
        """Initialize ChromaDB with sample data"""
        self.logger.info("🚀 Starting ChromaDB initialization...")

        # Check for OpenAI API key
        import os
        if not skip_api_check and not os.getenv("OPENAI_API_KEY"):
            self.logger.error("❌ OpenAI API key not found!")
            self.logger.error("   Please set OPENAI_API_KEY environment variable")
            self.logger.error("   export OPENAI_API_KEY=your_api_key_here")
            self.logger.error("   Or use --skip-api-check for testing (embeddings will fail)")
            return False

        # Initialize vector service
        try:
            self.vector_service = VectorService()
            self.logger.info("✅ ChromaDB connection established")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize VectorService: {e}")
            return False

        # Check existing data
        if not force_reset:
            existing_count = self.vector_service.get_knowledge_count()
            if existing_count > 0:
                self.logger.info(f"📊 Found {existing_count} existing entries")
                self.logger.info("Use --force to skip this prompt")
                return True  # Skip if data exists and no force flag

        # Clear existing data if requested
        if force_reset:
            await self.clear_existing_data()

        # Ingest sample data
        success = await self.ingest_sample_data()

        if success:
            self.logger.info("🎉 ChromaDB initialization completed successfully!")
            await self.display_summary()
        else:
            self.logger.error("❌ ChromaDB initialization failed")

        return success

    async def clear_existing_data(self):
        """Clear all existing monster and item data"""
        try:
            self.logger.info("🧹 Clearing existing data...")

            # Get counts before clearing
            total_before = self.vector_service.get_knowledge_count()
            monster_before = self.vector_service.get_knowledge_count("monster")
            item_before = self.vector_service.get_knowledge_count("item")

            # Clear data
            monster_count = self.vector_service.knowledge_model.clear_knowledge("monster")
            item_count = self.vector_service.knowledge_model.clear_knowledge("item")

            self.logger.info(f"✅ Cleared {monster_count} monsters and {item_count} items")
            self.logger.info(f"📊 Before: {total_before} total ({monster_before} monsters, {item_before} items)")

        except Exception as e:
            self.logger.warning(f"⚠️ Failed to clear existing data: {e}")

    async def reset_database(self):
        """Reset the entire database to fix dimension issues"""
        try:
            self.logger.info("🔄 Resetting entire database...")

            # Use database model's reset function
            success = self.vector_service.database_model.reset_database()
            if success:
                self.logger.info("✅ Database reset successful")
            else:
                self.logger.warning("⚠️ Database reset may have failed")

        except Exception as e:
            self.logger.error(f"❌ Failed to reset database: {e}")
            # Try manual cleanup
            try:
                import shutil
                import os
                persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
                if os.path.exists(persist_dir):
                    shutil.rmtree(persist_dir)
                    self.logger.info("✅ Manually cleaned database directory")
            except Exception as e2:
                self.logger.error(f"❌ Manual cleanup also failed: {e2}")

    async def ingest_sample_data(self):
        """Ingest sample monsters and items into ChromaDB"""
        try:
            self.logger.info("📥 Ingesting sample data...")

            success = await self.vector_service.ingest_game_data(
                monsters_data=SAMPLE_MONSTERS,
                items_data=SAMPLE_ITEMS
            )

            if success:
                self.logger.info("✅ Sample data ingested successfully")
                return True
            else:
                self.logger.error("❌ Failed to ingest sample data")
                return False

        except Exception as e:
            self.logger.error(f"❌ Failed to ingest sample data: {e}")
            return False

    async def display_summary(self):
        """Display summary of ingested data"""
        try:
            total_count = self.vector_service.get_knowledge_count()
            monster_count = self.vector_service.get_knowledge_count("monster")
            item_count = self.vector_service.get_knowledge_count("item")
            game_event_count = self.vector_service.get_knowledge_count("game_event")

            self.logger.info("📊 Database Summary:")
            self.logger.info(f"   Total entries: {total_count}")
            self.logger.info(f"   Monsters: {monster_count}")
            self.logger.info(f"   Items: {item_count}")
            self.logger.info(f"   Game Events: {game_event_count}")

            # Monster breakdown
            monster_types = {}
            for monster_data in SAMPLE_MONSTERS.values():
                monster_type = monster_data.get('type', 'unknown')
                monster_types[monster_type] = monster_types.get(monster_type, 0) + 1

            if monster_types:
                self.logger.info("🐉 Monster Types:")
                for mtype, count in monster_types.items():
                    self.logger.info(f"   {mtype.title()}: {count}")

            # Item breakdown
            item_types = {}
            for item_data in SAMPLE_ITEMS.values():
                item_type = item_data.get('type', 'unknown')
                item_types[item_type] = item_types.get(item_type, 0) + 1

            if item_types:
                self.logger.info("⚔️ Item Types:")
                for itype, count in item_types.items():
                    self.logger.info(f"   {itype.title()}: {count}")

        except Exception as e:
            self.logger.warning(f"⚠️ Failed to display summary: {e}")

    async def verify_data(self):
        """Verify that data was ingested correctly"""
        try:
            self.logger.info("🔍 Verifying ingested data...")

            # Test monster search
            monster_results = await self.vector_service.semantic_search(
                query="fire dragon powerful boss",
                content_type="monster",
                limit=3
            )

            # Test item search
            item_results = await self.vector_service.semantic_search(
                query="healing potion restore health",
                content_type="item",
                limit=3
            )

            self.logger.info(f"✅ Monster search returned {len(monster_results)} results")
            self.logger.info(f"✅ Item search returned {len(item_results)} results")

            if monster_results and item_results:
                self.logger.info("🎯 Data verification successful!")
                return True
            else:
                self.logger.warning("⚠️ Some searches returned no results")
                return False

        except Exception as e:
            self.logger.error(f"❌ Data verification failed: {e}")
            return False

    async def load_custom_data(self, data_file: str):
        """Load custom data from JSON file"""
        try:
            data_path = Path(data_file)
            if not data_path.exists():
                self.logger.warning(f"⚠️ Data file not found: {data_file}")
                return False

            self.logger.info(f"📥 Loading custom data from {data_file}")

            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            monsters = data.get('monsters', {})
            items = data.get('items', {})

            if not monsters and not items:
                self.logger.warning(f"⚠️ No monsters or items found in {data_file}")
                return False

            success = await self.vector_service.ingest_game_data(monsters, items)
            if success:
                self.logger.info(f"✅ Loaded custom data: {len(monsters)} monsters, {len(items)} items")
                return True
            else:
                self.logger.error(f"❌ Failed to load custom data from {data_file}")
                return False

        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Invalid JSON in {data_file}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error loading custom data: {e}")
            return False


async def main():
    """Main entry point for ChromaDB initialization"""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize ChromaDB for Dungeon Quest game")
    parser.add_argument("--force", "-f", action="store_true",
                       help="Force reset existing data without prompt")
    parser.add_argument("--verify", "-v", action="store_true",
                       help="Verify data after initialization")
    parser.add_argument("--custom-data", "-c", type=str,
                       help="Path to custom JSON data file")
    parser.add_argument("--skip-api-check", action="store_true",
                       help="Skip OpenAI API key check (for testing)")

    args = parser.parse_args()

    logger = setup_logger("init_chroma_db")
    logger.info("🎮 Dungeon Quest - ChromaDB Initialization")

    initializer = ChromaDBInitializer()

    try:
        # Initialize with sample data
        success = await initializer.initialize(force_reset=args.force, skip_api_check=args.skip_api_check)

        # Load custom data if provided
        if args.custom_data and success:
            custom_success = await initializer.load_custom_data(args.custom_data)
            if custom_success:
                await initializer.display_summary()

        # Verify data if requested
        if args.verify and success:
            verify_success = await initializer.verify_data()
            if not verify_success:
                logger.warning("⚠️ Data verification had issues")

        if success:
            logger.info("🎉 ChromaDB is ready for Dungeon Quest!")
            logger.info("🚀 You can now start the game server with: python main.py")
        else:
            logger.error("❌ Initialization failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("🛑 Initialization cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())