import numpy as np
from IPython import embed
from copy import deepcopy as copy
import argparse

# .msh file format, for info http://www.mujoco.org/book/XMLreference.html#mesh
"""
    (int32)   nvertex
    (int32)   nnormal
    (int32)   ntexcoord
    (int32)   nface
    (float)   vertex_positions[3*nvertex]
    (float)   vertex_normals[3*nnormal]
    (float)   vertex_texcoords[2*ntexcoord]
    (int32)   face_vertex_indices[3*nface]
    """


def obj2msh(obj_path, msh_path):
    # load the obj file
    with open(obj_path, "r") as f:
        lines = f.readlines()

    # take out vertices, texture and face indices
    # for obj file refer https://en.wikipedia.org/wiki/Wavefront_.obj_file#File_format
    (
        vertex_positions,
        vertex_normals,
        vertex_texcoords,
        face_vertex_indices,
        face_text_indices,
    ) = (
        [],
        [],
        [],
        [],
        [],
    )

    vert_tex_dic = {}  # creat unique (vert,text) pairs
    msh_face_vert_indices = []  # face vert indices for msh file

    for line in lines:
        words = line[:-1].split(" ")
        words = [w for w in words if w != ""]
        if line[:2] == "vn":
            vertex_normals.append([float(w) for w in words[1:]])
        elif line[:2] == "vt":
            vertex_texcoords.append([float(w) for w in words[1:]])
        elif line[0] == "v":
            vertex_positions.append([float(w) for w in words[1:]])
        elif line[0] == "f":
            # can handle non triangluar faces as well
            for i in range(len(words) - 3):
                temp = []
                for w in [words[1], words[2 + i], words[3 + i]]:
                    v = int(w.split("/")[0])
                    t = int(w.split("/")[1])
                    if t == "":
                        raise Exception(
                            "Texture not defined for vertex, can only handle .obj files in whichi (vetex, texture) pair is defined"
                        )
                    if (v, t) not in vert_tex_dic:
                        face_vertex_indices.append(v)
                        face_text_indices.append(t)
                        vert_tex_dic.update({(v, t): len(face_text_indices) - 1})

                    temp.append(vert_tex_dic[(v, t)])

                msh_face_vert_indices.append(copy(temp))

    # create vert and texture data for msh file
    msh_vertex_positions = [vertex_positions[i - 1] for i in face_vertex_indices]
    # obj consider origin at top left, while msh assumes origin on bottom left
    msh_vertex_texcoords = [
        [vertex_texcoords[i - 1][0], 1.0 - vertex_texcoords[i - 1][1]] for i in face_text_indices
    ]

    # dump data to msh file
    with open(msh_path, "wb") as f:
        # write nvertex
        f.write(np.int32(len(msh_vertex_positions)))

        # write nnormal (mujoco is able to capculate on its own)
        f.write(np.int32(0))

        # write ntextcoord
        f.write(np.int32(len(msh_vertex_texcoords)))

        # write nface
        f.write(np.int32(len(msh_face_vert_indices)))

        # vertext position
        for vertex_position in msh_vertex_positions:
            for v in vertex_position:
                f.write(np.float32(v))

        # vertext texcoords
        for vertex_texcoord in msh_vertex_texcoords:
            for vt in vertex_texcoord:
                f.write(np.float32(vt))

        # face_vertex_indices
        for face_vertex_indice in msh_face_vert_indices:
            for vf in face_vertex_indice:
                f.write(np.int32(vf))

    print("Stored msh file at '{}'".format(msh_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for obj to msh file conversion")
    parser.add_argument("--obj-path", type=str, help="path to obj file")
    parser.add_argument("--msh-path", type=str, default=None, help="path to the save msh file")
    args = parser.parse_args()
    if args.msh_path is None:
        args.msh_path = args.obj_path[:-3]+'msh'
    obj2msh(args.obj_path, args.msh_path)