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

class FrequencyHistogramHelper:
    """All methods of an helper class dosen't have self parameter """
    @staticmethod
    def plot_histogram(ax, series, color="green", edgecolor="black", density=False):
        """Plots a frequency histogram."""
        ax.hist(series, color=color, edgecolor=edgecolor, density=density)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.grid(axis='y', alpha=0.75)

    @staticmethod
    def format_axes(ax, x_label="Value", y_label="Frequency", y_label_position="left"):
        """Formats the axes of the histogram."""
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.yaxis.set_label_position(y_label_position)
        ax.grid(axis='y', alpha=0.75)

    @staticmethod
    def add_lines(ax, target=None, avg=None, target_color="orange", avg_color="blue", linewidth=2):
        """Adds vertical lines for target and average."""
        if target is not None:
            ax.axvline(target, color=target_color, linewidth=linewidth, label="Target")
        if avg is not None:
            ax.axvline(avg, color=avg_color, linewidth=linewidth, label="Average")
        ax.legend()
