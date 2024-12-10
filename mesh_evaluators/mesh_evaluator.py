import abc
import bpy
import logging
from mathutils import Vector

from ..pixel_collection import PixelCollection
from .vertex_identifiers import VertexIdentifier
logger = logging.getLogger(__name__+"."+__file__)


class MeshEvaluator(abc.ABC):

    evaluated_meshes: list[bpy.types.Mesh]
    object_to_evaluate: bpy.types.Object
    uv_layers: list[tuple[int, bpy.types.MeshUVLoopLayer]]
    base_object: bpy.types.Object
    frame_range: tuple[int, int]

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        self.frame_range = frame_range
        self.evaluated_meshes = []
        self.object_to_evaluate = object_to_evaluate
        self.uv_layers = []
        for i in range(self.frame_range[0], self.frame_range[1] + 1):
            context.scene.frame_set(i)
            eval_obj = self.evaluate_object(context, self.object_to_evaluate)
            self.evaluated_meshes.append(self.evaluate_mesh(eval_obj))
        self.base_object = self.create_base_object(context)

    def evaluate_object(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object):
        deps_graph = context.evaluated_depsgraph_get()
        return object_to_evaluate.evaluated_get(deps_graph)

    def evaluate_mesh(self, evaluated_object: bpy.types.Object) -> bpy.types.Mesh:
        return bpy.data.meshes.new_from_object(evaluated_object)

    @abc.abstractmethod
    def evaluate_vertex_data(self, vertex_identifier: VertexIdentifier) -> list[PixelCollection]:
        pass

    @abc.abstractmethod
    def create_base_object(self, context: bpy.types.Context) -> bpy.types.Object:
        pass

    @abc.abstractmethod
    def evaluate_position_data(self) -> list[PixelCollection]:
        pass

    @abc.abstractmethod
    def evaluate_normal_data(self) -> list[PixelCollection]:
        pass

    @abc.abstractmethod
    def evaluate_tangent_data(self) -> list[PixelCollection]:
        pass

    def create_uv_maps(self, ev_mesh: bpy.types.Mesh):
        """
        Creates an uv map every 4096 vertices, these go from left to right and start at Y=0
        maximum 4 uv maps including the ones already in the mesh for more than 16384 vertices, the system will use
        multiple meshes and textures
        :param ev_mesh: evaluated mesh for modification
        """
        uv_map_count = -1
        loop_counter = 0
        layer_name = ""
        logger.info(f"Creating uv maps for base mesh ({len(ev_mesh.vertices)} vertices)")
        for v_id, vertex in enumerate(ev_mesh.vertices):
            if loop_counter >= 4096 or uv_map_count < 0:
                x_limit = min(4096, len(ev_mesh.vertices) - v_id)
                loop_counter = 0
                uv_map_count += 1
                layer_name = f"VAT_{uv_map_count}"
                try:
                    ev_mesh.uv_layers.remove(ev_mesh.uv_layers[layer_name])
                except Exception as e:
                    print(f"Creating new uv layer ({layer_name})")
                    self.uv_layers.append((x_limit, ev_mesh.uv_layers.new(name=layer_name, do_init=False)))
            ev_mesh.uv_layers[layer_name].data[v_id].uv = Vector((loop_counter/x_limit, 0))
            loop_counter += 1
