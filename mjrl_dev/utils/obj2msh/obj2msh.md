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

## Convert obj to msh file

`
python obj_to_msh.py --obj-path path_to_obj_file --msh-path path_to_store_msh_file
`

## Examples
[Examples](examples) folder contains a few obj files, the converted .msh files, mujoco models using those files. The steps followed are outlined below -
1. `python obj_to_msh.py --obj-path examples/door_handle.obj --msh-path examples/door_handle.msh`
2. Load the generated `examples/door_handle.msh` into a mujoco model [examples/door_handle.xml](examples/door_handle.xml)
3. Visualize the model using `./mujoco200/bin/simulate PATH_TO_OBJ2MSH/door_handle.xml`
