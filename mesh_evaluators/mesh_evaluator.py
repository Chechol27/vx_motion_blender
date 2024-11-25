import abc
import bpy
from ..pixel_collection import PixelCollection


class MeshEvaluator(abc.ABC):
    evaluated_meshes: [bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
    uv_layers: [bpy.types.MeshUVLoopLayer]
    base_object: bpy.types.Object
    frame_range: (int, int)

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        pass

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
        raise Exception("Per Verex normal baking not implemened")
