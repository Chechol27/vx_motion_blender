bl_info = {
    "name": "Vertex animation textures",
    "version": (1, 0, 0),
    "author": "Sergio Peñaloza",
    "blender": (4, 0, 0),
    "description": "Export simulations and animations as vector displacement textures",
    "location": "View3d tools panel",
    "category": "Animation"
}


import sys
import importlib

load_order = [
    'mesh_evaluators',
    'mesh_evaluators.mesh_evaluator',
    'mesh_evaluators.constant_topology_evaluator',
    'mesh_evaluators.variable_topology_evaluator',
    'mesh_evaluators.smoke_simulation_evaluator',
    'mesh_evaluators.particle_system_evaluator',
    'operators'
    '.bake_vat',
]


def get_loaded_modules():
    prefix = __name__ + "."
    return [name for name in sys.modules if name.startswith(prefix)]


def reload_modules():
    names = [__name__ + "." + name for name in load_order]
    print(f"VATs Reloading modules: {names}")
    for name in names:
        importlib.reload(sys.modules[name])


def compare_lists(a:list, b:list) -> bool:
    a_copy = list(a)
    b_copy = list(b)

    print(f"\n\n Comparing lists:\n a: \n{a} \n\n b: \n{b}\n\n")

    return a_copy == b_copy


def load_modules() -> list[str]:
    names = [__name__ + "." + name for name in load_order]
    print(f"VATs Loading modules: {names}")
    for name in names:
        importlib.import_module(name)
    return names

print("\n\n\n\n\n")

if "bpy" in locals():
    reload_modules()
else:
    load_modules()


import bpy
from .operators import bake_vat


def register():
    bake_vat.register()


def unregister():
    bake_vat.unregister()
