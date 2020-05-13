# Isolated_Galaxy_Simulation
Isolated Galaxy Simulation using Blender 3D, Python YT

Blender is the free and open source 3D creation suite. It supports the entirety of the 3D pipeline—modeling, 
rigging, animation, simulation, rendering, compositing and motion tracking, video editing and 2D animation pipeline (www.blender.org).

yt is an open-source, permissively-licensed python package for analyzing and visualizing volumetric data (https://yt-project.org/).

Sample data for creating the Isolated Galaxy can be found here : https://yt-project.org/data/

The blend file includes a python script which needs to be manually run:

1) Loads volumetric data ENZO from file which can be found here https://yt-project.org/data/IsolatedGalaxy.tar.gz
   (Update path to this file in line 143 of the Blender script) 
2) Adds an Emitter object (single vert) with a Particle System to the scene
3) Adds an Instance Object with a material to the scene which will be used as the Particle System object
4) Adds a handler to the scene which will be run after each frame change (frame_change_post.append). 
   Each time this handler runs it puts a copy of the Instance Object (particle) at each location found in the ENZO file (approx. 76K).
   Unfortunately at each frame change the location of all particles is reset so the handler needs to them back in place for the render.

The script only needs to be run once to setup the scene above. As the Camara is animated you can then start the "Render Animation" which will create the image sequence used to create the Youtube video below.

As the script uses a few Python packages which are not part of Blender i installed Anaconda on my Windows 10 PC and appand a link (sys.path) to the   


