import bpy

bl_info = {
    "name": "Mixamo Bone Renamer",
    "author": "Your Name",
    "version": (1, 1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Bone Tools",
    "description": "Rename bones between Mixamo and custom naming conventions",
    "category": "Rigging",
}

# Default Mixamo bone name dictionary
mixamo_bone_names = {
    "Pelvis": "mixamorig:Hips",
    "Spine.Lower": "mixamorig:Spine",
    "Spine.Middle": "mixamorig:Spine1",
    "Spine.Upper": "mixamorig:Spine2",
    "Neck": "mixamorig:Neck",
    "Head": "mixamorig:Head",
    "Shoulder.L": "mixamorig:LeftShoulder",
    "UpperArm.L": "mixamorig:LeftArm",
    "Forearm.L": "mixamorig:LeftForeArm",
    "Hand.L": "mixamorig:LeftHand",
    "Shoulder.R": "mixamorig:RightShoulder",
    "UpperArm.R": "mixamorig:RightArm",
    "Forearm.R": "mixamorig:RightForeArm",
    "Hand.R": "mixamorig:RightHand",
    "Thigh.L": "mixamorig:LeftUpLeg",
    "Shin.L": "mixamorig:LeftLeg",
    "Foot.L": "mixamorig:LeftFoot",
    "Thigh.R": "mixamorig:RightUpLeg",
    "Shin.R": "mixamorig:RightLeg",
    "Foot.R": "mixamorig:RightFoot",
    "Thumb1.L": "mixamorig:LeftHandThumb1",
    "Thumb2.L": "mixamorig:LeftHandThumb2",
    "Thumb3.L": "mixamorig:LeftHandThumb3",
    "Index1.L": "mixamorig:LeftHandIndex1",
    "Index2.L": "mixamorig:LeftHandIndex2",
    "Index3.L": "mixamorig:LeftHandIndex3",
    "Middle1.L": "mixamorig:LeftHandMiddle1",
    "Middle2.L": "mixamorig:LeftHandMiddle2",
    "Middle3.L": "mixamorig:LeftHandMiddle3",
    "Ring1.L": "mixamorig:LeftHandRing1",
    "Ring2.L": "mixamorig:LeftHandRing2",
    "Ring3.L": "mixamorig:LeftHandRing3",
    "Pinky1.L": "mixamorig:LeftHandPinky1",
    "Pinky2.L": "mixamorig:LeftHandPinky2",
    "Pinky3.L": "mixamorig:LeftHandPinky3",
    "Thumb1.R": "mixamorig:RightHandThumb1",
    "Thumb2.R": "mixamorig:RightHandThumb2",
    "Thumb3.R": "mixamorig:RightHandThumb3",
    "Index1.R": "mixamorig:RightHandIndex1",
    "Index2.R": "mixamorig:RightHandIndex2",
    "Index3.R": "mixamorig:RightHandIndex3",
    "Middle1.R": "mixamorig:RightHandMiddle1",
    "Middle2.R": "mixamorig:RightHandMiddle2",
    "Middle3.R": "mixamorig:RightHandMiddle3",
    "Ring1.R": "mixamorig:RightHandRing1",
    "Ring2.R": "mixamorig:RightHandRing2",
    "Ring3.R": "mixamorig:RightHandRing3",
    "Pinky1.R": "mixamorig:RightHandPinky1",
    "Pinky2.R": "mixamorig:RightHandPinky2",
    "Pinky3.R": "mixamorig:RightHandPinky3",
    "Toe.L": "mixamorig:RightToeBase",
    "Toe.R": "mixamorig:LeftToeBase",
}

# Reverse lookup dictionary
custom_bone_names = {v: k for k, v in mixamo_bone_names.items()}


# --------- Editable Custom Map Data ---------
class BoneMappingItem(bpy.types.PropertyGroup):
    original: bpy.props.StringProperty(name="Original")
    target: bpy.props.StringProperty(name="Target")

class OBJECT_UL_BoneMappingList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(item, "original", text="", emboss=False)
        row.prop(item, "target", text="", emboss=False)

class BONE_MAPPING_OT_Add(bpy.types.Operator):
    bl_idname = "bone_mapping.add"
    bl_label = "Add Bone Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene:
            context.scene.bone_mappings.add()
            return {'FINISHED'}
        return {'CANCELLED'}

class BONE_MAPPING_OT_Remove(bpy.types.Operator):
    bl_idname = "bone_mapping.remove"
    bl_label = "Remove Bone Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.scene:
            return {'CANCELLED'}
        idx = context.scene.bone_mappings_index
        mappings = context.scene.bone_mappings
        if mappings and 0 <= idx < len(mappings):
            mappings.remove(idx)
            context.scene.bone_mappings_index = min(max(0, idx - 1), len(mappings) - 1)
        return {'FINISHED'}

class OBJECT_OT_RenameBonesUsingMap(bpy.types.Operator):
    bl_label = "Rename Bones Using Map"
    bl_idname = "object.rename_bones_custom_map"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an armature")
            return {'CANCELLED'}

        if not context.scene:
            self.report({'WARNING'}, "No scene context available")
            return {'CANCELLED'}

        mapping = {item.original: item.target for item in context.scene.bone_mappings}
        renamed = 0
        for bone in armature.data.bones:
            if bone.name in mapping:
                bone.name = mapping[bone.name]
                renamed += 1

        self.report({'INFO'}, f"Renamed {renamed} bones using custom map")
        return {'FINISHED'}


# --------- Original Mixamo Functions ---------
def rename_bones_to_mixamo(self, context):
    armature = context.object
    if not armature or armature.type != 'ARMATURE':
        self.report({'WARNING'}, "Selected object is not an armature")
        return {'CANCELLED'}

    for bone in armature.data.bones:
        if bone.name in mixamo_bone_names:
            bone.name = mixamo_bone_names[bone.name]
    self.report({'INFO'}, "Bones renamed to Mixamo names")
    return {'FINISHED'}

def rename_bones_to_custom(self, context):
    armature = context.object
    if not armature or armature.type != 'ARMATURE':
        self.report({'WARNING'}, "Selected object is not an armature")
        return {'CANCELLED'}

    for bone in armature.data.bones:
        if bone.name in custom_bone_names:
            bone.name = custom_bone_names[bone.name]
    self.report({'INFO'}, "Bones renamed to custom names")
    return {'FINISHED'}


# --------- Panel UI ---------
class OBJECT_PT_BoneRenamerPanel(bpy.types.Panel):
    bl_label = "Bone Renamer"
    bl_idname = "OBJECT_PT_bone_renamer_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bone Tools'

    @classmethod
    def poll(cls, context):
        # Always show the panel
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Safety check for scene
        if not scene:
            layout.label(text="No scene context available")
            return

        # Safely preload defaults once
        if not scene.bone_mappings:
            for original, target in mixamo_bone_names.items():
                item = scene.bone_mappings.add()
                item.original = original
                item.target = target

        layout.operator("object.rename_bones_to_mixamo", text="Rename Default Custom Names to Mixamo")
        layout.operator("object.rename_bones_to_custom", text="Rename to Default Custom")

        layout.separator()
        layout.label(text="Custom Bone Mappings:")
        row = layout.row()
        row.template_list("OBJECT_UL_BoneMappingList", "", scene, "bone_mappings", scene, "bone_mappings_index")

        row = layout.row(align=True)
        row.operator("bone_mapping.add", icon="ADD", text="")
        row.operator("bone_mapping.remove", icon="REMOVE", text="")

        layout.operator("object.rename_bones_custom_map", text="Rename to Mixamo Using Map")
        layout.operator("object.rename_bones_custom_reverse", text="Rename to Custom Using Map")


# --------- Operator Definitions ---------
class OBJECT_OT_RenameBonesToMixamo(bpy.types.Operator):
    bl_label = "Rename Bones to Mixamo"
    bl_idname = "object.rename_bones_to_mixamo"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        return rename_bones_to_mixamo(self, context)

class OBJECT_OT_RenameBonesToCustom(bpy.types.Operator):
    bl_label = "Rename Bones to Custom"
    bl_idname = "object.rename_bones_to_custom"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        return rename_bones_to_custom(self, context)
    
class OBJECT_OT_RenameBonesUsingReverseMap(bpy.types.Operator):
    bl_label = "Rename Using Reverse Map"
    bl_idname = "object.rename_bones_custom_reverse"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'ARMATURE'

    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an armature")
            return {'CANCELLED'}

        if not context.scene:
            self.report({'WARNING'}, "No scene context available")
            return {'CANCELLED'}

        # Create a reversed mapping: {target: original}
        reverse_mapping = {item.target: item.original for item in context.scene.bone_mappings}
        renamed = 0
        for bone in armature.data.bones:
            if bone.name in reverse_mapping:
                bone.name = reverse_mapping[bone.name]
                renamed += 1

        self.report({'INFO'}, f"Renamed {renamed} bones using reverse map")
        return {'FINISHED'}


# --------- Registration ---------
classes = (
    BoneMappingItem,
    OBJECT_UL_BoneMappingList,
    BONE_MAPPING_OT_Add,
    BONE_MAPPING_OT_Remove,
    OBJECT_OT_RenameBonesUsingMap,
    OBJECT_PT_BoneRenamerPanel,
    OBJECT_OT_RenameBonesToMixamo,
    OBJECT_OT_RenameBonesToCustom,
    OBJECT_OT_RenameBonesUsingReverseMap,
    
)

# def preload_default_mappings():
#     scene = bpy.context.scene
#     if not scene.bone_mappings:
#         for original, target in mixamo_bone_names.items():
#             item = scene.bone_mappings.add()
#             item.original = original
#             item.target = target

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bone_mappings = bpy.props.CollectionProperty(type=BoneMappingItem)
    bpy.types.Scene.bone_mappings_index = bpy.props.IntProperty()
    
    
    # # Preload only once after registering
    # preload_default_mappings()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bone_mappings
    del bpy.types.Scene.bone_mappings_index

# if __name__ == "__main__":
#     register()
