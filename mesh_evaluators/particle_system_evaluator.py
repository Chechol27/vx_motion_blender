import bpy
from .mesh_evaluator import MeshEvaluator


class ParticleSystemEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection with an intermediary face triangle cloud database that stems from an object
    which animation variates its topology, specialized for particle systems using 2 triangles per particle
    """

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)
