class Book:

    def __init__(self, title, author, available, checkout_date=None):
        self.title = title
        self.author = author
        self.available = available
        self.checkout_date = checkout_date

# Validate if the data is clean and does not already exist in the database
    def validate(self):
        pass

    def checkout(self):
        pass
