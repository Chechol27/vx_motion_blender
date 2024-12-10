import bpy.types
import logging
from typing import cast
from .mesh_evaluator import MeshEvaluator
from .constant_topology_evaluator import ConstantTopologyEvaluator
from .variable_topology_evaluator import VariableTopologyEvaluator
from .particle_system_evaluator import ParticleSystemEvaluator
from .smoke_simulation_evaluator import SmokeSimulationEvaluator


logger = logging.getLogger(__name__+"."+__file__)


def evaluate_variable_topology(object_to_evaluate: bpy.types.Object) -> bool:
    variable_topology_modifiers = ['NODES', 'PARTICLE_SYSTEM', 'FLUID', 'VOLUME_TO_MESH']
    for modifier in object_to_evaluate.modifiers:
        if modifier.type in variable_topology_modifiers:
            return True
    return False


def get_fluid_simulation_evaluator(context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)) -> MeshEvaluator:
    fluid_modifier = cast(bpy.types.FluidModifier, [mod for mod in object_to_evaluate.modifiers if mod.type == "FLUID"][0])
    if fluid_modifier.fluid_type != "DOMAIN":
        print("!!!VATs fluid simulation object must be flow")
    domain_type = fluid_modifier.domain_settings.domain_type
    if domain_type in ["SMOKE", "BOTH", "FIRE"]:
        return SmokeSimulationEvaluator(context, object_to_evaluate, frame_range)
    else:
        return VariableTopologyEvaluator(context, object_to_evaluate, frame_range)


def get_variable_topology_evaluator(context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)) -> MeshEvaluator:
    evaluator_dict = {
        "NODES": VariableTopologyEvaluator,
        "PARTICLE_SYSTEM": ParticleSystemEvaluator,
        "FLUID": get_fluid_simulation_evaluator,
        "VOLUME_TO_MESH": VariableTopologyEvaluator
    }

    for modifier in object_to_evaluate.modifiers:
        if modifier.type in evaluator_dict:
            return evaluator_dict[modifier.type](context, object_to_evaluate, frame_range)

    return VariableTopologyEvaluator(context, object_to_evaluate, frame_range)


def get_mesh_evaluator(context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)) -> MeshEvaluator:
    # for smoke simulations and particle systems
    if evaluate_variable_topology(object_to_evaluate):
        logger.info(f"{object_to_evaluate.name} has variable topology")
        return get_variable_topology_evaluator(context, object_to_evaluate, frame_range)
    else:
        logger.info(f"{object_to_evaluate.name} has constant topology")
        return ConstantTopologyEvaluator(context, object_to_evaluate, frame_range)
    pass
