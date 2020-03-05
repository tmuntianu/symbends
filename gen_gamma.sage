from bends import gen_random_walks, find_intersections, \
gen_ab, gen_gamma, create_dt, create_intersection_pairings, gen_random_walk
from pyknotid.representations.dtnotation import DTNotation
from pyknotid.representations.gausscode import GaussCode
from pyknotid.representations.representation import Representation
from bends import plot_walk
import numpy as np
from sage.knots.knot import Knots
import sys, os, warnings
from pickle import dump, load

warnings.filterwarnings("ignore")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    symmetry_class = 'gamma'
    try:
        walks_to_gen = int(sys.argv[1])
    except:
        walks_to_gen = 100

    data = dict()
    datadir = os.path.join(os.getcwd(),'data',symmetry_class)

    knots_generated = 0
    blockPrint()

    for j in range(walks_to_gen):
        w1 = gen_random_walk()
        alpha_or_gamma = True
        w2 = gen_gamma(w1)

        walks = [w1, w2]
        ints1 = find_intersections(walks)
        ints2 = find_intersections(reversed(walks))
        ints = create_intersection_pairings(ints1, ints2, alpha_or_gamma=alpha_or_gamma)
        enablePrint()
        print(ints)
        blockPrint()

        if ints is None:
            continue
        print('ints not none')
        for i in ints:
            try:
                dt_code = create_dt(ints2, ints1, i)
            except:
                continue
            try:
                gc = Knots().from_dowker_code(dt_code).gauss_code()[0]
            except:
                continue
            gc_py = ''
            for i in gc:
                gc_py += str(abs(i))
                if np.sign(i) == 1:
                    gc_py += '+'
                else:
                    gc_py += '-'
                gc_py += ','
            gc_py = GaussCode.calculating_orientations(gc_py[:-1])

            rep = GaussCode(gc_py, verbose=False)
            try:
                rep.simplify()
            except: pass
            rep = Representation(rep)
            knots = rep.identify()

            if knots[0].identifier in data:
                continue

            simpgc = []
            gcstr = str(rep)
            try:
                for s in gcstr.split(','):
                    if '-' in s:
                        num = int(s.split('-')[0]) * -1
                    else:
                        num = int(s.split('+')[0])
                    simpgc.append(num)
            except:
                print('Failed to convert to Gauss code')
                continue

            sageknot = Knots().from_gauss_code(simpgc)
            outplot = os.path.join(datadir, knots[0].identifier + '.png')
            print(outplot)
            plot(sageknot).save(outplot)

            infodict = {
                "plot": outplot,
                "gc": simpgc,
                "dt": dt_code,
                "w1": w1,
                "w2": w2,
                "ints": i
            }

            data[knots[0].identifier] = infodict

            enablePrint()
            knots_generated += 1
            print('Successfully generated knot #' + str(knots_generated))
            blockPrint()

    # pickle dict
    enablePrint()
    prevdict = None
    try:
        f = open(os.path.join(datadir, 'datadict'), 'rb')
        prevdict = load(f)
        f.close()
    except: pass
    if prevdict is not None:
        data.update(prevdict)

    f = open(os.path.join(datadir, 'datadict'), 'wb')
    dump(data, f)
    f.close()
    print(data)
