from array import array
import itertools
import copy
import argparse
import random

class Lattice:
    def __init__(self, size, dimensions, seed, pc, initial_condition="full"):
        self.__size = size
        self.__dimensions = dimensions
        self.__pc = pc
        self.__gen = random.Random(seed)

        if initial_condition == "full":
            self.__sites = array('B',
                    (1 for _ in range(size**dimensions)))
        elif initial_condition == "single":
            self.__sites = array('B',
                    (0 for _ in range(size**dimensions)))
            self.__sites[0] = 1
        else:
            raise TypeError('initial_condition must be "full" or "single"')

        self.__projection = array('B', self.__sites)
        self.__total_mass = sum(self.__sites)

    def numeric_index(self, idx):
        return sum(n*self.__size**i for i, n in enumerate(idx))

    def neighbours(self, idx):
        neighbours = []
        l = list(idx)
        for d in range(self.__dimensions):
            l[d] = (l[d]+1) % self.__size
            yield tuple(l)
            l[d] = (l[d]-1) % self.__size

            if self.__size > 2:
                l[d] = (l[d]-1) % self.__size
                yield tuple(l)
                l[d] = (l[d]+1) % self.__size

    def sites(self):
        return array('B', self.__sites)

    def density(self):
        return sum(self.__sites)/len(self.__sites)

    def total_mass(self):
        return self.__total_mass

    def projection_volume(self):
        return sum(self.__projection)

    def evolve(self):
        next_state = array('B',
                (0 for _ in range(len(self.__sites))))

        for idx in itertools.product(
                range(self.__size), repeat=self.__dimensions):
            for neighbour in self.neighbours(idx):
                if self.__gen.random() < self.__pc:
                    next_state[self.numeric_index(neighbour)] |= \
                            self.__sites[self.numeric_index(idx)]

        self.__sites = next_state
        self.__total_mass += sum(self.__sites)

        for i in range(len(self.__sites)):
            self.__projection[i] |= self.__sites[i]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bond percolation on "
            "(d+1)-dimentional lattices.')

    parser.add_argument('--dimensions', dest='dimensions', metavar='d',
            type=int, default=1, help='Spacial dimensions of the lattice')
    parser.add_argument('--nodes', dest='size', metavar='N', type=int,
            default=1024, help='Number of nodes along each dimension')
    parser.add_argument('--time', dest='t_max', type=int, default=1024,
            help='Maximum number of turns simulated')
    parser.add_argument('--seed', dest='seed', type=int, default=42,
            help='Seed for determining existance of links')
    parser.add_argument('--pc', dest='pc', type=float, default=0.1,
            help='probability of existance of link')

    args = parser.parse_args()

    if args.pc > 1.0 or args.pc < 0.0:
        raise "p_c should be in [0 1]"

    if args.t_max < 0:
        raise "t_max should be non-negative"

    if args.size <= 0:
        raise "nodes should be positive"

    if args.dimensions <= 0 :
        raise "dimensions should positive"

    l = Lattice(size=args.size, dimensions=args.dimensions, seed=args.seed,
            pc=args.pc, initial_condition="single")
    t = 0
    rho = l.density()
    while t < args.t_max and rho > 0:
        l.evolve()
        t += 1
        rho = l.density()

    print(args.pc, args.dimensions, args.seed, args.size,
            l.total_mass(), t, l.projection_volume())
