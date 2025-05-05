# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   var MMXXV
# -----------------------------------------------------------------------------
""" This is the youden plot helper class of Biovarase."""
import matplotlib.pyplot as plt
import matplotlib.ticker

class YoudenPlotHelper:

    @staticmethod
    def set_axes_limits(ax, first_sample_target, first_sample_sd, second_sample_target, second_sample_sd):
        """Imposta i limiti degli assi in base ai target e alle deviazioni standard."""

        first_sample_low_limit = first_sample_target - (first_sample_sd * 5)
        first_sample_high_limit = first_sample_target + (first_sample_sd * 5)

        second_sample_low_limit = second_sample_target - (second_sample_sd * 5)
        second_sample_high_limit = second_sample_target + (second_sample_sd * 5)

        ax.set_xlim(first_sample_low_limit, first_sample_high_limit)
        ax.set_ylim(second_sample_low_limit, second_sample_high_limit)

    @staticmethod
    def plot_target_lines(ax, first_sample_target, second_sample_target):
        """Traccia le linee target orizzontali e verticali."""

        ax.axvline(x=first_sample_target, linewidth=2, color='orange')
        ax.axhline(y=second_sample_target, linewidth=2, color='orange')

    @staticmethod
    def plot_sd_lines(ax, first_sample_target, first_sample_sd, second_sample_target, second_sample_sd):
        """Traccia le linee di deviazione standard."""

        # Linee verticali (primo campione)
        ax.axvline(x=first_sample_target + (first_sample_sd), ymin=0.4, ymax=0.6, linestyle='--', color='green')
        ax.axvline(x=first_sample_target - (first_sample_sd), ymin=0.4, ymax=0.6, linestyle='--', color='green')
        ax.axvline(x=first_sample_target + (first_sample_sd * 2), ymin=0.3, ymax=0.7, linestyle='--', color='yellow')
        ax.axvline(x=first_sample_target - (first_sample_sd * 2), ymin=0.3, ymax=0.7, linestyle='--', color='yellow')
        ax.axvline(x=first_sample_target + (first_sample_sd * 3), ymin=0.2, ymax=0.8, linestyle='--', color='red')
        ax.axvline(x=first_sample_target - (first_sample_sd * 3), ymin=0.2, ymax=0.8, linestyle='--', color='red')

        # Linee orizzontali (secondo campione)
        ax.axhline(y=second_sample_target + (second_sample_sd), xmin=0.4, xmax=0.6, linestyle='--', color='green')
        ax.axhline(y=second_sample_target - (second_sample_sd), xmin=0.4, xmax=0.6, linestyle='--', color='green')
        ax.axhline(y=second_sample_target + (second_sample_sd * 2), xmin=0.3, xmax=0.7, linestyle='--', color='yellow')
        ax.axhline(y=second_sample_target - (second_sample_sd * 2), xmin=0.3, xmax=0.7, linestyle='--', color='yellow')
        ax.axhline(y=second_sample_target + (second_sample_sd * 3), xmin=0.2, xmax=0.8, linestyle='--', color='red')
        ax.axhline(y=second_sample_target - (second_sample_sd * 3), xmin=0.2, xmax=0.8, linestyle='--', color='red')

    @staticmethod
    def plot_data_points(ax, x, y):
        """Traccia i punti dati e le annotazioni."""

        ax.scatter(x, y, marker='8', s=80)
        for i, txt in enumerate(zip(x, y)):
            ax.annotate(f"{txt[0]:.2f}, {txt[1]:.2f}", (x[i], y[i]), size=8)


    @staticmethod
    def set_axes_labels(ax, um):
        """Imposta le etichette degli assi."""

        if um is not None:
            ax.set_ylabel(str(um[0]))
            ax.set_xlabel(str(um[0]))
        else:
            ax.set_ylabel("No unit assigned yet")
            ax.set_xlabel("No unit assigned yet")

    @staticmethod
    def create_title(batches):
        """Crea il titolo del grafico."""

        first_sample_target = batches[0][6]
        second_sample_target = batches[1][6]

        first_sample_sd = batches[0][7]
        second_sample_sd = batches[1][7]

        s = "Batch: {0} Target: {1:.1f} sd: {2:.1f} Batch: {3} Target: {4:.1f} sd: {5:.1f}"

        return s.format(batches[0][4],
                         first_sample_target,
                         first_sample_sd,
                         batches[1][4],
                         second_sample_target,
                         second_sample_sd)
