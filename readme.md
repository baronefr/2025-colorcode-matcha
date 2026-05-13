# public data for "Color code thresholds under circuit-level noise beyond the Pauli framework"

The workflow to generate the data shown in the paper is briefly described here:
- Matcha generates a circuit for the given code distance $d$, number of error correction cycles $C$ and physical error rate $p_{err}$. The circuit is generated in Stim format, but the emulator internally replaces the DEPOLARIZING instructions with the given noise model.
- The sampling is run in parallel on a cluster. Parallelism is at the level of samples: nodes run independently to generate the samples, which are then reduced to a single node. Data resulting from the decoding is finally aggregated in `experiments/` in form of csv.
- The plots are dumped into `img/`.

## circuits

The circuits that are passed to the Quantum Matcha Tea emulator are generated according to [Quantum 9, 1609 (2025)](https://doi.org/10.22331/q-2025-01-27-1609), which has published its code in [this repo](https://github.com/seokhyung-lee/color-code-stim). 
Given that the authors have been atively developing their code after publication, we have dumped the version that we have used as entrypoint in `src/color_code_stim.py`.

## plots

To recreate the plots of Figures 3-5, run `make-plots.sh`.

The twirling data coming from Stim simulation for a twirled noise physical rate is saved in `experiments/twirl/`.
The data is plotted through `plt_twirl.py`, which fetches the corresponding data from the Matcha experiments and recreates Figure 5 of the paper.
