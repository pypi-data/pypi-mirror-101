#!/usr/bin/python3

import piecash, decimal

book = piecash.open_book("book.sqlite3.gnucash", readonly=False, open_if_lock=True)

# RUB = book.currencies(mnemonic="RUB")


for s in book.accounts(fullname="Unsorted").splits:
    print(s.transaction.description, s.transaction.currency, s.value)
    split = s
    break


if type(split) == piecash.core.transaction.Split:
    trans = split.transaction
    val = split.value

    acc = book.accounts(fullname="Expenses:Other")
    trans.description = "[edited] " + trans.description

    new_split = []

    for i in range(10):
        new_split.append(
            piecash.Split(
                account=acc, value=-decimal.Decimal(str(100)), transaction=trans, memo=i
            )
        )

    new_split.append(
        piecash.Split(
            account=book.accounts(fullname="My:Bank"), value=val, transaction=trans
        )
    )
    new_split.append(
        piecash.Split(
            account=book.accounts(fullname="Unsorted"), value=0, transaction=trans
        )
    )
    print(trans.splits)
    print(new_split)
    trans.splits[:] = new_split
    print(trans.splits)


print("---")

for s in trans.splits:
    print(s.quantity, s.value, s.account.name)

print(trans.currency)
print(acc.commodity)

print("---")

# book.delete(split)

for s in book.accounts(fullname="My:Bank").splits:
    print(s.transaction)

print("---")

for s in book.accounts(fullname="Unsorted").splits:
    print(s.transaction)

print("---")

for s in book.accounts(fullname="Expenses:Other").splits:
    print(s.transaction)

# print(book.track_dirty())

# book.flush()
book.save()
book.close()
