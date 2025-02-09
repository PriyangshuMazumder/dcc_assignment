import bpy
import sys
import os


# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import your module
from dataclass import *  # Replace 'MyClass' with actual class name


class BlenderFunctions:
    """
    A class that provides utility functions to manipulate objects in Blender 
    using the Blender Python API (bpy).
    """

    def __init__(self):
        """
        Initializes the BlenderFunctions class.
        """
        self.blender_path = "/Applications/Blender.app"
        bpy.ops.wm.open_mainfile(filepath="/Users/priyangshumazumder/Desktop/DSA/DCC_ass/server/untitled.blend",load_ui=True)
        # Get all objects in the current scene
        all_objects = bpy.context.scene.objects

        self.object_names = [obj.name for obj in all_objects]

    def save_blend_file(self):
        """Explicitly call this function to save the Blender file instead of using __del__."""
        bpy.ops.wm.save_as_mainfile(filepath="/Users/priyangshumazumder/Desktop/DSA/DCC_ass/server/untitled.blend")
        print("Blender file saved successfully.")

    def transform(self, obj_name: str, position: positionRequest, rotation: rotationRequest, scale: scaleRequest):
        """
        Applies all transformations (translation, rotation, and scale) to an object.
        """
        try:
            self.translation(obj_name, position)
            self.rotation(obj_name, rotation)
            self.scale(obj_name, scale)
            return True
        except Exception as e:
            print(f"Error in transform: {e}")
            return False

    def translation(self, obj_name: str, position: positionRequest):
        """
        Moves an object to the specified position.
        """
        try:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                position = (position.x,position.y,position.z)
                obj.location = position
                self.save_blend_file()
                print(f"Translated {obj_name} to {position}")
                return True
            else:
                print(f"Object '{obj_name}' not found")
                return False
            
        except Exception as e:
            print(f"Error in translation: {e}")
            return False

    def rotation(self, obj_name: str, rotation: rotationRequest):
        """
        Rotates an object to the specified rotation.
        """
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.rotation_euler = (rotation.x,rotation.y,rotation.z)
            self.save_blend_file()
            print(f"Rotated {obj_name} to {rotation} (radians)")
            return True
        else:
            print(f"Object '{obj_name}' not found")
            return False

    def scale(self, obj_name: str, scale: scaleRequest):
        """
        Scales an object to the specified size.
        """
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.scale = (scale.x,scale.y,scale.z)
            self.save_blend_file()
            print(f"Scaled {obj_name} to {scale}")
        else:
            print(f"Object '{obj_name}' not found")

    def filepath(self, projectpath: bool = False):
        """
        Returns the file path of the current Blender project.
        """
        if projectpath:
            return bpy.path.abspath("//")  # Project folder path
        else:
            return bpy.data.filepath  # Full Blender file path
    

    # def add_item(self, item: Item):
    #     bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

    #     if item.type == "cube":
    #         size = item.dimensions["size"]
    #         bpy.ops.mesh.primitive_cube_add(size=size, location = (item.position.x,item.position.y,item.position.z))
        
    #     elif item.type == "sphere":
    #         radius = item.dimensions["radius"]
    #         bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location = (item.position.x,item.position.y,item.position.z))
        
    #     elif item.type == "cylinder":
    #         radius, depth = item.dimensions["radius"],item.dimensions["height"]
    #         bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location = (item.position.x,item.position.y,item.position.z))
        
    #     elif item.type == "plane":
    #         size = item.dimensions["size"]
    #         bpy.ops.mesh.primitive_plane_add(size=size, location = (item.position.x,item.position.y,item.position.z))
        
    #     self.save_blend_file()
        # elif object_type == "custom":
        #     verts, faces = dimensions
        #     mesh = bpy.data.meshes.new(name)
        #     obj = bpy.data.objects.new(name, mesh)
        #     bpy.context.collection.objects.link(obj)
        #     mesh.from_pydata(verts, [], faces)
        #     mesh.update()
        #     if custom_properties:
        #         for key, value in custom_properties.items():
        #             obj[key] = value
        #     return obj  # Return the created custom object

        # else:
        #     print("Unsupported object type!")
        #     return None

    #     obj = bpy.context.view_layer.objects.active  # Get the created object
    #     if obj:
    #         obj.name = item.name  # Rename the object
    #         return obj  # Return the created object
    #     else:
    #         print("Failed to create object.")
    #         return None

    def add_item(self, item: Item):
        if item.name in self.object_names: 
            print("name is taken")
            raise NameError

        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

        obj = None  # Placeholder for the created object

        if item.type == "cube":
            size = item.dimensions["size"]
            bpy.ops.mesh.primitive_cube_add(size=size, location=(item.position.x, item.position.y, item.position.z))
            obj = bpy.context.object  # Get the newly created object

        elif item.type == "sphere":
            radius = item.dimensions["radius"]
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(item.position.x, item.position.y, item.position.z))
            obj = bpy.context.object

        elif item.type == "cylinder":
            radius, depth = item.dimensions["radius"], item.dimensions["height"]
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(item.position.x, item.position.y, item.position.z))
            obj = bpy.context.object

        elif item.type == "plane":
            size = item.dimensions["size"]
            bpy.ops.mesh.primitive_plane_add(size=size, location=(item.position.x, item.position.y, item.position.z))
            obj = bpy.context.object

        if obj:
            obj.name = item.name  # Assign the correct name
            obj["quantity"] = item.qty
            self.save_blend_file()
            print(f"Created object: {obj.name}")
            return obj
        else:
            print("Failed to create object.")
            return None

    def remove_item(self, name: str):
        """
        Removes an object from the Blender scene by name.
        """
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)  # Remove object
            self.save_blend_file()
            print(f"Removed object: {name}")
            return True
        else:
            print(f"Object '{name}' not found")
            return False


    def update_quantity(self, name: str, new_quantity: int):
        """
        Updates the quantity of an object in the Blender scene.
        """
        obj = bpy.data.objects.get(name)
        if obj:
            obj["quantity"] = new_quantity
            print(f"Updated quantity of '{name}' to {new_quantity}")
            self.save_blend_file()
            return True
        else:
            print(f"Object '{name}' not found")
            return False

# if __name__ == "__main__":
#     # Create a test object
#     test_obj = Item(
#         name="Cube1",
#         qty=5,
#         type="cube",
#         dimensions={"size": 2.0},
#         position=positionRequest(x=0.0, y=0.0, z=0.0),
#         rotation=rotationRequest(x=0.0, y=0.0, z=0.0),
#         scale=scaleRequest(x=1.0, y=1.0, z=1.0)
#     )

#     # Initialize Blender functions
#     bf = BlenderFunctions()

#     print("\nInitial objects in the scene:")
#     print(bf.object_names)  # Print all objects in the scene

#     # Test adding an object
#     print("\nAdding an object...")
#     added_obj = bf.add_item(test_obj)
#     if added_obj:
#         print(f"Successfully added {added_obj.name}")

#     print("\nObjects after adding:")
#     print([obj.name for obj in bpy.context.scene.objects])  # Print objects after addition

#     # Test transformation (translate, rotate, scale)
#     print("\nTransforming the object...")
#     bf.transform(
#         obj_name="Cube1",
#         position=positionRequest(x=2.0, y=3.0, z=4.0),
#         rotation=rotationRequest(x=0.5, y=0.5, z=0.5),
#         scale=scaleRequest(x=1.5, y=1.5, z=1.5),
#     )

#     # Test updating quantity
#     print("\nUpdating quantity...")
#     bf.update_quantity("Cube1", 10)

#     # Test removing the object
#     print("\nRemoving the object...")
#     bf.remove_item("Cube1")

#     print("\nObjects after removal:")
#     print([obj.name for obj in bpy.context.scene.objects])  # Print objects after removal
