import numpy as np
from matplotlib import pyplot as plt
# Custom imports:
from Synthetic_Sequencer import synthseq as seq, noisify as noise
from Burgess_Model import main as burg
from Post_Burgess import idealseq
from Visualization_Tools import profile_visualizers as pv, matrix_visualizers as mv


# Set filepath:
filepath = r'D:\AESB\AESB3\BEP\Figures\03 - Methodology'
# Define parasequence:
para_depths = [0, 6.5, 10, 12.5, 13.5, 15]
para_lithologies = ['SST', 'SHSST', 'SLT', 'SH', 'COAL']
colors = ['gold', 'goldenrod', 'chocolate', 'sienna', 'purple']
hatches = ['.', '.-', '-.-', '---', 'o.']
layout = {}
for i in range(len(para_lithologies)):
    layout[para_lithologies[i]] = [colors[i], hatches[i]]
# Define resolution and number of parasequences:
res = 0.2
n = 5

# Visualize the parasequence:
pv.parasequence_profile(para_depths, para_lithologies, layout, 1, filepath=filepath + '\Parasequence.png')

# Create asymmetric synthetic profile (no gamma noise):
depths, lithologies = seq.sequencer(para_depths, para_lithologies, layout, res, n, alpha=5, beta=0, psi=0.9, omega=0,
                                    asymmetric=True, filepath=filepath)

# # Create synthetic profile:
# x, y, derivatives, bounds, dictionaries = seq.sequencer(para_depths, para_lithologies, layout, res, n,
#                                                         alpha=5, beta=0, psi=0.9, omega=0, filepath=filepath)

# # Read back the profile (potentially with added gamma noise):
# depths, lithologies = noise.gaussian_noise(x, y, derivatives, bounds, dictionaries, layout, res, gamma=0,
#                                            filepath=filepath)

# Run through Burgess model:
result1, result2, result3 = burg.main(depths, lithologies, layout, res, n, filepath)
mv.matrix_imager(result1[0][1], para_lithologies, result1[2][1], layout, filepath=filepath + '\Bad Matrix.png',
                 title='Markov Order Metric m = ' + str(round(result1[1][1], 2)), cmap='Oranges')


# # Create ideal sequence:
# ideal_depths, ideal_lithologies = idealseq.ideal_sequencer(depths, lithologies, result3[0][0], result3[0][2],
#                                                            result3[0][3], layout, filepath)



# # Create Mu vs Psi plot:
# psi_vector = np.linspace(0, 1, 200)
# mu_1 = 50 - 50*psi_vector
# mu_2 = 50 + 50*psi_vector
# plt.plot(psi_vector, mu_1, linestyle='-.', color='maroon', lw=2, label=r'$\mu_{1}$')
# plt.text(0.5, 72, r'$\mu_2$', weight='bold', fontsize='large')
# plt.plot(psi_vector, mu_2, linestyle='--', color='maroon', lw=2, label=r'$\mu_{2}$')
# plt.text(0.5, 27, r'$\mu_1$', fontsize='large')
# plt.hlines(50, xmin=0, xmax=1, color='indianred', lw=1.8, linestyle='dotted')
# plt.text(0.9, 51, r'$\mu_{0}$', fontsize='large')
# plt.vlines(0.2, ymin=50-50*0.2, ymax=50+50*0.2, linestyle='--', color='black', lw=1.8)
# plt.vlines(0.4, ymin=50-50*0.4, ymax=50+50*0.4, linestyle='--', color='black', lw=1.8)
# plt.vlines(0.6, ymin=50-50*0.6, ymax=50+50*0.6, linestyle='--', color='black', lw=1.8)
# plt.vlines(0.8, ymin=50-50*0.8, ymax=50+50*0.8, linestyle='--', color='black', lw=1.8)
# plt.text(0.2 - 0.02, 40 - 4, r'$P_{40}^*$', weight='semibold', va='center')
# plt.text(0.2 - 0.02, 60 + 4, r'$P_{60}^*$', weight='semibold', va='center')
# plt.text(0.4 - 0.02, 30 - 4, r'$P_{30}^*$', weight='semibold', va='center')
# plt.text(0.4 - 0.02, 70 + 4, r'$P_{70}^*$', weight='semibold', va='center')
# plt.text(0.6 - 0.02, 20 - 4, r'$P_{20}^*$', weight='semibold', va='center')
# plt.text(0.6 - 0.02, 80 + 4, r'$P_{80}^*$', weight='semibold', va='center')
# plt.text(0.8 - 0.02, 10 - 4, r'$P_{10}^*$', weight='semibold', va='center')
# plt.text(0.8 - 0.02, 90 + 4, r'$P_{90}^*$', weight='semibold', va='center')
# plt.xlim(0, 1)
# plt.ylim(0, 100)
# plt.xticks(np.arange(0, 1.1, 0.1))
# plt.yticks(np.arange(0, 110, 10))
# plt.xlabel(r'$\psi$ [-]')
# plt.ylabel(r'$n$th shifted percentile [-]')
# plt.title(r'Compensational Stacking: $\psi$ vs $\mu_{1}$, $\mu_{2}$', weight='semibold')
# plt.savefig(filepath + '\Psi vs Mu plot.png', bbox_inches='tight')
# plt.close()
