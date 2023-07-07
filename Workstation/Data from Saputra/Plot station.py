from matplotlib import pyplot as plt
import numpy as np

## Group B runs:
gamma = [0, 0.1, 0.3, 0.5, 0.8, 1]
m_1 = [1, 0.78, 0.49, 0.32, 0.17, 0.1]
m_2 = [1, 0.79, 0.49, 0.31, 0.15, 0.14]
m_3 = [1, 0.79, 0.55, 0.32, 0.17, 0.14]
m_4 = [1, 0.76, 0.5, 0.3, 0.19, 0.11]
m_5 = [1, 0.76, 0.47, 0.36, 0.13, 0.15]
plt.scatter(gamma, m_1, label='Run 1')
plt.scatter(gamma, m_2, label='Run 2')
plt.scatter(gamma, m_3, label='Run 3')
plt.scatter(gamma, m_4, label='Run 4')
plt.scatter(gamma, m_5, label='Run 5')
### Fit trendline:
coefficients = np.polyfit(gamma + gamma + gamma + gamma + gamma, m_1 + m_2 + m_3 + m_4 + m_5, 2)
line = np.poly1d(coefficients)
plt.plot(np.linspace(0, 1, 100), line(np.linspace(0, 1, 100)))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xlabel(r'$\gamma$ [-]')
plt.ylabel('Max. Markov Order Metric m')
plt.title('Group B', weight='semibold')
plt.legend()
plt.savefig(r'D:\AESB\AESB3\BEP\Figures\04 - Results\Synthetic Sequences\Group B\Gamma vs m.png', bbox_inches='tight')
plt.close()

## Group C runs:
gamma = [0, 0.1, 0.3, 0.5, 0.8, 1]
m_1 = [0.9, 0.69, 0.39, 0.28, 0.14, 0.1]
m_2 = [0.78, 0.53, 0.35, 0.29, 0.15, 0.09]
m_3 = [0.84, 0.67, 0.4, 0.28, 0.14, 0.08]
m_4 = [0.75, 0.5, 0.36, 0.29, 0.17, 0.12]
m_5 = [0.83, 0.6, 0.45, 0.29, 0.15, 0.1]
plt.scatter(gamma, m_1, label='Run 1')
plt.scatter(gamma, m_2, label='Run 2')
plt.scatter(gamma, m_3, label='Run 3')
plt.scatter(gamma, m_4, label='Run 4')
plt.scatter(gamma, m_5, label='Run 5')
### Fit trendline:
coefficients = np.polyfit(gamma + gamma + gamma + gamma + gamma, m_1 + m_2 + m_3 + m_4 + m_5, 2)
line = np.poly1d(coefficients)
plt.plot(np.linspace(0, 1, 100), line(np.linspace(0, 1, 100)))
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xlabel(r'$\gamma$ [-]')
plt.ylabel('Max. Markov Order Metric m')
plt.title('Group C', weight='semibold')
plt.legend()
plt.savefig(r'D:\AESB\AESB3\BEP\Figures\04 - Results\Synthetic Sequences\Group C\Gamma vs m.png', bbox_inches='tight')
plt.close()


# Group D:
psi = [0.5, 0.7, 0.8, 0.9, 1]
m_1 = [0.48, 0.41, 0.53, 0.48, 0.52]
