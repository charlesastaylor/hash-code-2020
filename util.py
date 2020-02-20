class Library:
    def __init__(self, id, books, time_signup, scan_per_day):
        self.id = id
        self.books = books
        self.signup_days_left = time_signup - 1
        self.time_signup = time_signup
        self.scan_per_day = scan_per_day
        self.signedup = False
        self.scanned = []

    def __str__(self):
        return f'Sign up time: {self.signup_days_left}, Scans per day: {self.scan_per_day}, books: {self.books}'

    def check_signup(self):
        self.signup_days_left -= 1
        if self.signup_days_left <= 0:
            self.signedup = True

    def scan(self, books_scanned):
        out = []
        # this is prob really inefficient
        # to_choose_from = self.books.intersection(books_left)
        to_choose_from = self.books
        for s in range(self.scan_per_day):
            try:
                books_iterable = iter(self.books.items())
                while True:
                    good_book = next(books_iterable)
                    if good_book in books_scanned:
                        self.books.pop(good_book[0])
                    else:
                        break
            except StopIteration:
                return out
            out.append(good_book)  # handle empty
            self.scanned.append(good_book)
            self.books.pop(good_book[0])
        return out