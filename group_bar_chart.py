import matplotlib.pyplot as plt
import numpy as np


def grouped_percentage_bar_chart(categories, usage_values, win_values, title):
    """
    Creates a grouped bar chart for Usage % and Win %.

    categories: list like ["Wide", "Body", "T"]
    usage_values: list of floats (0–1)
    win_values: list of floats (0–1)
    title: chart title
    """

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width/2, usage_values, width, label="Usage %")
    rects2 = ax.bar(x + width/2, win_values, width, label="Win %")

    # Add labels on top of bars
    ax.bar_label(rects1, labels=[f"{v:.0%}" for v in usage_values], padding=3)
    ax.bar_label(rects2, labels=[f"{v:.0%}" for v in win_values], padding=3)

    ax.set_ylabel("Percentage")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1)
    ax.set_yticks(np.linspace(0, 1, 5))
    ax.set_yticklabels([f"{int(t*100)}%" for t in np.linspace(0, 1, 5)])

    ax.legend()

    return fig
