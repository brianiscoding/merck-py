from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
from pyplate import Substance, Container, Plate, Recipe


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# CORS(app, origins=["http://localhost:3000"])


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/foo")
def foo():
    triethylamine = Substance.liquid(
        name="triethylamine", mol_weight=101.19, density=0.726
    )
    water = Substance.liquid(name="water", mol_weight=18.015, density=1.0)

    triethylamine_50mM = Container.create_solution(
        solute=triethylamine,
        solvent=water,
        concentration="50 mM",
        total_quantity="10 mL",
    )

    plate = Plate(name="plate", max_volume_per_well="50 uL")

    recipe = Recipe().uses(triethylamine_50mM, plate)
    recipe.transfer(
        source=triethylamine_50mM, destination=plate[2:7, 2:11], quantity="10 uL"
    )
    results = recipe.bake()
    triethylamine_50mM = results[triethylamine_50mM.name]
    plate = results[plate.name]

    return str(plate.get_volumes(unit="uL"))


@app.route("/bar", methods=["POST"])
def bar():
    data = request.json
    for x in data:
        print(x, file=sys.stderr)

    return jsonify(data)


@app.route("/test", methods=["POST"])
def test():
    data = request.json

    objs = {}
    for obj in data["preparations"]:
        objs[obj["name"]] = create_obj(obj)

    for name in objs:
        print(objs[name].is_solid(), file=sys.stderr)

    return jsonify(data)


def create_obj(obj):
    name = obj["name"]
    match obj["type"]:

        case "Solid":
            mol_weight = float(obj["molweight"])
            return Substance.solid(name=name, mol_weight=mol_weight)

        case "Liquid":
            mol_weight = float(obj["molweight"])
            density = float(obj["density"])
            return Substance.liquid(
                name=name,
                mol_weight=mol_weight,
                density=density,
            )

        case "Enzyme":
            specific_activity = obj["activity"]
            return Substance.enzyme(name=name, specific_activity=specific_activity)
