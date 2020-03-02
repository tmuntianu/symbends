from walks import plot_pivot, pivot, plot_dimer
import matplotlib.pyplot as plt
import numpy as np

def plot_walk(walks):
    plt.figure(figsize = (8, 8))
    c = ['b','g', 'r', 'c', 'm', 'y', 'k']
    if isinstance(walks,list):
        for i, walk in enumerate(walks):
            x, y = walk
            plt.plot(x, y, c[i%len(c)] + '.-', linewidth = 1)
    else:
        x, y = walk
        plt.plot(x, y, 'b.-', linewidth = 1)
    plt.plot(0, 0, 'go', ms = 12, label = 'Start')
    plt.plot(x[-1], y[-1], 'ro', ms = 12, label = 'End')
    plt.axis('equal')
    plt.legend()
    plt.title('Walk', fontsize=14, fontweight='bold', y = 1.05)
    plt.show()

def de_palindrome(walk):
    coords = list(zip(walk[0],walk[1]))
    stack = []
    droming = False
    for i, coord in enumerate(coords):
        if i > 1:
            # if we find a match
            if coord == stack[-2]:
                droming = True
                stack.pop()
            else:
                droming = False
        
        if not droming:
            stack.append(coord)

    if stack[-1] == stack[-2]:
        stack.pop()

    return list(zip(*stack))

def centrify(walk):
    xbar = sum(walk[0])//len(walk[0])
    ybar = sum(walk[1])//len(walk[1])
    return [2 * (walk[0] - xbar), 2 * (walk[1] - ybar)] # multiply by two to get on even grid

def gen_ab(walk):
    return [-walk[0] + 1, -walk[1] + 1]

def gen_gamma(walk):
    return [walk[1] + 1, walk[0] + 1]


tst = np.array([[ 0,  0,  0,  1,  1,  1,  1,  0, -1, -1, -1, -2, -2, -2, -2, -2,
        -1,  0,  0,  1,  2,  2,  3,  4,  4,  3,  3,  4,  4,  5,  5,  6,
         7,  7,  7,  8],
       [ 0,  1,  2,  2,  1,  0,  1,  1,  1,  0,  1,  1,  0, -1, -2, -3,
        -3, -3, -2, -2, -2, -1, -1, -1,  0,  0,  1,  1,  0,  0, -1, -1,
        -1, -2, -3, -3]])

# plot_walk(tst)
# plot_walk(de_palindrome(tst))
tst = centrify(de_palindrome(tst))
a_tst = gen_ab(tst)
walks = [tst, a_tst]
plot_walk(walks)