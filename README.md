# 🏰 Dungeon Quest

An AI-driven text adventure game featuring RAG (Retrieval-Augmented Generation) system that creates immersive dungeon exploration experiences. Players input actions and the system generates dynamic storylines with context-aware responses using semantic search and LLM generation.

## ✨ Features

- **🤖 RAG-Powered AI System**: Intelligent context retrieval with ChromaDB vector search
- **📖 Dynamic Storytelling**: AI-generated narratives that adapt to player actions and game history
- **🧠 Semantic Memory**: Vector database stores and retrieves relevant game events
- **⚔️ Rich Game Content**: 25+ pre-loaded monsters and items with detailed descriptions
- **🌍 Multi-Language Support**: English and Traditional Chinese localization
- **🎮 Game State Management**: HP, inventory, experience, and combat mechanics with 10-turn progression
- **🌐 Web Interface**: Browser-based game client with real-time interactions
- **📋 REST API**: Full game API with automatic FastAPI documentation

## 🏗️ Architecture

The game uses a streamlined RAG-based architecture:

- **🎯 GameService**: Unified game logic with RAG integration for context-aware responses
- **🗄️ VectorService**: ChromaDB-powered semantic search for game events, monsters, and items
- **🧠 LLMService**: OpenAI GPT integration with fallback mechanisms
- **📊 GameController**: Game state orchestration and player action processing
- **🌐 Localization**: Centralized multi-language message management

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **OpenAI API Key** (required for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dungeon-quest
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Initialize ChromaDB with game data** ⭐
   ```bash
   # Initialize with sample monsters and items
   python src/scripts/init_chroma_db.py --force

   # Verify the data was loaded correctly
   python src/scripts/init_chroma_db.py --verify
   ```

5. **Run the game server**
   ```bash
   python main.py
   ```

### 🎯 Access Points

- **🎮 Game Interface**: http://localhost:8000/static/index.html
- **📋 API Documentation**: http://localhost:8000/docs
- **🔧 API Base**: http://localhost:8000

### 🏃‍♂️ Quick Test

```bash
# Create a new game
curl -X POST "http://localhost:8000/game/new?player_name=Hero"

# Process an action (replace game_id with the actual ID)
curl -X POST "http://localhost:8000/game/action" \
  -H "Content-Type: application/json" \
  -d '{"game_id":"<game_id>","action":"explore the dungeon"}'
```

## 🎮 How to Play

1. **Open the game interface**
   ```
   http://localhost:8000/static/index.html
   ```

2. **Create a new game** by entering your player name

3. **Type actions** to explore the dungeon:
   - `"explore the dungeon"` - Move deeper into the caves
   - `"attack the monster"` - Engage in combat
   - `"check inventory"` - View your items
   - `"rest"` - Recover health
   - `"look around"` - Examine your surroundings
   - `"talk to the NPC"` - Interact with characters

4. **Game progresses for 10 turns** with escalating challenges:
   - **Turns 1-3**: Basic monsters and exploration
   - **Turns 4-6**: Stronger enemies and better loot
   - **Turns 7-9**: Elite monsters and boss encounters
   - **Turn 10**: Epic finale

## 📁 Project Structure

```
dungeon-quest/
├── main.py                          # FastAPI application entry point
├── src/
│   ├── game_controller.py          # Game orchestration and state management
│   ├── services/                   # Core business logic
│   │   ├── game_service.py         # Main game logic with RAG integration
│   │   ├── llm_service.py          # OpenAI client management
│   │   └── vector_service.py       # ChromaDB vector operations
│   ├── models/                     # Data models and schemas
│   │   ├── game_state.py           # Game state, player, and API models
│   │   └── chroma/                 # ChromaDB model implementations
│   │       ├── database_model.py   # ChromaDB connection and collection management
│   │       ├── embedding_model.py  # OpenAI embedding generation
│   │       ├── search_model.py     # Vector search operations
│   │       └── knowledge_model.py  # Data storage and retrieval
│   ├── localization/              # Multi-language support
│   │   ├── __init__.py             # Centralized message management
│   │   ├── en.py                   # English text and fallback events
│   │   └── zh_tw.py                # Traditional Chinese text
│   ├── utils/                     # Utility functions
│   │   └── logger.py               # Logging configuration
│   └── scripts/                   # Setup and maintenance scripts
│       └── init_chroma_db.py       # ChromaDB initialization with sample data
├── static/                        # Web interface
│   └── index.html                 # Game client interface
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (create this)
└── chroma_db/                    # ChromaDB persistence (auto-created)
```

## 🛠️ Tech Stack

- **🚀 FastAPI**: High-performance REST API with automatic documentation
- **🔍 ChromaDB**: Local vector database for semantic search
- **🤖 OpenAI**: GPT models and text embeddings (gpt-5-nano, text-embedding-3-small)
- **📋 Pydantic**: Data validation and serialization
- **🌍 python-dotenv**: Environment variable management
- **📊 LangChain**: Ready for advanced agent orchestration

## 🗄️ Data Initialization

The `init_chroma_db.py` script sets up your game world with rich content:

### 📋 Available Commands

```bash
# Basic initialization (with prompt if data exists)
python src/scripts/init_chroma_db.py

# Force reset and reload all data
python src/scripts/init_chroma_db.py --force

# Verify data integrity after setup
python src/scripts/init_chroma_db.py --verify

# Load custom data from JSON file
python src/scripts/init_chroma_db.py --custom-data my_data.json

# Get help and see all options
python src/scripts/init_chroma_db.py --help
```

### 🎲 Included Game Content

**🐉 Monsters (10 total)**:
- **Boss Level**: Fire Dragon, Ice Queen
- **Elite Level**: Shadow Wolf, Stone Golem, Lightning Eagle
- **Common Level**: Goblin Warrior, Skeleton Warrior, Cave Spider, Orc Brute, Fire Imp

**⚔️ Items (15 total)**:
- **Consumables**: Healing/Mana Potions, Strength Elixir, Phoenix Feather
- **Weapons**: Rusty Sword, Flaming Sword, Ice Staff, Dragon Slayer
- **Armor**: Leather Armor, Shadow Cloak, Steel Plate Mail, Dragon Scale Armor
- **Accessories**: Ring of Power, Amulet of Health, Boots of Speed

### 📊 Data Verification

After initialization, you should see:
```
📊 Database Summary:
   Total entries: 25
   Monsters: 10
   Items: 15
   Game Events: 0 (grows as players play)
```

## 🔧 Development & Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   ```bash
   # Make sure .env file exists with your API key
   echo "OPENAI_API_KEY=your_actual_api_key" > .env
   ```

2. **"ChromaDB dimension mismatch"**
   ```bash
   # Reset the database completely
   python src/scripts/init_chroma_db.py --force
   ```

3. **"No module named 'dotenv'"**
   ```bash
   # Install missing dependency
   pip install python-dotenv
   ```

### Performance Tips

- **Game responds in ~30 seconds** due to AI processing
- **RAG search** finds relevant context from previous game events
- **Memory optimization** keeps recent events in RAM for faster access
- **Vector search** works better with more game history

## 🌍 Multi-Language Support

The game supports both English and Traditional Chinese:

- Language is automatically detected from game creation
- All system messages and fallback events are localized
- AI responses adapt to the selected language
- Centralized message management in `src/localization/`