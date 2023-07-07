# Custom imports:
from Visualization_Tools import profile_visualizers as pv
from Synthetic_Sequencer import synthseq as seq, noisify as noise
from Burgess_Model import main as burg
from Post_Burgess import idealseq


# Filepath:
filepath = r'D:\AESB\AESB3\BEP\Figures\04 - Results\Synthetic Sequences\Group A'
# Define (para)sequence:
seq_depths = [0, 6.3, 10.1, 13, 14.5, 17.9, 20]
seq_facies = ['Fluv.', 'U.Delta', 'L.Delta', 'Coast.', 'N.Shore', 'Marine']
colors = ['gold', 'yellowgreen', 'mediumspringgreen', 'cyan', 'cornflowerblue', 'navy']
patterns = ['o.', '\ \*', '\ \o', '\ \.', '-.-', '--']
layout = dict()
for i in range(len(seq_facies)):
    layout[seq_facies[i]] = [colors[i], patterns[i]]
# Define resolution and number of (para)sequences:
res = 0.4
n = 15
# Visualize parasequence:
pv.parasequence_profile(seq_depths, seq_facies, layout, 5,
                        filepath=r'D:\AESB\AESB3\BEP\Figures\04 - Results\Synthetic Sequences' + '\Parasequence.png')


# Create synthetic sequence:
# x, y, derivatives, boundaries, dicts = seq.sequencer(seq_depths, seq_facies, layout, res, n, alpha=10, beta=1, psi=1.0,
#                                                      omega=4, asymmetric=False, filepath=filepath + r'\Config 1')

# # Asymmetric sequence runs:
depths, lithologies = seq.sequencer(seq_depths, seq_facies, layout, res, n, alpha=10, beta=0, psi=0.7,
                                    omega=4, asymmetric=True, filepath=filepath + '\Config 3')
result1_1, result2_1, result3_1 = burg.main(depths, lithologies, layout, res, n, filepath=filepath + '\Config 3')


# Add various amounts of noise:
# depths1, lithologies1 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.2,
#                                              filepath=filepath + r'\Config 1')
# depths2, lithologies2 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.1,
#                                              filepath=filepath + r'\Config 2')
# depths3, lithologies3 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.3,
#                                              filepath=filepath + r'\Config 3')
# depths4, lithologies4 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.5,
#                                              filepath=filepath + r'\Config 4')
# depths5, lithologies5 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.8,
#                                              filepath=filepath + r'\Config 5')
# depths6, lithologies6 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=1.0,
#                                              filepath=filepath + r'\Config 6')

# Run through Burgess model:
# result1_1, result2_1, result3_1 = burg.main(depths1, lithologies1, layout, res, n, filepath=filepath + r'\Config 1')
# result1_2, result2_2, result3_2 = burg.main(depths2, lithologies2, layout, res, n, filepath=filepath + r'\Config 2')
# result1_3, result2_3, result3_3 = burg.main(depths3, lithologies3, layout, res, n, filepath=filepath + r'\Config 3')
# result1_4, result2_4, result3_4 = burg.main(depths4, lithologies4, layout, res, n, filepath=filepath + r'\Config 4')
# result1_5, result2_5, result3_5 = burg.main(depths5, lithologies5, layout, res, n, filepath=filepath + r'\Config 5')
# result1_6, result2_6, result3_6 = burg.main(depths6, lithologies6, layout, res, n, filepath=filepath + r'\Config 6')
