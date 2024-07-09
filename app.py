from flask import Flask
from pyplate import Substance, Container, Plate, Recipe

app = Flask(__name__)


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
