import bpy
import logging


from .mesh_evaluator import MeshEvaluator
from mathutils import Vector
from ..pixel_collection import PixelCollection


logger = logging.getLogger(__name__+"."+__file__)


class ConstantTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection from an object which animation has a constant topology
    useful for rigged meshes , soft bodies, ocean, clothes, etc
    """

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)

    def create_base_object(self, context: bpy.types.Context):
        mesh = self.evaluated_meshes[0]
        self.create_uv_maps(mesh)
        obj = bpy.data.objects.new(f"{self.object_to_evaluate.name}_VAT", mesh)
        context.collection.objects.link(obj)
        self.base_object = obj
        return obj

    def evaluate_position_data(self) -> list[PixelCollection]:
        pos_data_collection: list[PixelCollection] = []
        logger.info(
            f"Evaluating position data ({len(self.evaluated_meshes)} evaluated meshes) for object \"{self.base_object.name}\", expected position data count: {len(self.base_object.data.vertices) * len(self.uv_layers) * 4}")
        for ev_mesh in self.evaluated_meshes:
            vertex_offset = 0
            for layer_id, (tex_coord_count, layer_info) in enumerate(self.uv_layers):
                if len(pos_data_collection) < layer_id + 1:
                    pos_data_collection.append(PixelCollection((tex_coord_count, len(self.evaluated_meshes), 4)))
                pos_data = pos_data_collection[layer_id]
                vertex_id = 0
                for vertex_id, vertex in enumerate(ev_mesh.vertices[vertex_offset:vertex_offset + tex_coord_count]):
                    pos_data.append_pixel((vertex.co.x, vertex.co.y, vertex.co.z, 1))
                if vertex_id < tex_coord_count:
                    for i in range(tex_coord_count - vertex_id):
                        pos_data.append_pixel((0, 0, 0, 0))
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
                vertex_range = list(range(vertex_offset, vertex_offset + tex_coord_count))
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
