from testing_course.connect_four.player import Player

from testing_course.connect_four.connect_four import InvalidMoveError


class ConnectFourGame:
    def __init__(self, player_on_turn: Player) -> None:
        self.feld=[]
        
        for row in range(0,6):
            self.feld.append([Player.NONE,Player.NONE,Player.NONE,Player.NONE,
                              Player.NONE,Player.NONE,Player.NONE])
                
        self._player_on_turn = player_on_turn

    def __str__(self) -> str:
        header = "  1 2 3 4 5 6 7"
        rows = []

        for row in self.feld:
            rendered_row = []
            for cell in row:
                if cell == Player.RED:
                    rendered_row.append("R")
                elif cell == Player.YELLOW:
                    rendered_row.append("Y")
                else:
                    rendered_row.append(".")
            rows.append("  " + " ".join(rendered_row))

        return header + "\n" + "\n".join(rows)
        
        

    def get_player_at(self, row: int, col: int) -> Player:
        return self.feld[row][col]

    @property
    def player_on_turn(self) -> Player:
        return self._player_on_turn

    @property
    def is_game_over(self) -> bool:
        if self.winner != Player.NONE:
            return True
        return False

    @property
    def winner(self) -> Player:
        for player in (Player.RED, Player.YELLOW):
            for row in range(6):
                for col in range(7):
                    if self.feld[row][col] != player:
                        continue

                    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                    for d_row, d_col in directions:
                        count = 1
                        for step in range(1, 4):
                            next_row = row + d_row * step
                            next_col = col + d_col * step

                            if not (0 <= next_row < 6 and 0 <= next_col < 7):
                                break
                            if self.feld[next_row][next_col] == player:
                                count += 1
                            else:
                                break

                        if count >= 4:
                            return player

        return Player.NONE

    def reset(self, player_on_turn: Player) -> None:
        self.feld=[]
        
        for row in range(0,6):
            self.feld.append([Player.NONE,Player.NONE,Player.NONE,Player.NONE,
                              Player.NONE,Player.NONE,Player.NONE])
                
        self._player_on_turn = player_on_turn

    def drop(self, col: int) -> None:
        if col < 0 or col >= 7:
            raise InvalidMoveError("outside the playfield")

        if all(self.feld[row][col] != Player.NONE for row in range(6)):
            raise InvalidMoveError("column is full")

        for row in range(0, 6):
            if self.feld[row][col] == Player.NONE:
                self.feld[row][col] = self.player_on_turn

                if self.player_on_turn == Player.RED:
                    self._player_on_turn = Player.YELLOW
                elif self.player_on_turn == Player.YELLOW:
                    self._player_on_turn = Player.RED

                return
        
                
