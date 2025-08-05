from bnc import Board, Game, Player

if __name__ == "__main__":
    board = Board()
    print(board.display_board())

    players = [
        Player("Jae", board),
        Player("Soo", board),
    ]

    print(players[0].board.display_board())
    print(players[1].board.display_board())
    #
    # game = Game(players, code="1234")
