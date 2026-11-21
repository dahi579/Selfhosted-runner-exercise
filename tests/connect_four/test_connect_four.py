# 100% Test coverage needed
# uv run connect-four

# --- Setup and initialization tests ---
import pytest

from testing_course.connect_four.connect_four import InvalidMoveError
from testing_course.connect_four.connect_four_game import ConnectFourGame
from testing_course.connect_four.player import Player


def test_player_starts_on_red_turn() -> None:
    game = ConnectFourGame(Player.RED)

    assert game.player_on_turn == Player.RED


def test_board_has_expected_size() -> None:
    game = ConnectFourGame(Player.RED)

    assert len(game.feld) == 6
    for row in game.feld:
        assert len(row) == 7


def test_empty_board_contains_only_none_cells() -> None:
    game = ConnectFourGame(Player.RED)

    assert sum(
        cell == Player.NONE for row in game.feld for cell in row
    ) == 42


def test_reset_clears_board_and_sets_player_turn() -> None:
    game = ConnectFourGame(Player.RED)
    game.feld[0][0] = Player.RED
    game.feld[1][1] = Player.YELLOW
    game._player_on_turn = Player.YELLOW

    game.reset(Player.RED)

    assert game.player_on_turn == Player.RED
    for row in game.feld:
        for cell in row:
            assert cell == Player.NONE


# --- Move and validation tests ---
def test_drop_outside_field_raises_invalid_move_error() -> None:
    game = ConnectFourGame(Player.RED)

    with pytest.raises(InvalidMoveError, match="outside the playfield"):
        game.drop(-1)

    with pytest.raises(InvalidMoveError, match="outside the playfield"):
        game.drop(7)


def test_drop_full_column_raises_invalid_move_error() -> None:
    game = ConnectFourGame(Player.RED)

    for _ in range(6):
        game.drop(0)

    with pytest.raises(InvalidMoveError, match="column is full"):
        game.drop(0)


def test_drop_places_disc_in_first_free_row() -> None:
    game = ConnectFourGame(Player.RED)

    game.drop(1)

    assert game.get_player_at(0, 1) == Player.RED
    assert game.get_player_at(1, 1) == Player.NONE


def test_drop_stacks_disc_in_same_column() -> None:
    game = ConnectFourGame(Player.RED)

    game.drop(2)
    game.drop(2)

    assert game.get_player_at(0, 2) == Player.RED
    assert game.get_player_at(1, 2) != Player.NONE
    assert game.get_player_at(2, 2) == Player.NONE


def test_drop_switches_turn_after_each_move() -> None:
    game = ConnectFourGame(Player.RED)

    game.drop(2)
    game.drop(2)
    game.drop(2)

    assert game.get_player_at(0, 2) == Player.RED
    assert game.get_player_at(1, 2) == Player.YELLOW
    assert game.get_player_at(2, 2) == Player.RED
    assert game.get_player_at(3, 2) == Player.NONE


# --- Winner and game-over tests ---
def test_winner_detects_horizontal_connect_four() -> None:
    game = ConnectFourGame(Player.RED)

    for col in range(4):
        game.feld[5][col] = Player.RED

    assert game.winner == Player.RED


def test_winner_detects_vertical_connect_four() -> None:
    game = ConnectFourGame(Player.YELLOW)

    for row in range(4):
        game.feld[row][3] = Player.YELLOW

    assert game.winner == Player.YELLOW


def test_winner_returns_none_without_four_in_a_row() -> None:
    game = ConnectFourGame(Player.RED)

    game.feld[5][0] = Player.RED
    game.feld[5][1] = Player.RED
    game.feld[5][2] = Player.RED
    game.feld[5][3] = Player.YELLOW

    assert game.winner == Player.NONE
    assert game.is_game_over is False


def test_is_game_over_is_true_when_a_player_has_won() -> None:
    game = ConnectFourGame(Player.RED)

    for col in range(4):
        game.feld[5][col] = Player.RED

    assert game.is_game_over is True
    assert game.winner == Player.RED


# --- String representation and CLI tests ---
import runpy
import sys

from testing_course.connect_four.__main__ import main


def test_game_string_representation_displays_board() -> None:
    game = ConnectFourGame(Player.RED)
    game.feld[5][0] = Player.RED
    game.feld[5][1] = Player.YELLOW

    board_text = str(game)

    assert "object at" not in board_text
    assert "R" in board_text
    assert "Y" in board_text
    assert all(str(number) in board_text for number in range(1, 8))


def test_main_handles_help_and_quit(monkeypatch, capsys) -> None:
    responses = iter(["h", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "Available commands:" in output
    assert "Ok, bye." in output


def test_main_handles_unknown_command_and_reset(monkeypatch, capsys) -> None:
    responses = iter(["x", "r", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "Unknown command" in output
    assert "Ok, bye." in output


def test_main_returns_on_eof(monkeypatch, capsys) -> None:
    def raise_eof(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)

    main()

    output = capsys.readouterr().out
    assert output.startswith("  1 2 3 4 5 6 7")


def test_main_ends_on_winning_move_and_script_execution(monkeypatch, capsys) -> None:
    responses = iter(["1", "2", "1", "2", "1", "2", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    main()

    output = capsys.readouterr().out
    assert "GAME OVER - Winner: RED" in output

    sys.modules.pop("testing_course.connect_four.__main__", None)
    responses = iter(["2", "1", "2", "1", "2", "1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    runpy.run_module("testing_course.connect_four.__main__", run_name="__main__")

    script_output = capsys.readouterr().out
    assert "GAME OVER - Winner:" in script_output
