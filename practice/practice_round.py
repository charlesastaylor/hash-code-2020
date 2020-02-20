from itertools import combinations


class PizzaOrder:  
    def __init__(self, infile):
        self.in_fname = infile
        self.out_fname = infile.split('.')[0] + '.out'
        with open(infile) as f:
            s = f.read()
        lines = s.split('\n')
        self.M, self.N = [int(n) for n in lines[0].split()]
        self.num_slices = [int(n) for n in lines[1].split()]

    def write_output(self, fname, pizza_types):
        K = len(pizza_types)
        if self.is_output_valid(pizza_types):
            with open(fname, 'w') as f:
                f.write(str(K) + '\n')
                f.write(' '.join([str(n) for n in pizza_types]))
                print(f'Solution written to {self.out_fname}')

    def is_output_valid(self, pizza_types):
        K = len(pizza_types)
        # assert 0 <= K <= self.N, "K less than zero or bigger than N"
        # assert sum([self.num_slices[t] for t in pizza_types]) <= self.M, "Orderd too many slices"
        if (0 <= K <= self.N and
                sum([self.num_slices[t] for t in pizza_types]) <= self.M):
            return True
        return False

    def score_output(self, pizza_types):
        return sum(self.num_slices[t] for t in pizza_types)

    def solve_brute(self):
        max_score = 0
        for n in range(1, self.N + 1):
            for c in combinations(range(self.N), n):
                if self.is_output_valid(c):
                    max_score = max(max_score, self.score_output(c))
                    out = c
        print(f'Solution for dataset: {self.in_fname} found')
        self.write_output(self.out_fname, out)        


if __name__ == "__main__":
    data_sets = [
        "a_example.in",
        "b_small.in",
        "c_medium.in",
        "d_quite_big.in",
        "e_also_big.in"
    ]
    
    for fname in data_sets:
        P = PizzaOrder(fname)
        P.solve_brute()

