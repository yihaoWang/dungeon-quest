from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.models.game_state import PlayerAction, GameResponse, Language
from src.game_controller import GameController

# Load environment variables
load_dotenv()

app = FastAPI(title="Dungeon Quest API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_controller = GameController()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to Dungeon Quest API"}


@app.post("/game/new")
async def create_game(player_name: str = "Adventurer", language: Language = Language.ZH_TW):
    game_id = game_controller.create_new_game(player_name, language)

    # Get initial game state
    initial_response = await game_controller.process_action(game_id, "start")
    return initial_response


@app.post("/game/action", response_model=GameResponse)
async def perform_action(action_data: PlayerAction):
    response = await game_controller.process_action(
        action_data.game_id,
        action_data.action
    )

    if not response:
        raise HTTPException(status_code=404, detail="Game not found or inactive")

    return response


@app.get("/game/{game_id}/status")
async def get_game_status(game_id: str):
    game_state = game_controller.get_game(game_id)
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not found")

    return {
        "game_id": game_id,
        "player": game_state.player,
        "status": game_state.status,
        "turn_count": game_state.turn_count,
        "current_scene": game_state.current_scene,
        "language": game_state.language
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)