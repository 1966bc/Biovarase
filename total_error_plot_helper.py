# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   var MMXXV
# -----------------------------------------------------------------------------
""" This is the total error plot helper class of Biovarase."""
import matplotlib.pyplot as plt
import matplotlib.ticker

class TotalErrorPlotHelper:

    @staticmethod
    def plot_data_and_annotations(ax, series, x_labels):
        """Plots the data series and adds annotations for each point."""

        ax.plot(series, marker="8", label='data')
        ax.set_xticks(range(len(series)))
        ax.set_xticklabels(x_labels, rotation=70, size=6)

        for x, y in enumerate(series):
            ax.text(x, y, str(y))

    @staticmethod
    def plot_limit_lines(ax, target, upper_limit, lower_limit, series_length):
        """Plots the target line and the upper/lower limit lines."""

        upper_line = [upper_limit] * (series_length + 1)
        lower_line = [lower_limit] * (series_length + 1)
        target_line = [target] * (series_length + 1)

        ax.plot(upper_line, color="violet", label='Tea +4', linestyle='--')
        ax.plot(target_line, label='target', linewidth=2)
        ax.plot(lower_line, color="violet", label='Tea -4', linestyle='--')

    @staticmethod
    def set_axes_labels(ax, um):
        """Sets the y-axis label."""

        if um is not None:
            ax.set_ylabel(str(um[0]))
        else:
            ax.set_ylabel("No unit assigned yet")

    @staticmethod
    def create_title(batch, upper_limit, lower_limit, tea, te, z_score):
        """Creates the title for the subplot."""

        s = "Batch: {0} Target: {1} Upper: {2} Lower: {3} ETa%: {4:.2f} Te%: {5:.2f} Z Score: {6:.2f}"
        return s.format(batch[4],
                        round(batch[6], 2),
                        upper_limit,
                        lower_limit,
                        tea,
                        te,
                        z_score)

    @staticmethod
    def create_footer_text(dates, count_series, count_rs):
        """Creates the footer text for the subplot."""
        return ("from %s to %s" % (dates[0], dates[-1]), count_series, count_rs)

    @staticmethod
    def add_footer_text(ax, bottom_text):
        """Adds the footer text to the subplot."""

        ax.text(0.95, 0.01,
                '%s computed %s on %s results' % bottom_text,
                verticalalignment='bottom',
                horizontalalignment='right',
                transform=ax.transAxes,
                color='black')
