import sqlite3
from dataclass import *
import sqlite3
import json
from dataclasses import asdict
from typing import *
import ast

class DatabaseFunctions:
    def __init__(self):
        self.conn = sqlite3.connect("your_database.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS objects (
                name VARCHAR PRIMARY KEY,
                type TEXT CHECK(type IN ('cube', 'sphere', 'cylinder', 'plane', 'custom')),
                properties TEXT,
                values_ TEXT,
                dimensions TEXT,
                quantity INTEGER NOT NULL CHECK(quantity >= 0)
            )
            """)
        self.conn.commit()

    def exitdb(self):
        try:    
            self.conn.close()
        except Exception as e:
            print(f"Error closing database: {e}")

    def create_object(self, item:Item):
        try:
            position = [item.position.x,item.position.y,item.position.z]
            rotation = [item.rotation.x,item.rotation.y,item.rotation.z]
            scale = [item.scale.x,item.scale.y,item.scale.z]
            self.cursor.execute("INSERT INTO objects (name, type, properties, values_, dimensions ,quantity) VALUES (?, ?, ?, ?, ?, ?)", (item.name, item.type, f"['position','rotation','scale']", f"[{position},{rotation},{scale}]", json.dumps(item.dimensions) ,item.qty))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error posting object: {e}")
            return None

    def read_object(self,name: str = None):
        try:
            if name is None: self.cursor.execute("SELECT * FROM objects")
            else: self.cursor.execute("SELECT * FROM objects WHERE name = ?", (name,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching objects: {e}")
            return None

    def update_object(self, name: str, updateBody: Union[positionRequest,rotationRequest,scaleRequest,int]):
        row = self.read_object(name)[0]
        props_ = ast.literal_eval(row[2])
        vals_ = ast.literal_eval(row[3])
        try: 
            qty = row[-1]
            query = "UPDATE objects SET name = ?, type = ?, properties = ?, values_ = ?, dimensions = ?, quantity = ? WHERE name = ?"
            if isinstance(updateBody,positionRequest):
                new_vals = [[updateBody.x,updateBody.y,updateBody.z],vals_[1],vals_[2]]
                self.cursor.execute(query, (name, row[1], str(props_), str(new_vals) ,row[5], qty, name))
            elif isinstance(updateBody,rotationRequest): 
                new_vals = [vals_[0],[updateBody.x,updateBody.y,updateBody.z],vals_[2]]
                self.cursor.execute(query, (name, row[1], str(props_), str(new_vals),row[5], qty, name))
            elif isinstance(updateBody,scaleRequest):
                new_vals = [vals_[0],vals_[1],[updateBody.x,updateBody.y,updateBody.z]]
                self.cursor.execute(query, (name, row[1], str(props_), str(new_vals) ,row[5], qty, name))
            else:
                qty = updateBody
                self.cursor.execute(query, (name, row[1], str(props_), str(vals_) ,row[5], qty, name))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating object: {e}")
            return None

    def delete_object(self, name: str):
        try:
            self.cursor.execute("DELETE FROM objects WHERE name = ?", (name,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting object: {e}")
            return False

