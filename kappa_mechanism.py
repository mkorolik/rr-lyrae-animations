import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import scipy as sp

import matplotlib.patches as mpatch
from matplotlib.gridspec import GridSpec

from IPython.display import HTML
from matplotlib.animation import FuncAnimation

colors = ['#264653', '#287271', '#2A9D8F','#E9C46A', '#F4A261', '#E76F51']


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
                      'xtick.direction': 'in',
                      'ytick.direction': 'in',
                      'mathtext.fontset': 'custom',
                      'mathtext.rm': 'Serif',
                      'mathtext.it': 'Serif:italic',
                      'mathtext.bf': 'Serif:bold',
                      'hatch.color' : colors[0]
                    })

class model:
    def __init__(self, logs_dir='LOGS'):
        self.logs_dir = logs_dir

        self.DF = pd.read_table(os.path.join(self.logs_dir, 'history.data'), skiprows=5, sep=r'\s+')
        self.index = pd.read_table(os.path.join(self.logs_dir, 'profiles.index'), names=['model_number', 'priority', 'profile_number'], skiprows=1, sep=r'\s+')
        
        def load_profile(prof_num):
            return pd.read_table(os.path.join(self.logs_dir, 'profile' + str(prof_num) + '.data'), skiprows=5, sep=r'\s+')
        
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            self.profs = list(tqdm(executor.map(load_profile, self.index.profile_number),
                                   total=len(self.index.profile_number), desc='Loading Profiles: '))

star = model('LOGS')

teff = 10**star.DF.log_Teff
minima = teff.iloc[sp.signal.argrelmin(teff.values, order=100)]
len_phase = int(minima.index[1] - minima.index[0])

fig = plt.figure(figsize=(12, 6))

gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])


# Light Curve Plot (Unchanging):
ax=ax2
ax.plot(star.DF.day - star.DF.iloc[0].day, 10**star.DF.log_L, color='black')

ax.set_ylim(min(10**star.DF.log_L)-5, max(10**star.DF.log_L)+5)
ax.set_xlim(0, 1.365)
ax.set_yticks([40, 50, 60, 70])
ax.set_xlabel('Time [day]')
ax.set_ylabel(r'Luminosity [L$_\odot$]')

a2 = ax.scatter([], [])


# HR Diagram (Unchanging):
ax=ax3
ax.plot(10**star.DF.log_Teff, 10**star.DF.log_L, color='black', lw=2)

ax.invert_xaxis()
ax.set_ylim(35, 75)
ax.set_yticks([40, 50, 60, 70])
ax.set_ylabel(r'Luminosity [L$_\odot$]')
ax.set_xlabel('Effective Temperature [K]')

a3 = ax.scatter([], [])



def update_plot(idx):
    global a2, a3

    # Work Integrals + Opacity:
    ax=ax1
    ax.clear()
    prof = star.profs[idx]

    grad = np.gradient(prof['free_e'], prof.logT)

    ax.fill_between(10**prof.logR, -10, 10, where=grad>0.1, color=colors[1], alpha=0.2)
    ax.fill_between(10**prof.logR, -10, 10, where=prof.mixing_type>0, alpha=0, hatch='/')

    ax.plot(10**prof.logR, prof.opacity/max(prof.opacity), color=colors[5], lw=2, linestyle='dashed')
    ax.plot(10**prof.logR, prof.w/max(prof.w), color=colors[4], lw=3)

    ax.axvline(max(10**prof.logR), color=colors[3], lw=10)

    ax.set_ylim(0, 1)
    ax.set_xlim(5, 6.5)
    ax.set_xticks([5.2, 5.6, 6, 6.4])
    ax.set_xlabel(r'Radius [R$_\odot$]')
    ax.set_ylabel('Normalized Quantities')

    ax.legend(handles=[mpatch.Patch(color=colors[5], label='Opacity'), mpatch.Patch(color=colors[4], label='Work'), 
                       mpatch.Patch(color=colors[1], alpha=0.2, label='Ionization'), mpatch.Patch(alpha=0, hatch='//', label='Convection')],
            frameon=False, fontsize=12, loc='upper left')

    # Light Curve:
    ax=ax2
    a2.remove()
    a2 = ax.scatter(star.DF.iloc[idx*5].day - star.DF.iloc[0].day, 10**star.DF.iloc[idx*5].log_L, color='red', zorder=100)


    # HR Diagram:
    ax=ax3
    a3.remove()
    a3 = ax.scatter(10**star.DF.iloc[idx*5].log_Teff, 10**star.DF.iloc[idx*5].log_L, color='red', zorder=100)

    fig.tight_layout()



frames = np.arange(0, len_phase)

anim = FuncAnimation(fig, update_plot, frames=tqdm(frames), repeat=True)

# To display inline in a Jupyter notebook:
# HTML(anim.to_jshtml())

anim.save('rr lyrae opacity and work.gif', dpi=300, fps=30)
