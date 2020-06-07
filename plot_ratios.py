import fileinput

import numpy as np
import matplotlib.pyplot as plt

selected_dim = 1
p_crit = 0.644701

sizes = {}
for line in fileinput.input():
    pc, dims, seed, size, mass, lt, volume = \
            [float(i.strip()) for i in line.split()]

    if dims == selected_dim:
        nodes = int(size**dims)
        if nodes not in sizes:
            sizes[nodes] = {}
        if pc not in sizes[nodes]:
            sizes[nodes][pc] = {"mass": [], "lt": [], "volume": []}

        sizes[nodes][pc]["mass"].append(int(mass))
        sizes[nodes][pc]["volume"].append(int(volume))
        sizes[nodes][pc]["lt"].append(int(lt))


mass_fig, mass_ax = plt.subplots()
lt_fig, lt_ax = plt.subplots()
volume_fig, volume_ax = plt.subplots()

n = [(size, size//2) for size in sizes if size//2 in sizes]
for s1, s2 in n:
    pcs = sorted(set(sizes[s1]) & set(sizes[s2]))
    mass_ax.plot(pcs,
            [np.mean(sizes[s1][pc]["mass"])/np.mean(sizes[s2][pc]["mass"])
                for pc in pcs],
            label=f"N={s1}")
    lt_ax.plot(pcs,
            [np.mean(sizes[s1][pc]["lt"])/np.mean(sizes[s2][pc]["lt"])
                for pc in pcs],
            label=f"N={s1}")
    volume_ax.plot(pcs,
            [np.mean(sizes[s1][pc]["volume"])/np.mean(sizes[s2][pc]["volume"])
                for pc in pcs],
            label=f"N={s1}")

mass_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
mass_ax.set_yscale("log")
mass_ax.legend()
mass_fig.savefig("figures/ratios-mass.pdf")

lt_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
lt_ax.set_yscale("log")
lt_ax.legend()
lt_fig.savefig("figures/ratios-lt.pdf")

volume_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
volume_ax.set_yscale("log")
volume_ax.legend()
volume_fig.savefig("figures/ratios-volume.pdf")
