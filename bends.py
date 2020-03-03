from walks import plot_pivot, pivot, plot_dimer, is_saw
import matplotlib.pyplot as plt
import numpy as np
import itertools

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
    plt.axis('equal')
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
    return [-np.array(walk[0]) + 1, -np.array(walk[1]) + 1]

def gen_gamma(walk):
    return [np.array(walk[1]) + 1, np.array(walk[0]) - 1]

def add_midpoints(walk):
    walk_x = []
    walk_y = []
    for i in range(len(walk[0])):
        x = walk[0][i]
        y = walk[1][i]
        if i != 0:
            walk_x.append((x+walk[0][i-1])//2)
            walk_y.append((y+walk[1][i-1])//2)
        walk_x.append(x)
        walk_y.append(y)
    return (walk_x, walk_y)

# throws away walks which are not valid
# invalid walks are walks which overlap themselves (for simplicty's sake we're going with the over cautious approach of more than 2 consecutive points that have already been traveled on)
# invalid walks are also walks which never intersect themselves
def validity_check(walk):
    if is_saw(walk[0], walk[1], len(walk[0])-1):
        return False
    traveled = set()
    last_seen = False

    start_pt = (walk[0][0], walk[1][0])
    end_pt = (walk[0][-1], walk[1][-1])
    for i in range(len(walk[0])):
        pt = (walk[0][i], walk[1][i])
        if pt in traveled:
            if last_seen:
                return False
            last_seen = True
        else:
            last_seen = False

        if i > 0 and i < len(walk[0])-1:
            if pt == start_pt or pt == end_pt:
                return False
    
        traveled.add(pt)

    return True

# returns a list of intersections in the order of the second walk
def find_intersections(walks):
    w1, w2 = walks
    all_pts = set()
    w2_ints = []
    for i in range(len(w1[0])):
        pt1 = w1[0][i]
        pt2 = w1[1][i]
        all_pts.add((pt1, pt2))
    for i in range(len(w2[0])):
        coord = (w2[0][i], w2[1][i])
        if coord in all_pts:
            w2_ints.append(coord)
    return w2_ints

# makes sure there's an even number of intersections
def validate_intersections(intersections):
    if len(intersections[1]) != len(intersections[0]):
        return False
    return len(intersections[0]) % 2 != 0

test_walk = np.array([[ 0,  0,  0,  1,  1,  1,  1,  0, -1, -1, -1, -2, -2, -2, -2, -2,
        -1,  0,  0,  1,  2,  2,  3,  4,  4,  3,  3,  4,  4,  5,  5,  6,
         7,  7,  7,  8],
       [ 0,  1,  2,  2,  1,  0,  1,  1,  1,  0,  1,  1,  0, -1, -2, -3,
        -3, -3, -2, -2, -2, -1, -1, -1,  0,  0,  1,  1,  0,  0, -1, -1,
        -1, -2, -3, -3]])

def gen_random_walk():
    potential_walks = pivot(35, 20, 'dimer', 7)
    
    for w in potential_walks:
        walk = np.array(w)
        try:
            walk = centrify(de_palindrome(walk))
        except:
            pass
            # print('failed at de_pal')
        if (validity_check(walk)):
            return add_midpoints(walk)
    return gen_random_walk()

# returns a list of 
def create_intersection_pairings(w1_ints, w2_ints):
    if validate_intersections([w1_ints, w2_ints]):
        return None
    # we know from validate_intersections w1, w2 ints must be even
    n_bitstrings = ["".join(seq) for seq in itertools.product("01", repeat=(len(w1_ints)//2))]
    # generate all possible combinations
    # now we add to the list of maps based on the bitstrings
    all_intersections = []
    for bitstring in n_bitstrings:
        one_intersection = dict()
        for idx, bit in enumerate(bitstring):
            # NOT SURE IF THESE ARE THE CORRECT PAIRINGS
            one_intersection[w1_ints[idx]] = bit == '0'
            one_intersection[w2_ints[idx]] = bit == '0'
        all_intersections.append(one_intersection)
    return all_intersections

                


if __name__ == "__main__":
    walk = gen_random_walk()

    a_walk = gen_ab(walk)
    g_walk = gen_gamma(walk)
    walks_ab = [walk, a_walk]
    ints_1 = find_intersections(walks_ab)
    ints_2 = find_intersections(reversed(walks_ab))
    print(create_intersection_pairings(ints_1, ints_2))
    print('start a', (walks_ab[0][0][0], walks_ab[0][1][0]), 'start b', (walks_ab[1][0][0], walks_ab[1][1][0]))
    # plot_walk(walks_ab)
    # walks_g = [walk, g_walk]
    # find_intersections(walks_g)
    # print(find_intersections(reversed(walks_g)))
    # plot_walk(walks_g)
