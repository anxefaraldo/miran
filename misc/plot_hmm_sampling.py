print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

from sklearn import hmm

##############################################################
# Prepare parameters for a 3-components HMM
# Initial population probability
start_prob = np.array([0.33, 0.33, 0.33])
# The transition matrix, note that there are no transitions possible
# between component 1 and 4
trans_mat = np.array([[0, 0.5, 0.5],
                      [0.3, 0, 0.7],
                      [0.9, 0.1, 0]
                      ])
# The means of each component
means = np.array([[0,  0],
                  [100, 50],
                  [50, 100]
                  ])
# The covariance of each component
# covars = 0.5 * np.tile(np.identity(2), (4, 1, 1))
covars = np.array([0.0001,0.0001,0.0001])

# Build an HMM instance and set parameters
model = hmm.GaussianHMM(3, "spherical", start_prob, trans_mat,
                        random_state=3)

# Instead of fitting it from the data, we directly set the estimated
# parameters, the means and covariance of the components
model.means_ = means
model.covars_ = covars
###############################################################

# Generate samples
X, Z = model.sample(10)

# Plot the sampled data
plt.plot(X[:, 0], X[:, 1], "-o", label="observations", ms=6,
         mfc="orange", alpha=0.7)

# Indicate the component numbers
for i, m in enumerate(means):
    plt.text(m[0], m[1], 'Component %i' % (i + 1),
             size=17, horizontalalignment='center',
             bbox=dict(alpha=.7, facecolor='w'))
plt.legend(loc='best')
plt.show()

