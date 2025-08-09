"""
https://github.com/faif/python-patterns/blob/master/patterns/behavioral/state.py
"""

from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

from bncpy import Board, Game, Player
from bncpy.utils import generate_guess, get_random_number

from aifc import data


class GameMode(Enum):
    SINGLE_BOARD = 1
    MULTI_BOARD = 2
    
    
    
# class GameConfigStrategyValidator:
#     @staticmethod
#     def validate(game_config: GameConfig):
#         if game_config.code_length < 3:
#             raise ValueError(f"code_length must be at least 3, got {game_config.code_length}")
#         if game_config.num_of_colors < 5:
#             raise ValueError(f"num_of_colors must be at least 5, got {game_config.num_of_colors}")
#         if game_config.num_of_guesses < 1:
#             raise ValueError(f"num_of_guesses must be at least 1, got {game_config.num_of_guesses}")
    
@dataclass
class GameConfig:
    code_length: int = 4
    num_of_colors: int = 6
    num_of_guesses: int = 10
    secret_code: str | None = None
    
    def validate(self) -> None:
        if self.code_length < 3:
            raise ValueError(f"code_length must be at least 3, got {self.code_length}")
        if self.num_of_colors < 5:
            raise ValueError(f"num_of_colors must be at least 5, got {self.num_of_colors}")
        if self.num_of_guesses < 1:
            raise ValueError(f"num_of_guesses must be at least 1, got {self.num_of_guesses}")
        
    def generate_secret_code(self) -> str:
        return get_random_number(self.num_of_colors, self.code_length)
        


    
@dataclass
class GuessEntry:
    pass
@dataclass
class PlayerState:
    pass


class GameState:
    game_config_strategy = GameConfigStrategyValidator()
    
    def __init__(self, game_config: GameConfig) -> None:
        self.game_config_strategy.validate(game_config)
        self._game_config = game_config



if __name__ == "__main__":
    game_config = GameConfig()
    game_state = GameState() 
    
    board = Board()
    player = Player()
    game = Game()