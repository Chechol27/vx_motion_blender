import logging
import math
import sys

import bpy
import bmesh
from mathutils import Vector

from .vertex_identifiers import VertexIdentifier
from ..pixel_collection import PixelCollection
from .mesh_evaluator import MeshEvaluator

logger = logging.getLogger(__name__+"."+__file__)


class VariableTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection with an intermediary face triangle database created based on an object
    which animation variates its topology, useful for fluid simulations, animated generative modifiers
    and geometry nodes
    """

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)

    def evaluate_mesh(self, evaluated_object: bpy.types.Object) -> bpy.types.Mesh:
        out_mesh = super().evaluate_mesh(evaluated_object)
        b_mesh = bmesh.new()
        b_mesh.from_mesh(out_mesh)
        bmesh.ops.triangulate(b_mesh)
        b_mesh.to_mesh(out_mesh)
        out_mesh.update()
        b_mesh.free()
        return out_mesh

    def create_base_object(self, context: bpy.types.Context) -> bpy.types.Object:
        max_triangle_count = 0
        for ev_mesh in self.evaluated_meshes:
            triangle_count = len(ev_mesh.polygons)
            if triangle_count > max_triangle_count:
                max_triangle_count = triangle_count
        b_mesh = bmesh.new()
        for i in range(max_triangle_count):
            v1 = b_mesh.verts.new(Vector((-0.5, 0, 0)))
            v2 = b_mesh.verts.new(Vector((0, 1, 0)))
            v3 = b_mesh.verts.new(Vector((0.5, 0, 0)))

            b_mesh.edges.new((v1, v2))
            b_mesh.edges.new((v2, v3))
            b_mesh.edges.new((v3, v1))

            b_mesh.faces.new([v1, v2, v3])
        out_mesh = bpy.data.meshes.new(f"{self.object_to_evaluate.name}_VAT")
        b_mesh.to_mesh(out_mesh)

        obj = bpy.data.objects.new(out_mesh.name, out_mesh)
        self.create_uv_maps(obj.data)
        context.collection.objects.link(obj)
        return obj

    def evaluate_vertex_data(self, vertex_identifier: VertexIdentifier) -> list[PixelCollection]:
        ret = []
        layer_vertex_offset = 0
        flattened_evaluated_meshes = []
        # flatten meshes
        for frame_mesh in self.evaluated_meshes:
            vertex_list = []
            polygons = frame_mesh.polygons
            for polygon in polygons:
                match vertex_identifier:
                    case VertexIdentifier.POSITION:
                        vertex_list.extend(frame_mesh.vertices[v_id].co for v_id in polygon.vertices)
                    case VertexIdentifier.NORMAL:
                        vertex_list.extend(frame_mesh.vertex_normals[v_id] for v_id in polygon.vertices)
            flattened_evaluated_meshes.append(vertex_list)
        # Iterate through number of textures (z)
        for tex_coord_count, layer in self.uv_layers:
            shape = (tex_coord_count, len(self.evaluated_meshes), 4)
            pixel_data = PixelCollection(shape)
            # Iterate through frames (y)
            for frame_mesh in flattened_evaluated_meshes:
                # Iterate through vertices by triangle (x)
                frame_vertex_count = 0
                for vertex in frame_mesh[layer_vertex_offset:]:
                    if frame_vertex_count >= tex_coord_count:
                        break
                    pixel_data.append_pixel((vertex.x, vertex.y, vertex.z, 1))
                    frame_vertex_count += 1
                if frame_vertex_count < tex_coord_count:
                    for i in range(tex_coord_count - frame_vertex_count):
                        pixel_data.append_pixel((0, 0, 0, 1))
            ret.append(pixel_data)
            layer_vertex_offset += tex_coord_count
        return ret

    def evaluate_position_data(self) -> list[PixelCollection]:
        return self.evaluate_vertex_data(VertexIdentifier.POSITION)

    def evaluate_normal_data(self) -> list[PixelCollection]:
        return self.evaluate_vertex_data(VertexIdentifier.NORMAL)

    def evaluate_tangent_data(self) -> list[PixelCollection]:
        pass
