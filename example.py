from bnc import Board, Game, Player

if __name__ == "__main__":
    board = Board()
    players = [
        Player("Jae", board.copy()),
        Player("Soo", board.copy()),
    ]
    game = Game(players, secret_code="1234")

    players[0].make_guess("1234")

    print(players[0].board.display_board())
    # print(players[0].board.secret_code)
    # print(players[1].board.secret_code)
    print(players[1].board.display_board())
