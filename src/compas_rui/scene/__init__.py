from compas.plugins import plugin
from compas.scene.context import register

from compas.datastructures import Mesh
from .meshobject import RUIMeshObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(Mesh, RUIMeshObject, context="Rhino")
