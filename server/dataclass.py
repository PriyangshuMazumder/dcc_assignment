from pydantic import BaseModel
from typing import *

class positionRequest(BaseModel):
    x: float
    y: float
    z: float

class rotationRequest(BaseModel):
    x: float
    y: float
    z: float  

class scaleRequest(BaseModel):
    x: float
    y: float
    z: float

class transformRequest(BaseModel):
    new_position: positionRequest
    new_rotation: rotationRequest
    new_scale: scaleRequest

class Item(BaseModel):
    name: str
    qty: int
    type: str
    dimensions: Dict[str, float]
    position: positionRequest
    rotation: rotationRequest
    scale: scaleRequest


# position_obj = positionRequest(x=10.5, y=20.0, z=5.5)
# rotation_obj = rotationRequest(x=0.0, y=90.0, z=45.0)
# scale_obj = scaleRequest(x=1.0, y=1.0, z=1.0)

# transform_obj = transformRequest(
#     new_position=positionRequest(x=5.0, y=10.0, z=15.0),
#     new_rotation=rotationRequest(x=30.0, y=45.0, z=60.0),
#     new_scale=scaleRequest(x=2.0, y=2.0, z=2.0)
# )



