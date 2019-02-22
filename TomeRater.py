# Dustin Manns
# TomeRater Project


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):  # Returns email assoc with user
        return self.email

    def change_email(self, address):  # Updates a user's email
        self.email = address
        print("Your email has been changed to {}".format(self.email))

    def __repr__(self):
        return "USER: {}, EMAIL: {}, BOOKS READ: {}".format(self.name, self.email, self.books)

    def __eq__(self, other_user): # eq if email and name are the same
        if self.email == other_user.email and self.name == other_user.name:
            return True
        else:
            return False

    def read_book(self, book, rating = None):   # Add a new book and optional rating
        self.books[book] = rating

    def get_average_rating(self):   # Calculate user's average rating
        lst = [n for n in self.books.values() if n is not None]
        if len(lst) > 0:
            return sum(lst)/len(lst)
        else:
            return 0


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):   # Returns the title
        return self.title

    def get_isbn(self):   # Returns the ISBN
        return self.isbn

    def set_isbn(self, new_isbn):   # Updates the ISBN
        self.isbn = new_isbn
        print("The book, {} has had it's ISBN updated".format(self.title))

    def add_rating(self, new_rating): # If a rating is between 0 and 4, and to our list of ratings
        if new_rating in range(5):
            self.ratings.append(new_rating)
        else:
            print("No Rating given for ", self.title)

    def __eq__(self, other):   # Eq if title and isbn are the same
        if self.title == other.title and self.isbn == other.isbn:
            return True
        else:
            return False

    def get_average_rating(self):   # Calculate user's average rating
        if len(self.ratings) > 0:
            return sum(self.ratings)/len(self.ratings)
        else:
            return 0

    def __hash__(self):   # I need this to make read_book in the User class
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):   # Returns the Author
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):   # Returns the subject
        return self.subject

    def get_level(self):   # Returns the level
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)

# book1 = Fiction("The Great Gatsby", "F Scott Fitzgerald", "123")
#
# print(book1)


class TomeRater:
    def __init__(self):
        self.users = {}   # Key: email, Value: user object
        self.books = {}   # Key: book object, Value: read count

    def unique_isbn(self, isbn):

        isbn_list = []
        for book in self.books.keys():
            isbn_list.append(book.isbn)

        if isbn not in isbn_list:
            return True
        else:
            return False

    def create_book(self, title, isbn):
        if self.unique_isbn(isbn):
            return Book(title, isbn)
        else:
            print("ISBN Must be unique")

    def create_novel(self, title, author, isbn):
        if self.unique_isbn(isbn):
            return Fiction(title, author, isbn)
        else:
            print("ISBN Must be unique")

    def create_non_fiction(self, title, subject, level, isbn):
        if self.unique_isbn(isbn):
            return NonFiction(title, subject, level, isbn)
        else:
            print("ISBN Must be unique")

    def add_book_to_user(self, books, email, rating=None):
        # If the email exists add in the books
        if email in self.users:
            if type(books) is list:
                for book in books:
                    self.users[email].read_book(book, rating)
                    # Now we'll up the total read count for this book
                    if book in self.books:
                        self.books[book] += 1
                    else:
                        self.books[book] = 1
            else:
                self.users[email].read_book(books, rating)
                books.add_rating(rating)
                # Now we'll up the total read count for this book
                if books in self.books:
                    self.books[books] += 1
                else:
                    self.books[books] = 1

    def add_user(self, name, email, user_books=None):

        # First we make sure the email is valid
        last4 = email[len(email)-4:]

        if "@" in email and (".com" in last4 or ".edu" in last4 or ".org" in last4):
            # Let's check if the user exists before adding it
            if email not in self.users:
                self.users[email] = User(name, email)
            else:
                print("The email {} already exists.".format(email))
                return

            # Adding books if they exist
            if user_books is not None:
                for book in user_books:
                    self.add_book_to_user(book, email)
        else:
            print("Invalid email")

    def print_catalog(self):
        print("Catalog: ")
        for key in self.books.keys():
            print(key)

    def print_users(self):
        print("Users: ")
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        title = None
        max = 0
        # Check numbers times read. If It's the highest, save it. Print the most read at end
        for key in self.books.keys():
            if self.books[key] > max:
                title = key
                max = self.books[key]
        return title

    def highest_rated_book(self):
        title = None
        max = 0
        # Get average rating for each book. Return the highest
        for book in self.books.keys():
            if book.get_average_rating() > max:
                max = book.get_average_rating()
                title = book
        return title

    def most_positive_user(self):
        max_user = None
        max = 0
        # Get average rating for each user. Return the highest
        for user in self.users.values():
            if user.get_average_rating() > max:
                max = user.get_average_rating()
                max_user = user.name
        return max_user





