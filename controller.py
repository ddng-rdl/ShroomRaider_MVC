# controller.py
from model import ShroomRaiderModel
from view import ShroomRaiderView


class ShroomRaiderController:
    def __init__(self, model: ShroomRaiderModel, view: ShroomRaiderView):
        self.model = model
        self.view = view
        self.move_count = 0

    def process_move(self, move: str) -> None:
        if self.model.game_over:
            return
        match move:
            case "W":
                self.model.move_laro(-1, 0)
            case "A":
                self.model.move_laro(0, -1)
            case "S":
                self.model.move_laro(1, 0)
            case "D":
                self.model.move_laro(0, 1)
            case "P":
                self.model.pickup_item()
            case "!":
                self.model.reset_stage()
            case _:
                pass

    def update_view(self) -> None:
        tile_item = None
        if self.model.laro_loc is not None:
            r, c = self.model.laro_loc
            tile_item = self.model.get_original_tile(r, c)

        self.view.display(
            grid=self.model.grid,
            rows=self.model.rows,
            cols=self.model.cols,
            collected=self.model.mushrooms_collected,
            total=self.model.total_mushrooms,
            inventory=self.model.inventory,
            tile_item=tile_item,
            last_event=self.model.last_event,
        )

    def run_interactive(self) -> None:
        while not self.model.game_over:
            self.update_view()
            initial_moveset = self.view.get_player_input()

            moveset = initial_moveset
            for initial_move in initial_moveset:
                valid_moves = "WASDPQ!"
                self.move_count += 1
                if initial_move not in valid_moves:
                    moveset = moveset[1 : moveset.index(initial_move)]
                    break

            for move in moveset:
                if self.model.game_over:
                    break
                self.process_move(move)

        self.update_view()

        if self.model.game_over and not self.model.win:
            self.view.display_loss()

    def run_automated(self, moves: str) -> None:
        for move in moves.strip().upper():
            if self.model.game_over:
                break
            self.process_move(move)
