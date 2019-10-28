import numpy as np
from pymatgen.ext.matproj import MPRester

def activation_fn(x):
    return np.tanh(x)

def get_struct_from_mp(mp_id):
    with MPRester("81u7uwUvNq2vwGJH9") as m:
        structure = m.get_structure_by_material_id(mp_id)
    return structure

def extract_descrpt(structure, n_local = 52, rcut = 6.0, rcut_smth = 5.8):
    n_atoms = len(structure)
    descpts = np.zeros([n_atoms, 4 * n_local])
    for i, site in enumerate(structure):
        neighborlist = structure.get_neighbors(site, rcut)
        assert n_local >= len(neighborlist), "increase number of neighbor atoms for local environment calculation or decrease cutoff radius"
        neighborlist.sort(key = lambda neighbor: neighbor[1])
        coords = site.coords
        for j, neighbor in enumerate(neighborlist):
            dist = neighbor[1]
            idx_start = j * 4
            if dist < rcut_smth:
                descpts[i, idx_start] = 1 / dist
            else:
                # smooth function for atoms with distance within the shell [rcut_smth, rcut]
                descpts[i, idx_start] = 1 / dist * (0.5 * np.cos((dist - rcut_smth) / (rcut - dist) * np.pi) + 0.5)
            xji, yji, zji = neighbor[0].coords - coords
            descpts[i, idx_start + 1] = descpts[i, idx_start] * xji / dist
            descpts[i, idx_start + 2] = descpts[i, idx_start] * yji / dist
            descpts[i, idx_start + 3] = descpts[i, idx_start] * zji / dist
    # load descriptors of bulk silicon as reference
    ref = np.load(r"/home/ubuntu/ref.npy")
    # parameters for local embedded network
    seed = 1
    stddev = 1.0
    n_neuron = [1, 40, 80]
    n_g2 = 4
    xyz_scatter = descpts.reshape(-1, 4)[:,0].reshape(-1, 1)
    xyz_scatter_total = []
    
    for ii in range(1, 3):
        np.random.seed(seed)
        w = np.random.normal(0.0, stddev / np.sqrt(n_neuron[ii] + n_neuron[ii - 1]), (n_neuron[ii - 1], n_neuron[ii]))
        np.random.seed(seed)
        b = np.random.normal(0.0, stddev, (1, n_neuron[ii]))
        if n_neuron[ii] == n_neuron[ii - 1]:
            xyz_scatter += activation_fn(np.matmul(xyz_scatter, w) + b)
        elif n_neuron[ii] == n_neuron[ii - 1] * 2:
            xyz_scatter = np.concatenate((xyz_scatter, xyz_scatter), axis=1) + activation_fn(np.matmul(xyz_scatter, w) + b)
        else:
            xyz_scatter = activation_fn(np.matmul(xyz_scatter, w) + b)
    xyz_scatter = xyz_scatter.reshape(-1, n_local, n_neuron[-1])

    descpts_reshape = descpts.reshape(-1, n_local, 4)
    
    xyz_scatter_1 = np.matmul(np.transpose(descpts_reshape, (0, 2, 1)), xyz_scatter)
    xyz_scatter_1 /= n_local

    xyz_scatter_2 = xyz_scatter_1[:, :, :n_g2]
    
    result = np.matmul(np.transpose(xyz_scatter_1, (0, 2, 1)), xyz_scatter_2)
    result = np.reshape(result, (-1, n_g2 * n_neuron[-1]))
    
    distance = result - ref
    distance_2 = np.square(distance)
    return np.sum(distance_2, axis=1)
