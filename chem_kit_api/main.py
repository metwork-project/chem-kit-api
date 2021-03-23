from typing import List
from pathlib import Path
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from chem_kit.transformation import Transformation
from . import __version__ as api_version


api_description = (Path().parent / "README.md").read_text()
api_description = "\n".join(api_description.split("\n")[2:])

app = FastAPI(
    title="ChemKit API",
    description=api_description,
    version=api_version,
)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:3000",
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
    smiles: List[str] = Body(..., example=["CCO", "CCOC"])
):
    result = []
    transformation = Transformation.from_smiles(*smiles)
    simplified = transformation.simplify()  # **params)
    for idx, tsf in enumerate(simplified):
        data = {"id": idx, "smarts": tsf.smarts, "chemDoodleJson": tsf.chemdoodle_json}
        result.append(data)
    # simplified_smarts = {tsf.smarts for tsf in simplified}
    # reverted_smarts = {tsf.reverse().smarts for tsf in simplified}
    # result = result.union(simplified_smarts, reverted_smarts)
    return result
