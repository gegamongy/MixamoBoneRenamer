bl_info = {
    "name": "Mixamo Bone Renamer",
    "blender": (4, 0, 2),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Gegamongy",
    "description": "An addon to rename bones to Mixamo or custom names.",
    "location": "View3D > Sidebar > Bone Tools",
    "warning": "",
    "wiki_url": "https://github.com/Gegamongy/MixamoBoneRenamer",
    "tracker_url": "https://github.com/Gegamongy/MixamoBoneRenamer/issues",
    "support": "COMMUNITY",
}

if "bpy" in locals():
    import importlib
    importlib.reload(mixamo_bone_renamer)
else:
    from . import mixamo_bone_renamer

import bpy

def register():
    mixamo_bone_renamer.register()

def unregister():
    mixamo_bone_renamer.unregister()

if __name__ == "__main__":
    register()
