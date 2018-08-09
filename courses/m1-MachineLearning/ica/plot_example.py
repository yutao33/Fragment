import numpy as np
import scipy
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA, FastICA

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文
plt.rcParams['axes.unicode_minus']=False #正常显示负号

# #############################################################################
# Generate sample data
rng = np.random.RandomState(42)
#S = rng.standard_t(1.5, size=(20000, 2))
S = rng.normal(0, size=(20000, 2))
S[:, 0] *= 2.

# Mix data
A = np.array([[1, 1], [0, 2]])  # Mixing matrix

X = np.dot(S, A.T)  # Generate observations

pca = PCA()
S_pca_ = pca.fit(X).transform(X)

ica = FastICA(random_state=rng)
S_ica_ = ica.fit(X).transform(X)  # Estimate the sources

S_ica_ /= S_ica_.std(axis=0)

print(ica.mixing_)

# #############################################################################
# Plot results

def plot_samples(S, axis_list=None):
    plt.scatter(S[:, 0], S[:, 1], s=2, marker='o', zorder=10,
                color='steelblue', alpha=0.5)
    if axis_list is not None:
        colors = ['orange', 'red']
        for color, axis in zip(colors, axis_list):
            axis /= axis.std()
            x_axis, y_axis = axis
            # Trick to get legend to work
            plt.plot(0.1 * x_axis, 0.1 * y_axis, linewidth=2, color=color)
            plt.quiver(0, 0, x_axis, y_axis, zorder=11, width=0.01, scale=6,
                       color=color)

    plt.hlines(0, -3, 3)
    plt.vlines(0, -3, 3)
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.xlabel('x')
    plt.ylabel('y')

plt.figure()
plt.subplot(2, 2, 2)
plot_samples(S / S.std())
plt.title('真实信号')

axis_list = [pca.components_.T, ica.mixing_]
plt.subplot(2, 2, 3)
plot_samples(X / np.std(X))
# legend = plt.legend(['PCA', 'ICA'], loc='upper right')
# legend.set_zorder(100)

plt.title('混合信号')

plt.subplot(2, 2, 1)
xx=np.linspace(-3,3,100)
yy=scipy.stats.norm.pdf(xx)
plt.plot(xx,yy)
plt.title('正态分布概率密度函数')


plt.subplot(2, 2, 4)
plot_samples(S_ica_ / np.std(S_ica_))
plt.title('ICA解析信号')

plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.36)
plt.show()
