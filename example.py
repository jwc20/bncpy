from bnc import Board, Game, Player

if __name__ == "__main__":
    board = Board()
    print(board.display_board())

    players = [
        Player("Jae", board.copy()),
        Player("Soo", board.copy()),
    ]

    # print(players[1].board.display_board())

    game = Game(players, secret_code="1234")

    players[0].make_guess("1234")
    print(players[0].board.display_board())
