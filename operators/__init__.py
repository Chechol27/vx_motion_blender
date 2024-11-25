import bpy

class BakeVat(bpy.types.Operator):
    bl_idname = "object.vat_export"
    bl_label = "Bake VAT for selected object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        return {'FINISHED'}
