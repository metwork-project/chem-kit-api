from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from chem_kit.transformation import Transformation
from chem_kit.transformation.simplifier import SimplifierParams

# from chem_kit_api import __version__ as api_version


# api_description = (Path().parent / "README.md").read_text()
# api_description = "\n".join(api_description.split("\n")[2:])

app = FastAPI(
    title="ChemKit API",
    # description=api_description,
    # version=api_version,
)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://transformation.metwork.science",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transformations_from_smiles")
async def transformations_from_smiles(
    smiles: List[str] = Body(..., example=["CCO", "CCOC"]),
    params: SimplifierParams = Body(BaseModel(), example=SimplifierParams()),
):
    result = []
    transformation = Transformation.from_smiles(*smiles)
    simplified = transformation.simplify(**params.dict())
    for idx, tsf in enumerate(simplified):
        data = {"id": idx, "smarts": tsf.smarts, "chemDoodleJson": tsf.chemdoodle_json}
        result.append(data)
    # simplified_smarts = {tsf.smarts for tsf in simplified}
    # reverted_smarts = {tsf.reverse().smarts for tsf in simplified}
    # result = result.union(simplified_smarts, reverted_smarts)
    return result


@app.post("/smiles_from_smarts")
async def smiles_from_smarts(
    smarts: str = Body(
        ...,
        embed=True,
        example="[#8:1]-[#6:2]1:[#6:3]>>[#8:1]-[#6:2]1:[#6:3]",
    ),
):
    transformation = Transformation(smarts)
    smiles = [transformation.reactant.smiles, transformation.product.smiles]

    return smiles