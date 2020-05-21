import bpy
import importlib
import numpy as np

# check if yt is found in available sys.paths and if not, append path to Anaconda site-packages
# prerequisite of course is to have the yt package and dependencies installed in Anaconda. 
# See yt install instructions: https://yt-project.org/

spec = importlib.util.find_spec('yt')
if spec is None:
    import sys
    sys.path.append('C:\ProgramData\Anaconda3\Lib\site-packages')

import yt
from yt import load

coords_tag = ('Gas', 'Coordinates') # we will use the gas particle coordiantes

#########################################################################################################
# Handler for setting particles of particle systems into 3D space
#########################################################################################################

def particle_setter(scene):
    scene = bpy.context.scene
    cFrame = scene.frame_current
    sFrame = scene.frame_start
    print("Executing particle_setter handler for frame:"+str(cFrame))
    particle_systems = emitter.evaluated_get(degp).particle_systems
    particles = particle_systems[0].particles
#    emitter.particle_systems[0].settings.frame_start = cFrame
    emitter.particle_systems[0].settings.frame_end = cFrame

    particles.foreach_set("location", coord)
    print('particle setting completed for frame '+str(cFrame))

#########################################################################################################
# Prepare scene with emitter and instance object (delete and then add)
#########################################################################################################

# ensure we are in object mode
if bpy.context.mode!='OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')

# delete previous emitter object (really only a vert)
obj_name = "Emitter"
if obj_name in bpy.context.scene.objects:
    objs = bpy.data.objects
    objs.remove(objs[obj_name], do_unlink=True)

# add emitter
bpy.ops.mesh.primitive_vert_add()
bpy.context.object.name = (obj_name)

# creating a vert puts us in EDIT mode so go back to object mode
bpy.ops.object.mode_set(mode='OBJECT')    

bpy.ops.object.select_all(action='DESELECT')

# select all instance objects which were converted previous run
for ob in bpy.context.scene.objects:              
    if ob.type == 'MESH' and ob.name.startswith("instance_object"):
        #Select the object
        ob.select_set(state=True)     
#Delete all objects selected above 
bpy.ops.object.delete()

# add instance object
bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.0025, enter_editmode=False, location=(0, 0, 0))
bpy.ops.object.shade_smooth()
bpy.context.object.name = ("instance_object")  

current_scene = bpy.context.scene

default_cube = current_scene.objects["instance_object"]

# noe insert keys to scale (to reduce "flickering" of stars during rendering)
default_cube.scale = 14.0, 14.0, 14.0
# Set the keyframe with that scale, and which frame.
default_cube.keyframe_insert(data_path="scale", frame=2)

# do it again!
default_cube.scale = 5, 5, 5
default_cube.keyframe_insert(data_path="scale", frame=375)

# do it again!
default_cube.scale = 5, 5, 5
default_cube.keyframe_insert(data_path="scale", frame=536)

#########################################################################################################
# Delete old particle material and create new one
#########################################################################################################

# if particle_instance material already exists delete it
material_name = 'particle_material'
mat = bpy.data.materials.get(material_name)
if mat != None:
    bpy.data.materials.remove(mat)             

# create new material
mat = bpy.data.materials.new(material_name)
mat.use_nodes =True
    
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# get Pricipled BSDF node (should already exist)
bsdf = mat.node_tree.nodes["Principled BSDF"]
# add Mix RGB node
mix_rgb = nodes.new(type="ShaderNodeMixRGB")
mix_rgb.location = (-305, 86)
mix_rgb.inputs[1].default_value = (0.0247225, 0.0301564, 0.974478, 1)
mix_rgb.inputs[2].default_value = (0.891799, 1, 0, 1)


# add Object Info node   
obj_info = nodes.new(type="ShaderNodeObjectInfo")
obj_info.location = (-690, 86)

# make links between the 3 nodes
links.new( obj_info.outputs['Random'], mix_rgb.inputs['Fac'])
links.new( mix_rgb.outputs['Color'], bsdf.inputs['Base Color'])

mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.263036, 0.263036, 0.263036, 1)


# Now assign the material to the instance_object
ob = bpy.context.active_object   
if ob.data.materials:
    # assign to 1st material slot
    ob.data.materials[0] = mat
else:
    # no slots
    ob.data.materials.append(mat)

#########################################################################################################
# Load particles coordinates from file 'filename'
#########################################################################################################

filename = 'C:/Users/your_main_windows_folder/Downloads/TipsyGalaxy/TipsyGalaxy/galaxy.00300'
ds = load(filename)
# strip "/" for naming
xnn2 = 0
xnn = 0
# you only want the file name, not all the directory stuff
while xnn != -1:
    xnn2 = xnn
    xnn = filename.find('/',xnn+1)
fname_out = filename[xnn2+1:]            
dd = ds.all_data()
# load coordiantes for particle setting
#xcoord = dd[coords_tag][:,0].v 
#ycoord = dd[coords_tag][:,1].v
#zcoord = dd[coords_tag][:,2].v
pos = dd['Gas', 'Coordinates'].v
coord = pos.flatten()

print (len(coord))


#########################################################################################################
# Add Partcicle System to Emitter and set location of each particle
######################################################################################################### 

particle_system_name = 'particle'+fname_out
context = bpy.context
sceneb = context.scene
emitter = sceneb.objects.get(obj_name)
emitter.modifiers.new(name="partcicle_system", type='PARTICLE_SYSTEM')
emitter.particle_systems[0].settings.count = numrows = len(coord)/3
emitter.particle_systems[0].settings.frame_start = -1
emitter.particle_systems[0].settings.frame_end = 2

emitter.particle_systems[0].settings.lifetime = 900
emitter.particle_systems[0].settings.render_type = 'OBJECT'
emitter.particle_systems[0].settings.instance_object = bpy.data.objects["instance_object"]
emitter.particle_systems[0].settings.particle_size = 1
emitter.particle_systems[0].settings.emit_from = 'VERT'
emitter.particle_systems[0].settings.size_random = 0
emitter.particle_systems[0].settings.show_unborn = True
emitter.particle_systems[0].settings.use_emit_random = False
#emitter.particle_systems[0].seed = 50
#emitter.show_instancer_for_viewport = False

#--------------------------------------------------------------------------------------------------------#
# clear any previous pre- or post handlers
#bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_post.clear()
degp = bpy.context.evaluated_depsgraph_get()
bpy.ops.object.select_all(action='DESELECT')
emitter = bpy.data.objects[obj_name] # ensure emitter object is the active one
emitter.select_set(True)
# append handler into Blender particle system. This handler will be automatically run after each frame 
bpy.app.handlers.frame_change_post.append(particle_setter)
# Update to a frame where particles are updated (to ensure the handler is executed at least once)
