# VXMotion - Blender

VXMotion is a comprehensive toolset tailored for the creation, manipulation, and export of vertex animation textures. 
Designed to be highly versatile, it offers seamless integration between Blender and prominent game engines such as 
Unreal, Unity, and Godot.

This Addon allows you to bake and export Non-Alembic, Skinless animations from different animation workflows:

- Skinned Meshes
- Blend Shapes
- Deformer Modifiers
- Rigid Body Simulations
- Soft Body Simulations
- Cloth Simulations
- Fluid Simulations (Smoke, Fire and Liquid)
- Geometry Nodes
- And (Hopefully) Much More...

## How It Works

The majority of the game engines have a standard for only one type of animation: **Skinned Mesh Animations** This is a
great tool for a lot of applications in the game development workflow but is surprisingly limited when it comes to
variable topology or more complex and dynamic mesh deformations. This of course comes from the fact that Game developers always must
have an eye on performance, so complex soft body physics or fluid simulations are more often than not, not an option for
a game.

What a vertex animation texture does is Store all the position, normal and tangent data from the vertices of a mesh each frame in
pixels, given that the RGB channels can be encoded to XYZ coordinates, the translation can be done pretty much directly.
Once The data is stored in the necessary textures, a vertex shader can decode and apply this information as vertex offsets
for each vertex in a base mesh, making the runtime cost of such complex animations just a very small fraction of what it
would take to simulate something like a water splash or a Smoke puff.

## Usage Guide

TODO: Usage guide once UI is done

## Documentation


