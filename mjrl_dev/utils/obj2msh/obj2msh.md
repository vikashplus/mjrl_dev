# .obj to .msh converstion

## .obj files format [reference](https://en.wikipedia.org/wiki/Wavefront_.obj_file#File_format)
* has unique vertices
* has unique texture cordinate
* vetices to texture mapping is defined in face vertices

## .msh file format [reference](http://www.mujoco.org/book/XMLreference.html#mesh)
* vertices (can have duplicate copies of vertices)
* texture (texture mapping for corresponding vertices eg. for vertices[y] texture[y] will be used)
* face vertex indices, will define the indices of vertices used for building tringular face
* normal, can be calculated pretty well by mujoco itself

Note: for `obj` assume origin at top left corner while `msh` file assumes origin to be at the bottom left corner

## How to use it
* convert obj to msh file

`
python obj_to_msh.py --obj-path path_to_obj_file --msh-path path_to_store_msh_file
`

* visualize in mujoco using xml file

```
<mujoco>
    <asset>
        <texture name="texplane" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 0.15 0.2"
            width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>
        <material name="matplane" reflectance="0.3" texture="texplane" texrepeat="1 1" texuniform="true"/>

        <!-- load texture and mjl  -->
        <texture name="textobj" type="2d" file="path_to_texture"/>
        <mesh name="meshobj" file="path_to_msh_file"/>

        <material name="matobj" texture="textobj"/>
    </asset>

    <worldbody>
        <light directional="true" diffuse=".4 .4 .4" specular="0.1 0.1 0.1" pos="0 0 5.0" dir="0 0 -1" castshadow="false"/>
        <light directional="true" diffuse=".6 .6 .6" specular="0.2 0.2 0.2" pos="0 0 4" dir="0 0 -1"/>

        <geom name="ground" type="plane" size="0 0 1" pos="0 0 0" quat="1 0 0 0" material="matplane" condim="1"/>
        <body mocap="true" pos="0.0 0.0 0.1">
            <geom type="mesh" mesh="meshobj" size=".1 .1" material="matobj" group="1" condim="1"/>
        </body>
    </worldbody>
</mujoco>
```
