# main.py
import sys
from argparse import ArgumentParser
from model import ShroomRaiderModel
from view import ShroomRaiderView
from controller import ShroomRaiderController


def validate_laro_count(grid: list[list[str]], file_path: str) -> bool:
    laro_count = sum(1 for row in grid for char in row if char == "L")
    if laro_count > 1:
        print(
            f"Error: Stage file '{file_path}' is not formatted correctly. Multiple Laros in stage file"
        )
        return False
    if laro_count == 0:
        print(
            f"Error: Stage file '{file_path}' is not formatted correctly. No Laro in stage file"
        )
        return False
    return True


def load_file_data() -> tuple[list[list[str]], int, int, str | None, str | None] | None:
    parser = ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-m", "--moves")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    if args.file is None:
        grid_raw = [
            "TTTTTTTTT",
            "T...+...T",
            "T...~...T",
            "T...R.T.T",
            "T.T.LTT.T",
            "T.x...*.T",
            "T.......T",
            "T.......T",
            "TTTTTTTTT",
        ]
        grid = [list(grid_raw[i]) for i in range(9)]
        return grid, 9, 9, None, None

    try:
        with open(args.file, encoding="utf-8") as f:
            content = f.readlines()
            r, c = map(int, content[0].split())
            grid = [list(content[i][0:c]) for i in range(2, r + 2)]

            if not validate_laro_count(grid, args.file):
                return None

            moves = args.moves if args.moves and args.output else None
            output_file = args.output if args.moves and args.output else None
            return grid, r, c, moves, output_file
    except FileNotFoundError:
        print(f"Error: Stage file '{args.file}' not found.")
        return None
    except (ValueError, IndexError):
        print(f"Error: Stage file '{args.file}' is not formatted correctly.")
        return None


def main() -> None:
    file_data: tuple[list[list[str]], int, int, str | None, str | None] | None = (
        load_file_data()
    )

    if file_data is None:
        sys.exit(1)

    grid, r, c, moves, output_file = file_data

    model = ShroomRaiderModel(grid, r, c)
    view = ShroomRaiderView()
    controller = ShroomRaiderController(model, view)

    if moves is None:
        controller.run_interactive()
    else:
        controller.run_automated(moves)
        if output_file is not None:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("CLEAR\n" if model.win else "NO CLEAR\n")
                f.write("\n".join("".join(row) for row in model.grid))


if __name__ == "__main__":
    main()
