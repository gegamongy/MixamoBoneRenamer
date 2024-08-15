import bpy

# Dictionary to map default bone names to Mixamo bone names
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
    # Add more bone mappings if necessary
}

# Dictionary to map default bone names to custom bone names
custom_bone_names = {
    "mixamorig:Hips": "Pelvis",
    "mixamorig:Spine": "Spine.Lower",
    "mixamorig:Spine1": "Spine.Middle",
    "mixamorig:Spine2": "Spine.Upper",
    "mixamorig:Neck": "Neck",
    "mixamorig:Head": "Head",
    "mixamorig:LeftShoulder": "Shoulder.L",
    "mixamorig:LeftArm": "UpperArm.L",
    "mixamorig:LeftForeArm": "Forearm.L",
    "mixamorig:LeftHand": "Hand.L",
    "mixamorig:RightShoulder": "Shoulder.R",
    "mixamorig:RightArm": "UpperArm.R",
    "mixamorig:RightForeArm": "Forearm.R",
    "mixamorig:RightHand": "Hand.R",
    "mixamorig:LeftUpLeg": "Thigh.L",
    "mixamorig:LeftLeg": "Shin.L",
    "mixamorig:LeftFoot": "Foot.L",
    "mixamorig:RightUpLeg": "Thigh.R",
    "mixamorig:RightLeg": "Shin.R",
    "mixamorig:RightFoot": "Foot.R",
    "mixamorig:LeftHandThumb1": "Thumb1.L",
    "mixamorig:LeftHandThumb2": "Thumb2.L",
    "mixamorig:LeftHandThumb3": "Thumb3.L",
    "mixamorig:LeftHandIndex1": "Index1.L",
    "mixamorig:LeftHandIndex2": "Index2.L",
    "mixamorig:LeftHandIndex3": "Index3.L",
    "mixamorig:LeftHandMiddle1": "Middle1.L",
    "mixamorig:LeftHandMiddle2": "Middle2.L",
    "mixamorig:LeftHandMiddle3": "Middle3.L",
    "mixamorig:LeftHandRing1": "Ring1.L",
    "mixamorig:LeftHandRing2": "Ring2.L",
    "mixamorig:LeftHandRing3": "Ring3.L",
    "mixamorig:LeftHandPinky1": "Pinky1.L",
    "mixamorig:LeftHandPinky2": "Pinky2.L",
    "mixamorig:LeftHandPinky3": "Pinky3.L",
    "mixamorig:RightHandThumb1": "Thumb1.R",
    "mixamorig:RightHandThumb2": "Thumb2.R",
    "mixamorig:RightHandThumb3": "Thumb3.R",
    "mixamorig:RightHandIndex1": "Index1.R",
    "mixamorig:RightHandIndex2": "Index2.R",
    "mixamorig:RightHandIndex3": "Index3.R",
    "mixamorig:RightHandMiddle1": "Middle1.R",
    "mixamorig:RightHandMiddle2": "Middle2.R",
    "mixamorig:RightHandMiddle3": "Middle3.R",
    "mixamorig:RightHandRing1": "Ring1.R",
    "mixamorig:RightHandRing2": "Ring2.R",
    "mixamorig:RightHandRing3": "Ring3.R",
    "mixamorig:RightHandPinky1": "Pinky1.R",
    "mixamorig:RightHandPinky2": "Pinky2.R",
    "mixamorig:RightHandPinky3": "Pinky3.R",
    
    "mixamorig:RightToeBase": "Toe.R",
    "mixamorig:LeftToeBase": "Toe.L",
    # Add more bone mappings if necessary
}

# Function to rename bones to Mixamo names
def rename_bones_to_mixamo(self, context):
    armature = bpy.context.object
    if armature is None or armature.type != 'ARMATURE':
        self.report({'WARNING'}, "Selected object is not an armature")
        return {'CANCELLED'}
    
    for bone in armature.data.bones:
        
        if bone.name in custom_bone_names.values():
            
            bone.name = mixamo_bone_names[bone.name]
    self.report({'INFO'}, "Bones renamed to Mixamo names")
    return {'FINISHED'}

# Function to rename bones to custom names
def rename_bones_to_custom(self, context):
    armature = bpy.context.object
    if armature is None or armature.type != 'ARMATURE':
        self.report({'WARNING'}, "Selected object is not an armature")
        return {'CANCELLED'}
        
    
    print('Checking armature for custom bones...')
    for bone in armature.data.bones:
        
        if bone.name in mixamo_bone_names.values():
           
            
            bone.name = custom_bone_names[bone.name]
    self.report({'INFO'}, "Bones renamed to custom names")
    return {'FINISHED'}   



 # UI Panel
class OBJECT_PT_BoneRenamerPanel(bpy.types.Panel):
    bl_label = "Bone Renamer"
    bl_idname = "OBJECT_PT_bone_renamer_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bone Tools'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.rename_bones_to_mixamo", text="Rename to Mixamo")
        
        row = layout.row()
        row.operator("object.rename_bones_to_custom", text="Rename to Custom")

# Operator for renaming to Mixamo
class OBJECT_OT_RenameBonesToMixamo(bpy.types.Operator):
    bl_label = "Rename Bones to Mixamo"
    bl_idname = "object.rename_bones_to_mixamo"
    
    def execute(self, context):
        rename_bones_to_mixamo(self, context)
        return {'FINISHED'}

# Operator for renaming to Custom
class OBJECT_OT_RenameBonesToCustom(bpy.types.Operator):
    bl_label = "Rename Bones to Custom"
    bl_idname = "object.rename_bones_to_custom"
    
    def execute(self, context):
        rename_bones_to_custom(self, context)
        return {'FINISHED'}

# Register the panel and operators
def register():
    bpy.utils.register_class(OBJECT_PT_BoneRenamerPanel)
    bpy.utils.register_class(OBJECT_OT_RenameBonesToMixamo)
    bpy.utils.register_class(OBJECT_OT_RenameBonesToCustom)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_BoneRenamerPanel)
    bpy.utils.unregister_class(OBJECT_OT_RenameBonesToMixamo)
    bpy.utils.unregister_class(OBJECT_OT_RenameBonesToCustom)

#if __name__ == "__main__":
#    register()


#rename_bones_to_mixamo()
#rename_bones_to_custom()
