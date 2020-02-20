from util import *


def first_library(libraries):
    return list(sorted(libraries, key=lambda l: l.signup_days_left))[0]


def fastest_signup_libraries(libraries):
    # print([l.signup_days_left for l in sorted(libraries, key=lambda l: l.signup_days_left)])
    # return sorted(libraries, key=lambda l: l.signup_days_left)
    L = sorted(libraries, reverse=True, key=lambda l: l.scan_per_day)
    # print([l.scan_per_day for l in L])
    return L


def sim(days, books, libraries, books_scanned):
    libraries = fastest_signup_libraries(libraries)
    x = 0
    l1 = libraries[x]
    # l1 = first_library(libraries)
    libraries_activated = [l1]
    total_books = []
    for d in range(days):
        # print("days", d)
        if libraries_activated[-1].signedup:
            x += 1
            try:
                libraries_activated.append(libraries[x])
            except IndexError:
                pass

        # skip last libr that still signing up
        for l in libraries_activated[:-1]:
            books_from_l = l.scan(books_scanned)
            #print("books_from_l", books_from_l)
            # for l in libraries:
            #     for b in books_from_l:
            #         try:
            #             del l.books[b[0]]
            #         except KeyError:
            #             pass
        for l in libraries_activated:
            l.check_signup()
        #print("{l.id: {k: v for k, v in l.scanned} for l in libraries_activated}", {l.id: {k: v for k, v in l.scanned} for l in libraries_activated})
    # this doesnt optimise. cos maybe first library takes only book left that last library has to scan
    #return itertools.chain(*(l.scanned for l in libraries_activated)), libraries_activated
    return {l.id: {k: v for k, v in l.scanned} for l in libraries_activated}


class Solution:
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as f:
            s = f.read()
        lines = s.split("\n")
        B, L, self.days = [int(c) for c in lines[0].split()]
        self.books = {i: int(c) for i, c in enumerate(lines[1].split())}
        library_input = lines[2:]
        self.libraries = []
        self.books_scanned = set()
        for i in range(0, L):
            N, T, M = [int(n) for n in library_input[2* i].split()]
            book_ids_scores = [(int(n), self.books[int(n)]) for n in library_input[2 * i + 1].split()]
            libary_books = {x: y for (x, y) in sorted(book_ids_scores, key=lambda x: -x[1])}
            library = Library(i, libary_books, T, M)
            self.libraries.append(library)

    def text_input(self):
        print(f'{self.filename}, {self.days}, {self.books}')
        for l in self.libraries:
            print(l)

    def solve(self):
        highest_score = 0
        best_perm = None
        # for num_libs in range(1, len(self.libraries)):
        #     for permy in itertools.permutations(libraries, num_libs):
        out = sim(self.days, self.books, fastest_signup_libraries(self.libraries), self.books_scanned)
        score = sum(sum(o.values()) for o in out.values())
                # if highest_score < score:
                #     highest_score = score
                #     best_perm = permy
        #print(out) # {0: {3: 6}, 1: {}} 
        # print(score)
        out = {key: value for key, value in out.items() if len(value) != 0}
        self.write_output(out)

    def write_output(self, ans):
        """ ans is a dcitionary from library ids to ordered list of book ids to scan from that library
        """
        out_fname = self.filename[:-4] + '.out'
        out_fname = 'out_' + self.filename
        with open(out_fname, 'w') as f:
            f.write(str(len(ans)) + '\n')
            for library in ans:
                books = ans[library]
                f.write(str(library) + ' ' + str(len(books)) + '\n')
                f.write(' '.join(str(n) for n in books.keys()) + '\n')
        print(f'Output written to {out_fname}')

def f(a):
    s = Solution(a)
    s.solve()

def main():
    data_sets = [
        "a_example.txt",
        "b_read_on.txt",
        "c_incunabula.txt",
        "d_tough_choices.txt",
        "e_so_many_books.txt",
        "f_libraries_of_the_world.txt"
    ]


    # d = data_sets[2]
    # Solution(d).solve()
    from multiprocessing import Process
    from multiprocessing import Pool
    ps = []
    for d in data_sets:
        p = Process(target=f, args=(d,))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
    
    # Test output
    # ans = {1:[5,2,3], 0:[0,1,2,3,4]}
    # s.write_output(ans)

    return

if __name__ == "__main__":
    main()


