def save_returns(books):
    try:
        with open("returns.log", "a") as log:
            for b in books:
                log.write(b + "\n")

    except OSError as e:
        with open("error.log", "a") as err:
            err.write(str(e) + "\n")


def process(day_file):
    try:
        with open(day_file, "r") as f:
            books = f.read().splitlines()

        save_returns(books)

    except OSError as e:
        with open("error.log", "a") as err:
            err.write(str(e) + "\n")


process("day1.txt")
process("day2.txt")
process("day3.txt")