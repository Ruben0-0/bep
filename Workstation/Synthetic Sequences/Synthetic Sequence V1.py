# Custom imports:
from Synthetic_Sequencer import synthseq as seq, noisify as noise
from Burgess_Model import main as burg


# Filepath:
filepath = r'D:\AESB\AESB3\BEP\Figures\00 - Synthetic Sequence V1'
# Define (para)sequence:
seq_depths = [0, 40, 65, 100, 110, 140, 145]
seq_facies = ['Fluv.', 'U.Delta', 'L.Delta', 'Coast.', 'N.Shore', 'Marine']
colors = ['gold', 'yellowgreen', 'mediumspringgreen', 'deepskyblue', 'cornflowerblue', 'royalblue']
patterns = ['o.', '\ \*', '\ \o', '\ \.', '-.-', '--']
layout = dict()
for i in range(len(seq_facies)):
    layout[seq_facies[i]] = [colors[i], patterns[i]]
# Define resolution and number of (para)sequences:
res = 5
n = 4
# Create synthetic sequence:
x, y, derivatives, boundaries, dicts = seq.sequencer(seq_depths, seq_facies, layout, res, n, alpha=80, beta=2,
                                                     omega=4, filepath=filepath)

# Add various amounts of noise:
depths1, lithologies1 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0,
                                             filepath=filepath + r'\Gamma = 0')
depths2, lithologies2 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.3,
                                             filepath=filepath + r'\Gamma = 0.3')
depths3, lithologies3 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.5,
                                             filepath=filepath + r'\Gamma = 0.5')
depths4, lithologies4 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=0.8,
                                             filepath=filepath + r'\Gamma = 0.8')
depths5, lithologies5 = noise.gaussian_noise(x, y, derivatives, boundaries, dicts, layout, res, gamma=1.0,
                                             filepath=filepath + r'\Gamma = 1.0')

# Run through Burgess model:
result1_1, result2_1 = burg.main(depths1, lithologies1, layout, res, n, filepath=filepath + r'\Gamma = 0')
result1_2, result2_2 = burg.main(depths2, lithologies2, layout, res, n, filepath=filepath + r'\Gamma = 0.3')
result1_3, result2_3 = burg.main(depths3, lithologies3, layout, res, n, filepath=filepath + r'\Gamma = 0.5')
result1_4, result2_4 = burg.main(depths4, lithologies4, layout, res, n, filepath=filepath + r'\Gamma = 0.8')
result1_5, result2_5 = burg.main(depths5, lithologies5, layout, res, n, filepath=filepath + r'\Gamma = 1.0')
