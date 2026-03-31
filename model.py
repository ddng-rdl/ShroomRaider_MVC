# model.py
from common_types import GameEvent, Tile


class ShroomRaiderModel:
    def __init__(self, grid: list[list[str]], r: int, c: int) -> None:
        self.original_grid = [row[:] for row in grid]
        self.initial_grid = [row[:] for row in grid]
        self.grid = grid
        self.rows = r
        self.cols = c

        self.laro_loc = self.find_laro(Tile.LARO.ascii)
        self.inventory = None
        self.total_mushrooms = sum(row.count(Tile.MUSHROOM.ascii) for row in grid)
        self.mushrooms_remaining = self.total_mushrooms
        self.mushrooms_collected = 0
        self.game_over = False
        self.win = False
        self.last_event = GameEvent.NONE

    def find_laro(self, char: str) -> list[int] | None:
        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if tile == char:
                    return [r, c]
        return None

    def get_tile(self, r: int, c: int) -> str | None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def set_tile(self, r: int, c: int, char: str) -> None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = char

    def move_laro(self, r: int, c: int) -> None:
        if self.game_over:
            return
        if self.laro_loc is None:
            self.last_event = GameEvent.NO_LARO
            return
        (laro_r, laro_c) = self.laro_loc
        (new_r, new_c) = (laro_r + r), (laro_c + c)
        self.interaction(self.get_tile(new_r, new_c), laro_r, laro_c, new_r, new_c)

    def interaction(
        self, target_tile: str | None, lr: int, lc: int, nr: int, nc: int
    ) -> None:
        match target_tile:
            case Tile.EMPTY.ascii | Tile.PAVED.ascii:
                self._execute_move(lr, lc, nr, nc)
            case Tile.MUSHROOM.ascii:
                self.mushrooms_collected += 1
                self.mushrooms_remaining -= 1
                self._execute_move(lr, lc, nr, nc)
                self.last_event = GameEvent.MUSHROOM_COLLECTED
                if self.mushrooms_collected == self.total_mushrooms:
                    self.win = True
                    self.game_over = True
            case Tile.WATER.ascii:
                self.last_event = GameEvent.DROWNED
                self.game_over = True
                self.set_tile(lr, lc, ".")
            case Tile.AXE.ascii | Tile.FLAMETHROWER.ascii:
                self._execute_move(lr, lc, nr, nc)
                self.last_event = GameEvent.ITEM_FOUND
            case Tile.TREE.ascii:
                if self.inventory is not None:
                    self.after_item_tree_interaction(lr, lc, nr, nc)
                else:
                    self.last_event = GameEvent.TREE_BLOCKED
            case Tile.ROCK.ascii:
                rock_row = nr + (nr - lr)
                rock_column = nc + (nc - lc)
                next_rock_tile = self.get_tile(rock_row, rock_column)
                rock_tile_positions = (rock_row, rock_column, nr, nc, lr, lc)
                self.after_rock_push(next_rock_tile, rock_tile_positions)
            case _:
                self.last_event = GameEvent.OUT_OF_BOUNDS
                return

    def _execute_move(self, lr: int, lc: int, nr: int, nc: int) -> None:
        self.set_tile(nr, nc, Tile.LARO.ascii)
        original_tile = self.get_original_tile(lr, lc)
        self.set_tile(
            lr,
            lc,
            Tile.EMPTY.ascii
            if original_tile
            not in {Tile.AXE.ascii, Tile.FLAMETHROWER.ascii, Tile.PAVED.ascii}
            else original_tile,
        )
        self.laro_loc = [nr, nc]
        self.last_event = GameEvent.NONE

    def get_original_tile(self, r: int, c: int) -> str:
        return self.initial_grid[r][c]

    def pickup_item(self) -> None:
        if self.laro_loc is None:
            self.last_event = GameEvent.NO_LARO
            return
        (x, y) = self.laro_loc
        tile_item = self.get_original_tile(x, y)
        if tile_item in {Tile.AXE.ascii, Tile.FLAMETHROWER.ascii}:
            if self.inventory is None:
                self.inventory = tile_item
                self.initial_grid[x][y] = Tile.EMPTY.ascii
                if tile_item == Tile.AXE.ascii:
                    self.last_event = GameEvent.PICKED_AXE
                if tile_item == Tile.FLAMETHROWER.ascii:
                    self.last_event = GameEvent.PICKED_FLAMETHROWER
            else:
                self.last_event = GameEvent.ALREADY_HOLDING
        else:
            self.last_event = GameEvent.NOTHING_TO_PICKUP

    def reset_stage(self) -> None:
        self.grid = [row[:] for row in self.original_grid]
        self.initial_grid = [row[:] for row in self.original_grid]
        self.laro_loc = self.find_laro(Tile.LARO.ascii)
        self.inventory = None
        self.mushrooms_remaining = self.total_mushrooms
        self.mushrooms_collected = 0
        self.game_over = False
        self.win = False
        self.last_event = GameEvent.STAGE_RESET

    def after_rock_push(
        self, next_rock_tile: str | None, rock_tile_positions: tuple[int, ...]
    ) -> None:
        (rock_row, rock_column, nr, nc, lr, lc) = rock_tile_positions
        match next_rock_tile:
            case None:
                self.last_event = GameEvent.ROCK_OUT_OF_BOUNDS
                return
            case Tile.ROCK.ascii:
                self.last_event = GameEvent.ROCK_BLOCKED
            case Tile.WATER.ascii:
                self.set_tile(rock_row, rock_column, Tile.PAVED.ascii)
                self.initial_grid[rock_row][rock_column] = Tile.PAVED.ascii
                self._execute_move(lr, lc, nr, nc)
                self.last_event = GameEvent.WATER_PAVED
            case Tile.EMPTY.ascii | Tile.PAVED.ascii:
                self.set_tile(rock_row, rock_column, Tile.ROCK.ascii)
                self._execute_move(lr, lc, nr, nc)
                self.last_event = GameEvent.ROCK_PUSHED
            case _:
                self.last_event = GameEvent.INVALID_ROCK_PUSH

    def burn_trees(self, nr: int, nc: int) -> None:
        to_be_checked = [(nr, nc)]
        trees = [(nr, nc)]
        while to_be_checked != []:
            for tree in to_be_checked.copy():
                (tr, tc) = tree
                adjs = [
                    (tr + x_adj, tc + y_adj)
                    for x_adj, y_adj in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                ]
                for adj in adjs:
                    if (
                        adj[0] in range(self.rows)
                        and adj[1] in range(self.cols)
                        and self.initial_grid[adj[0]][adj[1]] == Tile.TREE.ascii
                    ):
                        self.initial_grid[adj[0]][adj[1]] = Tile.EMPTY.ascii
                        to_be_checked.append(adj)
                        trees.append(adj)
                to_be_checked.remove(tree)
        for tree in trees:
            (tr, tc) = tree
            self.set_tile(tr, tc, Tile.EMPTY.ascii)

    def after_item_tree_interaction(self, lr: int, lc: int, nr: int, nc: int) -> None:
        if self.inventory == Tile.AXE.ascii:
            self._execute_move(lr, lc, nr, nc)
            self.inventory = None
            self.last_event = GameEvent.TREE_CHOPPED
        elif self.inventory == Tile.FLAMETHROWER.ascii:
            self.burn_trees(nr, nc)
            self._execute_move(lr, lc, nr, nc)
            self.inventory = None
            self.last_event = GameEvent.TREE_BURNED
