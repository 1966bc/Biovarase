# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   var MMXXV
# -----------------------------------------------------------------------------
""" This is the frequency histogram helper class of Biovarase."""
import matplotlib.pyplot as plt
import matplotlib.ticker

class LeveyJenningsPlotHelper:
    """All methods of an helper class dosen't have self parameter """
    @staticmethod
    def plot_data(ax, series, x_labels, annotate=True):
        """Plots the series data on the Levey-Jennings chart."""
        ax.plot(range(len(series)), series, marker="8", label="data")
        if annotate:
            for x, y in enumerate(series):
                ax.text(x, y, str(y))

    @staticmethod
    def plot_sd_lines(ax, target, sd, colors=None, linestyles=None):
        """Plots standard deviation lines."""
        if colors is None:
            colors = ["red", "yellow", "green"]
        if linestyles is None:
            linestyles = ["--"] * 3

        sd_levels = [3, 2, 1]
        for i, level in enumerate(sd_levels):
            ax.axhline(target + sd * level, color=colors[i], linestyle=linestyles[i],
                       label=f"+{level} sd")
            ax.axhline(target - sd * level, color=colors[i], linestyle=linestyles[i],
                       label=f"-{level} sd")
        ax.axhline(target, color="black", linestyle="-", linewidth=2, label="Target")

    @staticmethod
    def format_axes(ax, x_labels, y_label, x_rotation=70, ha="right", x_size=6,
                    y_major_locator=21, y_major_formatter="%.2f"):
        """Formats the axes."""
        ax.set_xticks(range(len(x_labels))) 
        ax.set_xticklabels(x_labels, rotation=x_rotation, ha=ha, size=x_size)
        ax.set_ylabel(y_label)
        ax.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(y_major_locator))
        ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter(y_major_formatter))
        ax.grid(True)

    @staticmethod
    def create_title(ax, test_name, workstation_name1, workstation_name2,
                     control_name, batch_number, separator="\n", loc="center"):
        """Creates and sets the title."""
        title = f"{test_name} on {workstation_name1} {workstation_name2}{separator}{control_name} lot {batch_number}"
        ax.set_title(title, loc=loc)

    @staticmethod
    def create_footer_text(dates, count_series, count_rs, separator="to"):
        """Creates the footer text."""
        if not dates:
            return f"Computed {count_series} on {count_rs} results"
        text = f"from {dates[0]} {separator} {dates[-1]} computed {count_series} on {count_rs} results"
        return text

    @staticmethod
    def add_footer_text(ax, text, ha="right", va="bottom", weight="bold", color="black",
                        x_pos=0.95, y_pos=0.01):
        """Adds footer text."""
        ax.text(x_pos, y_pos, text, transform=ax.transAxes, ha=ha, va=va, weight=weight,
                color=color)
