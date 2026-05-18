import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os
import matplotlib.patches as mpatch
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
from matplotlib.gridspec import GridSpec

import lightkurve as lk

plt.rcParams.update({'axes.linewidth' : 1,
                     'ytick.major.width' : 1,
                     'ytick.minor.width' : 1,
                     'xtick.major.width' : 1,
                     'xtick.minor.width' : 1,
                     'xtick.labelsize': 10, 
                     'ytick.labelsize': 10,
                     'axes.labelsize': 12,
                     'font.family': 'Serif',
                      'figure.figsize': (6.4, 4.8),
                      # 'figure.figsize': (4, 3.8),
                      'xtick.direction': 'in',
                      'ytick.direction': 'in',
                      'mathtext.fontset': 'custom',
                      'mathtext.rm': 'Serif',
                      'mathtext.it': 'Serif:italic',
                      'mathtext.bf': 'Serif:bold'
                    })

colors = ['#264653', '#287271', '#2A9D8F','#E9C46A', '#F4A261', '#E76F51']
lightpurple = '#d0c9dd'
darkpurple = '#85789c'


# Find a lightcurve that looks "neat", isolate one Blazhko cycle by eye
search = lk.search_lightcurve('RR Lyr')
lc = search[1].download().normalize()
idx_min = 900
idx_max = 2800

period = lc.to_periodogram().period_at_max_power.value
b_period = lc.time.value[idx_max] - lc.time.value[idx_min]

x = lc.time.value[idx_min:idx_max]
y = lc.flux.value[idx_min:idx_max]
 
t0 = lc.time.value[idx_min]
phase       = ((x - t0) / period)   % 1
b_phase     = ((x - t0) / b_period) % 1
b_cycle     = ((x - t0) / b_period).astype(int)
cycle_number = np.floor((x - t0) / period).astype(int)
cycle = ((x - t0) / period).astype(int)

n_cycles = max(cycle_number)

# Insert your preferred colors here
cmap = plt.get_cmap('viridis', n_cycles)
colora = colors[2]
colorb = colors[5]


# ── figure layout ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 6))
 
gs = GridSpec(1, 2, figure=fig)
 
ax3d = fig.add_subplot(gs[1], projection='3d')
ax2d = fig.add_subplot(gs[0])
 
# ── 3D base plot (static) ───────────────────────────────────────────────────── 
for i in tqdm(range(0, max(cycle_number))):
    mask = cycle == i
    ax3d.scatter(phase[mask], x[mask] - t0, y[mask],
                 s=1,
                 color=cmap(i / n_cycles),
                 alpha=1)
 
ax3d.set_yticks([0, 10, 20, 30, 40])
ax3d.set_xlabel('Pulsation Phase', labelpad=10)
ax3d.set_ylabel('Time [day]',      labelpad=10)
ax3d.set_zlabel('Normalized Flux', rotation=90, labelpad=5)
ax3d.set_xlim(0, 1)
ax3d.view_init(elev=10, azim=-45, roll=0)
ax3d.set_rasterized(True)
ax3d.set_box_aspect(None, zoom=1)
 
# Placeholder for the highlight scatter on the 3D plot
highlight_3d = ax3d.scatter([], [], [], s=0)   # empty to start
 
# ── 2D base plot (static background) ─────────────────────────────────────────
# ax2d.patch.set_alpha(0.0)
 
ax2d.scatter(phase - 1, y, s=1, color=colora)
ax2d.scatter(phase,     y, s=1, color=colora)
ax2d.scatter(phase + 1, y, s=1, color=colora)
 
ax2d.set_xlim(-1, 1)
ax2d.set_xlabel('Phase')
ax2d.set_ylabel('Normalized Flux')
 
p1 = ax2d.scatter([], [])
p2 = ax2d.scatter([], [])
p3 = ax2d.scatter([], [])
 
n = 5   # cycles per window
 
# ── animation update ──────────────────────────────────────────────────────────
def update(idx):
    global p1, p2, p3, highlight_3d
 
    # ---- 2D highlight --------------------------------------------------------
    p1.remove()
    p2.remove()
    p3.remove()
 
    mask2d = (cycle_number >= idx) & (cycle_number < idx + n)
 
    p1 = ax2d.scatter(phase[mask2d],     y[mask2d], s=10, color=colorb)
    p2 = ax2d.scatter(phase[mask2d] - 1, y[mask2d], s=10, color=colorb)
    p3 = ax2d.scatter(phase[mask2d] + 1, y[mask2d], s=10, color=colorb)
 
    # ---- 3D highlight --------------------------------------------------------
    highlight_3d.remove()
    # if mask2d.any():
    highlight_3d = ax3d.scatter(
        phase[mask2d],
        (x - t0)[mask2d],      
        y[mask2d],
        s=50,
        color=colorb,      
        edgecolors='white',
        linewidths=0.4,
        alpha=1,
        zorder=10,
    )
 
    return p1, p2, p3, highlight_3d

fig.tight_layout()

frames = np.arange(0, int(max(cycle_number)), n)

anim = FuncAnimation(fig, update, frames=tqdm(frames), repeat=True)

# For showing within a Jupyter notebook:
# HTML(anim.to_jshtml())

pbar = tqdm(total=n)
anim.save('blazhko rr lyrae 2d3d.gif', dpi=300, fps=10, progress_callback=lambda i, n: pbar.update(1))

