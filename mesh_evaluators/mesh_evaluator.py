import abc
import bpy
from mathutils import Vector

from ..pixel_collection import PixelCollection


class MeshEvaluator(abc.ABC):

    evaluated_meshes: list[bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
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
        self.create_base_object(context)

    def evaluate_object(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object):
        deps_graph = context.evaluated_depsgraph_get()
        return object_to_evaluate.evaluated_get(deps_graph)

    def evaluate_mesh(self, evaluated_object: bpy.types.Object) -> bpy.types.Mesh:
        return bpy.data.meshes.new_from_object(evaluated_object)

    def evaluate_position_data(self) -> list[PixelCollection]:
        pos_data_collection: list[PixelCollection] = []
        for ev_mesh in self.evaluated_meshes:
            vertex_offset = 0
            for layer_id, (tex_coord_count, layer_info) in enumerate(self.uv_layers):
                if len(pos_data_collection) < layer_id + 1:
                    pos_data_collection.append(PixelCollection((tex_coord_count, len(self.evaluated_meshes), 4)))
                pos_data = pos_data_collection[layer_id]
                for vertex_id, vertex in enumerate(ev_mesh.vertices[vertex_offset:vertex_offset + tex_coord_count]):
                    pos_data.append_pixel((vertex.co.x, vertex.co.y, vertex.co.z, 1))
                vertex_offset += tex_coord_count
        return pos_data_collection

    def evaluate_normal_data(self) -> list[PixelCollection]:
        normal_data_collection: list[PixelCollection] = []
        for ev_mesh in self.evaluated_meshes:
            vertex_offset = 0
            for layer_id, (tex_coord_count, layer_info) in enumerate(self.uv_layers):
                if len(normal_data_collection) < layer_id + 1:
                    normal_data_collection.append(PixelCollection((tex_coord_count, len(self.evaluated_meshes), 4)))
                normal_data = normal_data_collection[layer_id]
                for vertex_id, normal in enumerate(
                        ev_mesh.vertex_normals[vertex_offset:vertex_offset + tex_coord_count]):
                    normal_data.append_pixel((normal.vector.x, normal.vector.y, normal.vector.z, 1))
                vertex_offset += tex_coord_count
        return normal_data_collection

    def evaluate_tangent_data(self) -> list[PixelCollection]:
        me = self.evaluated_meshes[0]
        tangent_data_collection: list[PixelCollection] = []
        for ev_mesh in self.evaluated_meshes:
            vertex_offset = 0
            for layer_id, (tex_coord_count, layer_info) in enumerate(self.uv_layers):
                if len(tangent_data_collection) < layer_id + 1:
                    tangent_data_collection.append(PixelCollection((tex_coord_count, len(self.evaluated_meshes), 4)))
                tangent_data = tangent_data_collection[layer_id]
                ev_mesh.calc_tangents()
                vertex_range = list(range(vertex_offset, vertex_offset+tex_coord_count))
                tangents = [Vector() for r in vertex_range]
                for face in ev_mesh.polygons:
                    for loop_id in face.loop_indices:
                        loop = me.loops[loop_id]
                        if loop.vertex_index not in vertex_range:
                            continue
                        tangents[loop.vertex_index - vertex_offset] += loop.tangent
                for tangent in tangents:
                    tangent.normalize()
                    tangent_data.append_pixel((tangent.x, tangent.y, tangent.z, 1))
                vertex_offset += tex_coord_count
        return tangent_data_collection

    def create_uv_maps(self, ev_mesh: bpy.types.Mesh):
        """
        Creates an uv map every 1024 vertices without separating polygons, these go from left to right and start at Y=0
        :param ev_mesh: evaluated mesh for modification
        """
        uv_map_count = -1
        loop_counter = 0
        layer_name = ""
        for v_id, vertex in enumerate(ev_mesh.vertices):
            if loop_counter >= 1024 or uv_map_count < 0:
                x_limit = min(1024, len(ev_mesh.vertices) - v_id)
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

    @abc.abstractmethod
    def create_base_object(self, context: bpy.types.Context):
        pass

