
import re

from flask import Flask, jsonify, render_template, request
from ships import place_ships

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/board", methods=["POST"])
def generate_board():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "A board configuration is required."}), 400

    width = data.get("width")
    height = data.get("height")
    if (
        isinstance(width, bool)
        or not isinstance(width, int)
        or isinstance(height, bool)
        or not isinstance(height, int)
        or not 1 <= width <= 30
        or not 1 <= height <= 30
    ):
        return jsonify({"error": "Board width and height must be between 1 and 30."}), 400

    ship_data = data.get("ships")
    if not isinstance(ship_data, list):
        return jsonify({"error": "Ships must be provided as a list."}), 400

    ground_ships = {}
    air_ships = {}
    colors = {}
    ship_names = set()
    for ship in ship_data:
        if not isinstance(ship, dict):
            return jsonify({"error": "Each ship must have a name, size, and color."}), 400

        name = ship.get("name")
        size = ship.get("size")
        shape = ship.get("shape")
        color = ship.get("color")
        hover = ship.get("hover", False)
        if not isinstance(name, str) or not name.strip() or len(name.strip()) > 40:
            return jsonify({"error": "Ship names must contain 1 to 40 characters."}), 400
        name = name.strip()
        if name.casefold() in ship_names:
            return jsonify({"error": "Ship names must be unique."}), 400
        ship_names.add(name.casefold())
        if not isinstance(hover, bool):
            return jsonify({"error": f"{name} hover setting must be true or false."}), 400
        if isinstance(size, bool) or not isinstance(size, int) or size < 1:
            return jsonify({"error": f"{name} size must be a positive whole number."}), 400
        if shape is not None:
            if (
                not isinstance(shape, list)
                or not 1 <= len(shape) <= 30
                or any(
                    not isinstance(cell, list)
                    or len(cell) != 2
                    or any(isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < 10 for value in cell)
                    for cell in shape
                )
                or len({tuple(cell) for cell in shape}) != len(shape)
            ):
                return jsonify({"error": f"{name} has an invalid custom shape."}), 400
            if len(shape) != size:
                return jsonify({"error": f"{name} size must match its number of selected squares."}), 400
            ship_shape = [tuple(cell) for cell in shape]
        else:
            if size > max(width, height):
                return jsonify({"error": f"{name} is longer than either board dimension."}), 400
            ship_shape = size
        if not isinstance(color, str) or re.fullmatch(r"#[0-9a-fA-F]{6}", color) is None:
            return jsonify({"error": f"{name} must have a valid hex color."}), 400

        colors[name] = color
        (air_ships if hover else ground_ships)[name] = ship_shape

    if sum(ship if isinstance(ship, int) else len(ship) for ship in ground_ships.values()) > width * height:
        return jsonify({"error": "The ground ships have more cells than the board."}), 400
    if sum(ship if isinstance(ship, int) else len(ship) for ship in air_ships.values()) > width * height:
        return jsonify({"error": "The air ships have more cells than the board."}), 400

    try:
        ground_board = place_ships(width, height, ground_ships)
        air_board = place_ships(width, height, air_ships)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "ground_board": ground_board,
        "air_board": air_board,
        "width": width,
        "height": height,
        "colors": colors
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
