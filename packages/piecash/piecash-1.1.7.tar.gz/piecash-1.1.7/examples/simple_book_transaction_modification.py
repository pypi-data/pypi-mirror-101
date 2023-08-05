from piecash import open_book, ledger, Split

# create a book with some account tree structure
with open_book(
    "../gnucash_books/simple_book_transaction_creation.gnucash", readonly=True
) as mybook:
    # iterate on all the transactions in the book
    for transaction in mybook.transactions:
        # add some extra text to the description
        transaction.description = transaction.description + " (some extra info)"
        # iterate over all the splits
        # as we will add splits to the transaction in the loop,
        # we need to use list(...) to make a list of the splits at the start of the loop
        for split in list(transaction.splits):
            # create the new split (here a copy of the each existing split
            # in the transaction with value/quantity divided by 10
            new_split = Split(
                account=split.account,
                value=split.value / 10,
                quantity=split.quantity / 10,
                memo="my new split",
                transaction=transaction,  # attach the split to the current transaction
            )
    mybook.flush()  # register the changes (but not save)
    print(ledger(mybook))

    # save the book
    # this will raise an error as readonly=True (change to readonly=False to successfully save the book)
    mybook.save()
