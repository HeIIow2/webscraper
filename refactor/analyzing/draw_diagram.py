import matplotlib.pyplot as plt
import numpy as np
import itertools

def get_most_important_trends(values: dict, number_of_communities=5):
    """
    Returns the most important trends of the given values.
    """
    values = dict(sorted(values.items(), key=lambda x:linear_regression_slope(x[1]), reverse=True))

    trends = {}
    for i, community in enumerate(values):
        if i >= number_of_communities:
            break

        trends[community] = values[community]

    return trends

def linear_regression(values: list):
    """
    Calculates the linear regression of the given values.
    """
    x = np.array(range(len(values)))
    y = np.array(values)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    return p(x)

def linear_regression_slope(values: list):
    """
    Calculates the linear regression slope of the given values.
    """
    x = np.array(range(len(values)))
    y = np.array(values)
    return np.polyfit(x, y, 1)[0]

def sum_values(values_, added_days=7):
    values = []
    for i, value in enumerate(values_):
        if i % added_days == 0:
            values.append(0)
        values[-1] += value
    # print([round(value, 1) for value in values])
    return values

def get_label(community, values: list, label_class):
    """
    Returns the label of the given community.
    """
    return f"{community}-{label_class.get_description(community)} :  {round(linear_regression_slope(values), 5)}"

def draw_diagram(label_class, magazine, dates_, values, dump_path: str, added_days=7, number_of_communities=5, x_label_tilt=45):
    """
    Draws a diagram of the given values.
    """
    plt.title(magazine)
    plt.xlabel("Dates")
    plt.ylabel("occurrences/article_number")

    # sum dates
    dates = []
    for i, date in enumerate(dates_):
        if i % added_days == 0:
            dates.append(date)

    for community in values:
        values[community] = sum_values(values[community], added_days)
    values = get_most_important_trends(values, number_of_communities)

    # draw diagram
    ax = plt.gca()
    for community in values:
        color = next(ax._get_lines.prop_cycler)['color']
        plt.plot(dates, values[community], '-', color=color, label=get_label(community, values[community], label_class))
        plt.plot(dates, linear_regression(values[community]), '--', color=color)

    plt.legend()
    plt.xticks(rotation=x_label_tilt)
    plt.tight_layout()

    plt.savefig(dump_path)
    plt.show()

