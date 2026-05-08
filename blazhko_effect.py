import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
=
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

plt.rcParams.update({'axes.linewidth' : 1,
                     'ytick.major.width' : 1,
                     'ytick.minor.width' : 1,
                     'xtick.major.width' : 1,
                     'xtick.minor.width' : 1,
                     'xtick.labelsize': 10, 
                     'ytick.labelsize': 10,
                     'axes.labelsize': 12,
                     'font.family': 'Serif',
                      'xtick.direction': 'in',
                      'ytick.direction': 'in',
                      'mathtext.fontset': 'custom',
                      'mathtext.rm': 'Serif',
                      'mathtext.it': 'Serif:italic',
                      'mathtext.bf': 'Serif:bold'
                    })

color1 = '#d0c9dd'
color2 = '#85789c'

# Insert any dataset you want, as long as you know the pulsation (fundamental) period and roughly the Blazhko period:
data = pd.read_table('OGLE-BLG-RRLYR-09193.dat.txt', sep=r'\s+', header=None, names=['date', 'mag', 'err'])
period = 0.52181455
b_period = 155

t0 = data.date[0]
phase = ((data.date - t0) / period) % 1
b_phase = ((data.date - t0) / b_period) % 1

fig = plt.figure(figsize=(8, 6))
ax = fig.gca()

ax.scatter(phase-1, data.mag, s=1, color=color1)
ax.scatter(phase, data.mag, s=1, color=color1)
ax.scatter(phase+1, data.mag, s=1, color=color1)

ax.invert_yaxis()
ax.set_xlim(-1, 1)
ax.set_xlabel('Phase')
ax.set_ylabel('I-Magnitude')

p1 = ax.scatter([], [])
p2 = ax.scatter([], [])
p3 = ax.scatter([], [])

max_idx = int((max(data.date)-min(data.date))/b_period)

def update_plot(idx):
    global p1, p2, p3
    p1.remove()
    p2.remove()
    p3.remove()

    b_lo = idx / max_idx
    b_hi = (idx + 1) / max_idx
    mask = (b_phase >= b_lo) & (b_phase < b_hi)
    
    p1 = ax.scatter(phase[mask], data.mag[mask], s=10, color=color2)
    p2 = ax.scatter(phase[mask]-1, data.mag[mask], s=10, color=color2)
    p3 = ax.scatter(phase[mask]+1, data.mag[mask], s=10, color=color2)

fig.tight_layout()

frames = np.arange(0, max_idx)

anim = FuncAnimation(fig, update_plot, frames=tqdm(frames), repeat=True)

# If in a Jupyter notebook, you can view the animation through:
# HTML(anim.to_jshtml())

anim.save('blazhko effect.gif', dpi=300, fps=15)
