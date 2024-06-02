from __future__ import annotations
from enum import Enum
import os
from typing import List, Callable, Dict
from fastapi import FastAPI
from pydantic import BaseModel
import requests


class Operation(str, Enum):
    addition = "+"
    division = "/"
    multiplication = "*"
    subtraction = "-"

Number = int | float

class Calculation(BaseModel):
    operation: Operation
    left: Calculation | Number
    right: Calculation | Number


Calculation.model_rebuild()

CalculationCallBack = Callable[[Calculation], Number]


_OP_REGISTRY = {}
_APP_NAME = ""
app = FastAPI()

env_vars_to_look_at = {
    Operation.addition: "ADDITION_SVC_URL",
    Operation.multiplication: "MULTIPLICATION_SVC_URL",
    Operation.division: "DIVISION_SVC_URL",
    Operation.subtraction: "SUBTRACTION_SVC_URL",
}

def get_remote_url_for_op(o: Operation) -> str:
    svc_url = os.environ.get(env_vars_to_look_at.get(o, "CALC_SVC_URL"), "http://localhost:8000")
    return svc_url + "/calculate"


def calc_fn(c: Calculation | Number) -> Number:
    if isinstance(c, Number):
        return c
    if c.operation in _OP_REGISTRY:
        return _OP_REGISTRY[c.operation](c)
    else:
        response = requests.post(get_remote_url_for_op(c.operation), json=c.model_dump())
        return response.json()


def init_app(app_name, op_callbacks: Dict[Operation, CalculationCallBack]):
    global _APP_NAME, _OP_REGISTRY
    _APP_NAME = app_name

    for k, v in op_callbacks.items():
        _OP_REGISTRY[k] = v

    return app

@app.get("/info")
def info():
   return {
        "app_name": _APP_NAME,
        "operations": [k for k in _OP_REGISTRY]
    }


@app.post("/calculate")
def calculate(c: Calculation) -> Number:
    return calc_fn(c)
