import fileinput

import numpy as np
import matplotlib.pyplot as plt

selected_dim = 1
p_crit = 0.644701

beta = 0.276486
v_para = 1.733847
v_perp = 1.096854
beta_p = beta
gamma = v_para + selected_dim*v_perp - beta - beta_p
tau = v_para - beta_p
nu = selected_dim*v_perp- beta_p

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
scaled_mass_fig, scaled_mass_ax = plt.subplots()

lt_fig, lt_ax = plt.subplots()
scaled_lt_fig, scaled_lt_ax = plt.subplots()

volume_fig, volume_ax = plt.subplots()
scaled_volume_fig, scaled_volume_ax = plt.subplots()

for s in sizes:
    pcs = np.array(sorted(sizes[s]))
    masses = np.array([np.mean(sizes[s][pc]["mass"]) for pc in pcs])
    lts = np.array([np.mean(sizes[s][pc]["lt"]) for pc in pcs])
    volumes = np.array([np.mean(sizes[s][pc]["volume"]) for pc in pcs])

    mass_ax.plot(pcs, masses, label=f"N={s}")
    scaled_mass_ax.plot(
            (pcs - p_crit)*s**(1/(selected_dim*v_perp)),
            (s**(gamma/(selected_dim*v_perp)))*masses,
            label=f"N={s}")

    lt_ax.plot(pcs, lts, label=f"N={s}")
    scaled_lt_ax.plot(
            (pcs - p_crit)*s**(1/(selected_dim*v_perp)),
            (s**(tau/(selected_dim*v_perp)))*lts,
            label=f"N={s}")

    volume_ax.plot(pcs, volumes, label=f"N={s}")
    scaled_volume_ax.plot(
            (pcs - p_crit)*s**(1/(selected_dim*v_perp)),
            (s**(nu/(selected_dim*v_perp)))*volumes,
            label=f"N={s}")

mass_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
mass_ax.set_xlabel("$p$")
mass_ax.set_ylabel("$M$")
mass_ax.set_yscale("log")
mass_ax.legend()
mass_fig.savefig("figures/mean-mass.pdf")

scaled_mass_ax.axvline(0, label=f"$p_c={p_crit}$", ls='--')
scaled_mass_ax.set_xlabel("$N^{1/{d v_\\perp}} (p-p_c)$")
scaled_mass_ax.set_ylabel("$N^{\\gamma/{d v_\\perp}} M$")
scaled_mass_ax.set_yscale("log")
scaled_mass_ax.legend()
scaled_mass_fig.savefig("figures/scaled-mean-mass.pdf")

lt_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
lt_ax.set_xlabel("$p$")
lt_ax.set_ylabel("$T$")
lt_ax.set_yscale("log")
lt_ax.legend()
lt_fig.savefig("figures/mean-lt.pdf")

scaled_lt_ax.axvline(0, label=f"$p_c={p_crit}$", ls='--')
scaled_lt_ax.set_xlabel("$N^{1/{d v_\\perp}} (p-p_c)$")
scaled_lt_ax.set_ylabel("$N^{\\tau/{d v_\\perp}} T$")
scaled_lt_ax.set_yscale("log")
scaled_lt_ax.legend()
scaled_lt_fig.savefig("figures/scaled-mean-lt.pdf")

volume_ax.axvline(p_crit, label=f"$p_c={p_crit}$", ls='--')
volume_ax.set_xlabel("$p$")
volume_ax.set_ylabel("$V$")
volume_ax.set_yscale("log")
volume_ax.legend()
volume_fig.savefig("figures/mean-volume.pdf")

scaled_volume_ax.axvline(0, label=f"$p_c={p_crit}$", ls='--')
scaled_volume_ax.set_xlabel("$N^{1/{d v_\\perp}} (p-p_c)$")
scaled_volume_ax.set_ylabel("$N^{\\nu/{d v_\\perp}} V$")
scaled_volume_ax.set_yscale("log")
scaled_volume_ax.legend()
scaled_volume_fig.savefig("figures/scaled-mean-volume.pdf")
