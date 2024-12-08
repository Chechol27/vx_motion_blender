import logging
import math

import bpy
import bmesh
from mathutils import Vector

from ..pixel_collection import PixelCollection
from .mesh_evaluator import MeshEvaluator

logger = logging.getLogger(__name__+"."+__file__)

class VariableTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection with an intermediary face triangle database that stems from an object
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

    def evaluate_position_data(self) -> list[PixelCollection]:
        ret = []
        for tex_coord_count, layer in self.uv_layers:
            polygon_offset = 0
            shape = (tex_coord_count, len(self.evaluated_meshes), 4)
            pixel_data = PixelCollection(shape)
            polygon_count = 0
            vertex_count = 0
            for mesh in self.evaluated_meshes:
                polygon_count = max(polygon_count, len(mesh.polygons))
                for polygon in mesh.polygons[polygon_offset:]:
                    if vertex_count + len(polygon.vertices) > tex_coord_count:
                        vertex_count = 0
                        break
                    for vertex in polygon.vertices:
                        v = mesh.vertices[vertex]
                        pixel_data.append_pixel((v.co.x, v.co.y, v.co.z, 1))
                        vertex_count += 1

                if vertex_count < tex_coord_count:
                    for i in range(tex_coord_count-vertex_count):
                        pixel_data.append_pixel((0, 0, 0, 1))

            polygon_offset += polygon_count
            ret.append(pixel_data)
        return ret

    def evaluate_normal_data(self) -> list[PixelCollection]:
        pass

    def evaluate_tangent_data(self) -> list[PixelCollection]:
        pass
