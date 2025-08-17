<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="cow.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# BNCPY

<em>Unleashing Collaborative Code-Breaking Fun for Everyone</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/jwc20/bncpy?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/jwc20/bncpy?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/jwc20/bncpy?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/jwc20/bncpy?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->

Benjamin and Charlotte python library

Demo: https://bnc-client-psi.vercel.app

Docs: https://jwc20.github.io/bnc-docs/

Mono-repo: https://github.com/jwc20/bnc-game

BE: https://github.com/jwc20/bncapi

FE: https://github.com/jwc20/bnc-client


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Project Structure](#project-structure)
  - [Project Index](#project-index)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)

---

## Overview

bncpy is a robust Python-based game development tool that simplifies the process of creating a code-breaking game.

This project streamlines the game development process, providing a comprehensive suite of features for building a Bulls and Cows game. The core features include:

- **Game Logic Management:** Handles the setup, progress, and conclusion of the game, ensuring a smooth gaming experience.
- **Game State Management:** Manages game state, player state, and game configuration, maintaining the integrity of the game.

---

## Project Structure

```sh
└── bncpy/
    ├── .github
    │   └── workflows
    ├── LICENSE
    ├── README.md
    ├── bnc
    │   ├── __init__.py
    │   ├── board.py
    │   ├── game.py
    │   ├── player.py
    │   ├── state.py
    │   └── utils.py
    ├── example.py
    ├── pyproject.toml
    ├── requirements.txt
    ├── tests
    │   ├── __init__.py
    │   ├── test_board.py
    │   ├── test_game.py
    │   ├── test_integration.py
    │   ├── test_player.py
    │   ├── test_state.py
    │   └── test_utils.py
    └── uv.lock
```

### Project Index

<details open>
	<summary><b><code>BNCPY/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/LICENSE'>LICENSE</a></b></td>
					<td style='padding: 8px;'>- The LICENSE file provides the legal framework for the project, granting users the freedom to use, modify, and distribute the software under the terms of the MIT License<br>- It disclaims warranties and limits liability, ensuring Jae W<br>- Chois rights are protected while encouraging open collaboration and sharing.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- Requirements.txt serves as a manifest for the projects Python dependencies, generated automatically by uv from pyproject.toml<br>- It lists libraries like anyio, certifi, httpx, and others, indicating their versions and interdependencies<br>- This file is crucial for ensuring consistent environment setup across different development and deployment scenarios.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/pyproject.toml'>pyproject.toml</a></b></td>
					<td style='padding: 8px;'>- The pyproject.toml file serves as the configuration blueprint for the bncpy project, a game developed by Jae W<br>- Choi<br>- It outlines the build system, project details, dependencies, and formatting rules<br>- The project requires Python 3.12 or higher and uses tools like setuptools and wheel for building and packaging<br>- It also specifies coding style guidelines using the ruff tool.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/example.py'>example.py</a></b></td>
					<td style='padding: 8px;'>- Example.py demonstrates the functionality of a collaborative and competitive game mode in a code-breaking game<br>- It showcases the process of setting up the game, adding players, submitting guesses, and tracking game status<br>- The script also tests JSON serialization and deserialization of the game state.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- bnc Submodule -->
	<details>
		<summary><b>bnc</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ bnc</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/bnc/board.py'>board.py</a></b></td>
					<td style='padding: 8px;'>- Board.py manages the game board for a Bulls and Cows game, handling the initialization and validation of game parameters such as code length, number of colors, and number of guesses<br>- It also manages the game state, including tracking guesses, evaluating the correctness of guesses, and determining game outcomes.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/bnc/game.py'>game.py</a></b></td>
					<td style='padding: 8px;'>- Game.py manages the game logic for a board game involving multiple players<br>- It handles the setup, progress, and conclusion of the game, including player actions such as submitting guesses and setting secret codes<br>- The module ensures consistency across player boards and determines the games winner(s).</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/bnc/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>- Bnc/utils.py` serves as a utility module in the codebase, providing essential functions for validating user input, generating random guesses, calculating game scores, and fetching random numbers<br>- It ensures the integrity of the game logic and enhances the overall functionality of the application.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/bnc/player.py'>player.py</a></b></td>
					<td style='padding: 8px;'>- Player, located at bnc/player.py, represents a participant in the game, maintaining their name and game board<br>- It provides methods to set a secret code, make a guess, and check the game status<br>- It interacts with the Board class to evaluate guesses and determine game outcomes.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/bnc/state.py'>state.py</a></b></td>
					<td style='padding: 8px;'>- The <code>state.py</code> module in the Bulls and Cows game codebase manages the game state, player state, and game configuration<br>- It handles player actions such as submitting guesses, adding or removing players, and resetting the game<br>- It also validates game configurations and maintains the games state, including tracking winners and remaining guesses.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- .github Submodule -->
	<details>
		<summary><b>.github</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ .github</b></code>
			<!-- workflows Submodule -->
			<details>
				<summary><b>workflows</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ .github.workflows</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/jwc20/bncpy/blob/master/.github/workflows/publish.yml'>publish.yml</a></b></td>
							<td style='padding: 8px;'>- Publishing Python Package to PyPI automates the process of packaging and uploading Python projects to the Python Package Index<br>- It triggers on a new release, sets up Python, installs dependencies, builds the package, stores the distribution, and uploads it to PyPI using GitHub Actions.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip, Uv

### Installation

Build bncpy from the source and intsall dependencies:

1. **Clone the repository:**

```sh
git clone https://github.com/jwc20/bncpy
```

2. **Navigate to the project directory:**

```sh
cd bncpy
```

3. **Install the dependencies:**

<!-- SHIELDS BADGE CURRENTLY DISABLED -->

```sh
pip install -r requirements.txt
```

<!-- SHIELDS BADGE CURRENTLY DISABLED -->

```sh
uv sync --all-extras --dev
```

Alternatively, you can pip install:

```bash
# Install package from PyPi
pip install bncpy
```

### Usage

```python
from bnc import Board, Game, Player
from bnc.utils import generate_guess, get_random_number

# Game configuration
config = {
  "code_length": 4,
  "num_of_colors": 6,
  "num_of_guesses": 10
}

# Create players with boards
players = [
  Player(name="Jae", board=Board(**config)),
  Player(name="Soo", board=Board(**config)),
  Player(name="Benjamin", board=Board(**config)),
  Player(name="Charlotte", board=Board(**config))
]

# Create game with secret code
secret_code = get_random_number(length=4, max_value=5)  # Random 4-digit code
game = Game(players, secret_code=secret_code)

# Submit guesses
game.submit_guess(players[0], "1234")
game.submit_guess(players[1], generate_guess(config["code_length"], config["num_of_colors"]))  # Random guess

# Check game state
print(game.state)
players[0].board.display_board()

# Check winners
if game.winners:
  for winner in game.winners:
    print(f"Winner: {winner.name}")
```

### Setting the secret code

- **Multiple ways to set secret codes:**
  - Via Game initialization: `Game(players, secret_code="1234")`
  - Per player: `player.set_secret_code_to_board("1234")`
  - Random generation: `game.set_random_secret_code()`

### Testing

Bncpy uses the **pytest** test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
pytest
```

**Using [uv](https://docs.astral.sh/uv/):**

```sh
uv run pytest tests/
```

### Dependencies

- [httpx](https://github.com/encode/httpx)
- [jsonpickle](https://github.com/jsonpickle/jsonpickle)

