from datetime import date

import piecash
from piecash import Commodity, Price

# create a new book
with piecash.create_book() as book:
    # create a commodity/stock
    cdty = Commodity("NYSE", "WOCA", "wonder cola", book=book)

    # create two quotes/prices
    p = Price(cdty, book.default_currency, date(2018, 9, 6), "3.44")
    p = Price(cdty, book.default_currency, date(2018, 9, 7), "3.52")

    # save the book
    book.save()

    # create a second price for the second day
    p = Price(cdty, book.default_currency, date(2018, 9, 7), "3.45")

    # save the book ==> raise exception when validating the book as duplicate price (same cdty x currency x day
    try:
        book.save()
        print("this code will not be reached")
    except ValueError:
        print(
            "You cannot have two price in same currency for same commodity and same day"
        )

    # cancel last operations
    book.cancel()

    # to change a price, retrieve it first and then modify it
    # retrieve price for given day
    price = book.prices(
        commodity=cdty, currency=book.default_currency, date=date(2018, 9, 7)
    )
    print(price)
    price.value = "3.45"

    book.save()

    # check prices have been modified correctly
    print(book.prices)

    # you can also use a helper that will either add or modify a price
    def add_or_update_price(cdty, curr, day, value):
        try:
            price = book.prices(
                commodity=cdty, currency=curr, date=day
            )  # raise a KeyError if Price does not exist
            print("--> modifying existing price ", price)
            price.value = value
        except KeyError:
            price = Price(cdty, curr, day, value)
            print("--> adding new price ", price)

    add_or_update_price(cdty, book.default_currency, date(2018, 9, 9), 5)
    book.save()

    add_or_update_price(cdty, book.default_currency, date(2018, 9, 9), 6)
    book.save()
