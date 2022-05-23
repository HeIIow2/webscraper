import matplotlib.pyplot as plt
import numpy as np

def sum_values(values_, added_days=7):
    values = []
    for i, value in enumerate(values_):
        if i % added_days == 0:
            values.append(0)
        values[-1] += value
    return values

def draw_diagram(magazine, dates_, values, dump_path: str, added_days=7):
    """
    Draws a diagram of the given values.
    """
    plt.title(magazine)
    plt.xlabel("Dates")
    plt.ylabel("Values")

    # sum dates
    dates = []
    for i, date in enumerate(dates_):
        if i % added_days == 0:
            dates.append(date)

    for community in values:
        values[community] = sum_values(values[community], added_days)
        plt.plot(dates, values[community])

    plt.savefig(dump_path)
    plt.show()

