import csv


def compare_csv_files(file1, file2):
    import os
    print(os.getcwd())
    print(file1)
    print(file2)

    with open(file1, newline='') as f1, open(file2, newline='') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        for row1, row2 in zip(reader1, reader2):
            if row1 != row2:
                return False

        # Check if there are any remaining rows in either file
        try:
            next(reader1)
            return False
        except StopIteration:
            pass

        try:
            next(reader2)
            return False
        except StopIteration:
            pass

    return True