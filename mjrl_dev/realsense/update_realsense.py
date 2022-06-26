from mujoco_py import load_model_from_path, MjSim,  MjViewer, functions
import numpy as np
import time
from mujoco_py.modder import TextureModder
import pickle
from PIL import Image


height_field_range = (.1, .5)

model_path = 'realsense.xml'
rs_data = pickle.load(open('realsense_rgbd.pkl', 'rb'))

model = load_model_from_path(model_path)
sim = MjSim(model)
viewer = MjViewer(sim)
height_field_dim = (int(sim.model.hfield_ncol), int(sim.model.hfield_nrow))

# modder = TextureModder(sim)

t0 = time.time()

# while True:
for iter in range(100*len(rs_data['rgbd'])):

    # Height Field ==========================
    # Programatically generated height field
    # tnow = 0.01*(time.time()-t0)
    # for i in range(height_field_dim[0]):
    #     for j in range(height_field_dim[1]):
    #         hf[i, j] = 0.2*np.sin(tnow*i+np.cos(np.pi-tnow*j))

    # Randomly generated height field
    # sim.model.hfield_data[:] = np.random.uniform(*height_field_range, size=np.shape(sim.model.hfield_data))

    # Read depth from real sense data
    iframe = iter%100
    depth = rs_data['rgbd'][iframe][0,::2,::2,3].flatten()/2000
    depth[depth==0] = 4
    sim.model.hfield_data[:] = 4-depth

    # Upload height field data to GPU
    functions.mjr_uploadHField(sim.model, sim.render_contexts[0].con, 0)


    # Texture  ==========================

    # Random textures
    # for name in sim.model.geom_names:
        # modder.rand_all(name)
    # modder.rand_all('hfield1')

    # Read texture from real sense data
    rgb = rs_data['rgbd'][iframe][0,::-1,:,:3]
    tex_adr = sim.model.tex_adr[-1]
    sim.model.tex_rgb[tex_adr:] = rgb.astype('uint8').flatten()

    # save the images if need be to view
    # image = Image.fromarray(rgb, 'RGB')
    # image.save(str(iframe)+".jpeg")

    # Upload texture data to GPU
    functions.mjr_uploadTexture(sim.model, sim.render_contexts[0].con, 2)

    sim.step()
    viewer.render()