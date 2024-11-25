import bpy
from .mesh_evaluator import MeshEvaluator


class VariableTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection with an intermediary face triangle cloud database that stems from an object
    which animation variates its topology, useful for fluid simulations, animated generative modifiers
    and geometry nodes
    """

    evaluated_meshes: [bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
    uv_layers: [bpy.types.MeshUVLoopLayer]
    base_object: bpy.types.Object

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)

    def create_base_object(self, context: bpy.types.Context, vertex_count: int, poly_count: int):
        """
        Creates the vertex database for texture vertex pulling based on max vertex count and max poly count
        :param context: blender context
        :param vertex_count: vertex count of the most topologically dense frame
        :param poly_count: poly count of the most topologically dense frame
        :return: the newly created object
        """

        return None