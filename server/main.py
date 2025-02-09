from typing import Union
from fastapi import FastAPI
import uvicorn
import time

from typing import Tuple, List
from blender.functions import BlenderFunctions
from database.functions import DatabaseFunctions
from dataclass import *

app = FastAPI()

bf = BlenderFunctions()  
dbf = DatabaseFunctions()


@app.get("/") #DONE
def read_root(name: str = None):
    if name is None: return {"rows": dbf.read_object()}
    else: return {"row": dbf.read_object(name)}

@app.post("/translation/{name}")
def translation(name:str, position:positionRequest):
    """Takes only position."""
    time.sleep(10)
    dbf.update_object(name,position)
    bf.translation(name,position)
    return {"message": "Translation successful"}


@app.post("/rotation/{name}")
def rotation(name:str, rotation:rotationRequest):
    """Takes only rotation."""
    time.sleep(10)
    dbf.update_object(name,rotation)
    bf.rotation(name,rotation)
    return {"message": "Rotation successful"}

@app.post("/scale/{name}")
def scale(name:str, scale:scaleRequest):
    """Takes only scale."""
    time.sleep(10)
    dbf.update_object(name,scale)
    bf.scale(name,scale)
    return {"message": "Scale successful"}


@app.post("/transform/{name}")
def transform(name:str, transform:transformRequest):
    """Takes all transforms (position, rotation, scale)."""
    time.sleep(10)
    dbf.update_object(name,transform.new_position)
    dbf.update_object(name,transform.new_rotation)
    dbf.update_object(name,transform.new_scale)
    bf.transform(name,transform.new_position,transform.new_rotation,transform.new_scale)
    return {"message": "Transform successful"}

# ------------------------------------------------------------------------------------------------------------------------------------

@app.get("/filepath")
def filepath(folderpath: bool = False):
    """Returns the DCC file's path. /filepath?projectpath=true returns the project folder path."""
    time.sleep(10)
    if folderpath: return {"folderpath": bf.filepath(folderpath)}
    else: return {"filepath": bf.filepath(folderpath)}

@app.post("/add-item")
def add_item(item: Item):
    """Adds an item to a database (name, quantity)."""
    time.sleep(10)
    dbf.create_object(item)
    bf.add_item(item)
    return {"message": "Add item successful"}

@app.delete("/remove-item")
def remove_item(name: str):
    """Removes an item from the database (by name)."""  
    time.sleep(10)
    dbf.delete_object(name)
    bf.remove_item(name)
    return {"message": "Remove item successful"}

@app.post("/update-quantity")
def update_quantity(name: str, new_quantity: int):
    """Updates an item's quantity (name, new quantity)."""
    time.sleep(10)
    dbf.update_object(name,new_quantity)
    bf.update_quantity(name,new_quantity)
    return {"message": "Update quantity successful"}

def start_server():
    """Runs FastAPI inside Blender."""
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

if __name__ == "__main__":
    start_server()