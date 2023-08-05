import csv
from importlib import resources


def csv_to_nested_dict(package, csv_file, index, lambda_function=lambda x: x):
    """
    Parses a CSV file to a dictionary of dictionaries.

    :param package: the package in which the CSV file is located
    :param csv_file: the CSV file to parse
    :param index: the column to use as the keys of the outer dictionary
    :param lambda_function: an optional function to apply to every value
    :return: A dictionary, with the keys being each row's value for the
    index column, and the values being dictionaries of each row's other values.
    """
    with resources.open_text(package, csv_file) as f:
        csv_iterator = csv.DictReader(f)

        nested_dict = {}
        for csv_row in csv_iterator:
            row_dict = {}
            for k, v in csv_row.items():
                if k != index:
                    row_dict[k] = lambda_function(v)
            nested_dict[csv_row[index]] = row_dict

    return nested_dict


if __name__ == "__main__":
    data = csv_to_nested_dict("pokesummary.data", "type_defenses_modified.csv", "defending_type", lambda x: float(x))
    print(data)
    data2 = csv_to_nested_dict("pokesummary.data", "pokemon_modified.csv", "pokemon_name")
    print(data2)
