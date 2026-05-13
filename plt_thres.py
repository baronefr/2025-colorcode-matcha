# %%

import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set style for plots
#plt.style.use('./plt.mplstyle')

PREFIX = 'circlevel'
STUDY_CASE = sys.argv[1] if len(sys.argv) > 1 else None

save_plots = True
PLOT_DIR = "img/"


# %%

# configuration file of matcha simulation

X_CORR_FACTOR = 1.0

if STUDY_CASE == 'ampd-dc':
    p_err = [ 5e-4, 6e-4, 7e-4, 8e-4, 9e-4, 1e-3, 1.5e-3, 2e-3, 3e-3, 4e-3, 5e-3, 6e-3, 7e-3, 8e-3, 9e-3, 1e-2, 2e-2, 3e-2, ]

    X_CORR_FACTOR = 2.0 # trajectories in this version of Quantum Matcha omit the 1/2 factor in the effective operator, here we correct this

    BACKEND = 'TTN'
    DIR = f'matchasim/ampd_{BACKEND}_compiled/'

    PLT_XLABEL = r'damping rate ($\gamma$)'

    DATASET = [
        {'distances':[3], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':3},
        {'distances':[5], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':5},
    ]

elif STUDY_CASE == 'ampd-1c':
    p_err = [ 7e-3, 8e-3, 9e-3, 1e-2, 1.25e-2, 1.5e-2, 1.75e-2, 2e-2, 2.25e-2, 2.5e-2, 2.75e-2, 3e-2, 3.25e-2, 3.5e-2, 3.75e-2,4e-2, 5e-2, 6e-2]

    X_CORR_FACTOR = 2.0 # trajectories in this version of Quantum Matcha omit the 1/2 factor in the effective operator, here we correct this

    BACKEND = 'TTN'
    DIR = f'matchasim/ampd_{BACKEND}_compiled/'

    PLT_XLABEL = r'damping rate ($\gamma$)'

    DATASET = [
        {'distances':[3], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':1},
        {'distances':[5], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':1},
        {'distances':[7], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':1},
    ]

elif STUDY_CASE == 'srx-dc':
    p_err = [0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.0125, 0.015, 0.02, 0.03, 0.04, 0.05, ]

    BACKEND = 'TTN'
    DIR = f'matchasim/srx_{BACKEND}_compiled/'

    PLT_XLABEL = r'systematic rotation angle ($\theta/\pi$)'

    DATASET = [
        {'distances':[3], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':3},
        {'distances':[5], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':5},
    ]

elif STUDY_CASE == 'srx-1c':
    p_err = [0.007, 0.008, 0.009, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.04,0.05,0.06,0.07,0.08,0.09,0.10]
    
    BACKEND = 'TTN'
    DIR = f'matchasim/srx_{BACKEND}_compiled/'

    PLT_XLABEL = r'systematic rotation angle ($\theta/\pi$)'

    DATASET = [
        {'distances':[3], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':1},
        {'distances':[5], 'p_err':p_err, 'bond_dims':[1024], 'repetitions':1},
        {'distances':[7], 'p_err':p_err, 'bond_dims':[256], 'repetitions':1},
    ]

else:
    raise ValueError(f"unknown study case {STUDY_CASE}")



# %%

PLOT_TITLE_LEFT = None
PLOT_TITLE_RIGHT = None
if 'srx' in STUDY_CASE:
    PLOT_TITLE_LEFT = 'SRX'
elif 'ampd' in STUDY_CASE:
    PLOT_TITLE_LEFT = 'AD'

def get_file(prefix, target, d, p_err, repetitions, bd):
    return DIR + f"{prefix}_{d}_{p_err:.2e}_{repetitions}_{bd}.{target}.csv"

print(f'loaded params for {STUDY_CASE}')

# %%

df = pd.read_csv(f"experiments/{STUDY_CASE}.csv")
distances = df['d'].unique()

# recap
print(df[['d','max_bd','repetitions','p_err']])

# %% plot raw data

markers = ['o', '^', 's', 'D', 'X', 'P', '<', '>']
for ii, dd in enumerate(distances):
    tmp = df[ df['d'] == dd ]
    plt.plot(tmp['p_err'], tmp['p_fail'],
        label='$d='+f'{dd}$', marker=markers[ii],
        zorder=10-ii,
    )
    plt.fill_between(tmp['p_err'], tmp['p_fail']-tmp['delta_p_fail'], tmp['p_fail']+tmp['delta_p_fail'], alpha=0.1)
plt.ylabel(r'$p_{\mathrm{fail}}$')
plt.xlabel(PLT_XLABEL)
plt.yscale('log')
plt.xscale('log')
plt.title(PLOT_TITLE_LEFT, loc='left')
plt.tight_layout()
plt.legend()
if save_plots:
    plt.savefig(PLOT_DIR + f"thres_{STUDY_CASE}_{BACKEND}_raw.pdf")
