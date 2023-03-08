# EasyLOD Add-on for Blender

EasyLOD is a powerful Blender addon for game developers, allowing for easy creation of LOD (Level of Detail) groups with just a few clicks. It simplifies the process of optimizing game performance while maintaining visual quality, with flexible options for fine-tuning settings.

Native support for **Unity** LOD format
## Requirements

This add-on requires Blender 3.0.0 or newer.

## Tutorial:

## Installation

1. Download the `easy_lod.py` file.
2. In Blender, go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select the `easy_lod.py` file.
4. Enable the "EasyLOD" add-on.

## Usage

1. Select the meshes object you want to create LOD groups for.
2. In the `Tools` panel, navigate to the `Easy LOD` tab.
3. Adjust the settings for `Amount`, `Intensity`, and `Ratio` as desired.
4. Click the `Add` button to add the LOD group.
5. Use the `Visibility` slider to switch between LOD preview levels in the viewport.
6. When you are ready to export, Enter the file Path to export.
7. Click the `Export FBX` button to export the mesh with LODs.

## Settings

The `Easy LOD` tool contains the following settings:

- **Amount**: The number of LOD levels to create.
- **Intensity**: The strength of the decimation applied to each LOD level.
- **Ratio**: The ratio of triangles to remove at each LOD level.
- **Symmetry**: Whether to apply symmetry to the decimation.

**To apply new Settings:** Click `Remove` and then `Add` buttons.


## Exporting

1. Select object to export (support multi objects)
2. Fill file path input for the exported file. 
3. Click the `Export FBX` button to export the mesh with LODs.

## Author
This addon was created by Alon Rubin.
