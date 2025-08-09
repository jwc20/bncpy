"""
https://github.com/faif/python-patterns/blob/master/patterns/behavioral/state.py
"""

from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

from bncpy import Board, Game, Player
from aifc import data


class GameMode(Enum):
    SINGLE_BOARD = 1
    MULTI_BOARD = 2
    
@dataclass
class GameConfig:
    code_length: int
    num_of_colors: int
    num_of_guesses: int
    
@dataclass
class GuessEntry:
    pass
@dataclass
class PlayerState:
    pass

@dataclass
class GameState:
    pass

