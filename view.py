# view.py
from common_types import UI, GameEvent


class ShroomRaiderView:
    def __init__(self):
        self.ui_map = UI
        self.event_messages = {
            GameEvent.NONE: "",
            GameEvent.OUT_OF_BOUNDS: "You can't go outside.",
            GameEvent.DROWNED: "Laro drowned!",
            GameEvent.ITEM_FOUND: "There is an item on the ground! Will you pick it up?",
            GameEvent.TREE_BLOCKED: "A tree blocks your path. You need an axe or flamethrower.",
            GameEvent.ROCK_OUT_OF_BOUNDS: "You can't push a rock outside.",
            GameEvent.ROCK_BLOCKED: "You can't push a rock into another rock.",
            GameEvent.WATER_PAVED: "Woah, the water became a walkable tile!",
            GameEvent.ROCK_PUSHED: "Rock pushed.",
            GameEvent.INVALID_ROCK_PUSH: "You can't push a rock there.",
            GameEvent.TREE_CHOPPED: "Tree chopped.",
            GameEvent.TREE_BURNED: "Tree/s burned.",
            GameEvent.NO_LARO: "Laro is not placed on the map.",
            GameEvent.PICKED_AXE: "You picked up an Axe(🪓)!",
            GameEvent.PICKED_FLAMETHROWER: "You picked up a Flamethrower(🔥)!",
            GameEvent.ALREADY_HOLDING: "You are already holding an item.",
            GameEvent.NOTHING_TO_PICKUP: "You have nothing to pick up here.",
            GameEvent.STAGE_RESET: "Stage has been reset.",
        }

    def clear_terminal(self) -> None:
        print("\033[H\033[J", end="")

    def render_map(self, grid: list[list[str]], rows: int, cols: int) -> None:
        map_list: list[str] = []
        for r in range(rows):
            row_emojis = [self.ui_map[grid[r][c]] for c in range(cols)]
            map_list.append("".join(row_emojis))
        print("\n".join(map_list))

    def display(
        self,
        grid: list[list[str]],
        rows: int,
        cols: int,
        collected: int,
        total: int,
        inventory: str | None,
        tile_item: str | None,
        last_event: GameEvent,
    ) -> None:

        self.clear_terminal()
        print("--- 🍄 SHROOM RAIDER 🍄 ---")
        self.render_map(grid, rows, cols)

        print(f"\nMushrooms Collected: {collected}")
        print(f"Mushrooms Remaining: {total - collected}")

        inventory_text = "Nothing"
        if inventory == "x":
            inventory_text = "🪓 Axe"
        elif inventory == "*":
            inventory_text = "🔥 Flamethrower"

        item_text = "Nothing"
        if tile_item == "x":
            item_text = "🪓 Axe"
        elif tile_item == "*":
            item_text = "🔥 Flamethrower"

        print(f"Currently Holding: {inventory_text}")
        print(f"Item on current tile: {item_text}")

        message = self.event_messages.get(last_event, "")
        if last_event == GameEvent.MUSHROOM_COLLECTED:
            message = f"You collected a mushroom! ({collected}/{total})"

        print(f"\nGame Message: {message}\n")
        print("""CONTROLS:
    [W] Move Up         [P] Pick Up Item
    [A] Move Left       [!] Reset
    [S] Move Down
    [D] Move Right""")

    def get_player_input(self) -> str:
        return input("\nInput your next move: ").strip().upper()

    def display_win(self) -> None:
        print("\nYou win! Congratulations for collecting all mushrooms!\n")

    def prompt_leaderboard_name(self) -> str:
        name = input("Enter your name for the leaderboard: ").strip()
        while not name or name.isspace():
            print("❌ Name cannot be empty!")
            name = input("Enter your name for the leaderboard: ").strip()
        return name

    def display_loss(self) -> None:
        print("You lost. Laro drowned...\n")
