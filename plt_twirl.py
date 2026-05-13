# %%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set style for plots
#plt.style.use('./plt.mplstyle')

from src.stats import get_pfail

twirl_dir = f'experiments/twirl/' # twirl directory for STIM simulations
matcha_dir = f'experiments/'

distances = [ 3, 5, 7 ]
repetitions = 1

# %%

def get_twirl_data(noise_model, p_err, repetitions):
    twirl_file = f'{twirl_dir}{noise_model}_{repetitions}.twirl.csv'
    df_twirl = pd.read_csv(twirl_file, comment='#')
    df_twirl = df_twirl[df_twirl['pnoise'].isin(p_err)]

    # Calculate the average and standard deviation of the failure probability
    sum_failures = df_twirl['nfails']
    shots = df_twirl['nsamples']

    df_twirl['p_fail'], df_twirl['delta_p_fail'] = get_pfail(
        shots, sum_failures,
        alpha=0.01,
        confint_method='binom_test'
    )
    return df_twirl

def get_ttn_data(noise_model, p_err_matcha):
    df = pd.read_csv(matcha_dir + f"{noise_model}-{repetitions}c.csv")
    df = df[df['p_err'].isin(p_err_matcha)]
    return df


# %%

fig, axs = plt.subplots(1, 2, figsize=(6, 4))

# Data L
p_err = [ 1e-2 ] # 5e-3
p_err_matcha = p_err

df_twirl = get_twirl_data('srx', p_err, repetitions)
df = get_ttn_data('srx', p_err_matcha)

C1 = 'tab:blue'
C2 = 'tab:orange'

# Plot L
axs[0].plot(df_twirl['d'], df_twirl['p_fail'], 'o--', label='Pauli twirling', color=C1)
axs[0].fill_between(df_twirl['d'], df_twirl['p_fail']-df_twirl['delta_p_fail'], df_twirl['p_fail']+df_twirl['delta_p_fail'], alpha=0.1, color=C1)
axs[0].plot(df['d'], df['p_fail'], label='TTN', marker='s', color=C2)
axs[0].fill_between(df['d'], df['p_fail']-df['delta_p_fail'], df['p_fail']+df['delta_p_fail'], alpha=0.1, color=C2)

axs[0].set_xlabel('$d$')
axs[0].set_ylabel('$p_{\mathrm{fail}}$')
axs[0].set_yscale('log')
axs[0].set_xticks(distances)
axs[0].legend(fontsize=11, loc='upper right')
axs[0].set_title('SRX', family='sans-serif', loc='left')
axs[0].set_title(r'$\theta/\pi=1\%$', family='sans-serif', loc='right', fontsize=12)

# Data R

p_err = [ 4e-3 ]
p_err_matcha = p_err

df_twirl = get_twirl_data('ampd', p_err, repetitions)
df = get_ttn_data('ampd', p_err_matcha)

# Plot R
axs[1].plot(df_twirl['d'], df_twirl['p_fail'], 'o--', label='Pauli twirling', color=C1)
axs[1].fill_between(df_twirl['d'], df_twirl['p_fail']-df_twirl['delta_p_fail'], df_twirl['p_fail']+df_twirl['delta_p_fail'], alpha=0.1, color=C1)
axs[1].plot(df['d'], df['p_fail'], label='TTN', marker='s', color=C2)
axs[1].fill_between(df['d'], df['p_fail']-df['delta_p_fail'], df['p_fail']+df['delta_p_fail'], alpha=0.1, color=C2)

axs[1].set_xlabel('$d$')
#axs[1].set_ylabel('$p_{\mathrm{fail}}$')
axs[1].set_yscale('log')
axs[1].set_xticks(distances)
#axs[1].legend()
axs[1].set_title('AD', family='sans-serif', ha='left', loc='left')
axs[1].set_title(r'$\gamma = 0.4\%$', family='sans-serif', loc='right', fontsize=12)

plt.tight_layout()
plt.savefig('img/twirl_vs_ttn.pdf', bbox_inches='tight')

# %%
