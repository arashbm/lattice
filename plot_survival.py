import fileinput

import numpy as np
import matplotlib.pyplot as plt

selected_dim = 1
p_crit = 0.644701

beta = 0.276486
v_para = 1.733847
v_perp = 1.096854
beta_p = beta
z = v_para/v_perp
alpha = beta_p/v_para

t_max = 1024

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


survival_fig, survival_ax = plt.subplots()
scaled_survival_fig, scaled_survival_ax = plt.subplots()

for s in sizes:
    ts = np.arange(1, t_max+1)
    lts = np.array(sizes[s][p_crit]["lt"])
    p_surv = np.array([np.count_nonzero(lts >= t) for t in ts])/lts.shape[0]

    survival_ax.plot(ts, p_surv, label=f"N={s} p={p_crit}")
    scaled_survival_ax.plot(
            ts/s**(z/(selected_dim)),
            (ts**alpha)*p_surv,
            label=f"N={s} p={p_crit}")

survival_ax.plot(ts, ts**-alpha, label="$t^{-\\alpha}$", ls='--')
survival_ax.set_xlabel("$t$")
survival_ax.set_ylabel("$P(t)$")
survival_ax.set_xscale("log")
survival_ax.set_yscale("log")
survival_ax.legend()
survival_fig.savefig("figures/survival.pdf")

scaled_survival_ax.set_xlabel("$t/N^{z/d}$")
scaled_survival_ax.set_ylabel("$t^{\\alpha} P(t)$")
scaled_survival_ax.set_xscale("log")
scaled_survival_ax.set_yscale("log")
scaled_survival_ax.set_ylim(1e-4, 4)
scaled_survival_ax.legend()
scaled_survival_fig.savefig("figures/scaled-survival.pdf")
