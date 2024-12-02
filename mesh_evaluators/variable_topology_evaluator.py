import bpy
import bmesh
from mathutils import Vector
from .mesh_evaluator import MeshEvaluator


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
