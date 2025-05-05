# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXIII
# -----------------------------------------------------------------------------
""" This is the westgard module of Biovarase."""

import sys
import inspect


class Westgards:
    def __str__(self):
        return "class: {0}\nMRO: {1}".format(
            self.__class__.__name__, [x.__name__ for x in Westgards.__mro__]
        )

    def get_westgard_violation_rule(
        self, target, sd, series, selected_batch=None, selected_test=None
    ):
        """This function recive target, sd and series's values
        to compute westgard violation rule.

        @param name: target and sd of the selected batch, series are
                     a list of reversed results of the relative batch
        @return: westgard rule
        @rtype: string
        """
        try:
            self.target = target
            self.sd = sd
            self.series = series
            self.selected_batch = selected_batch
            self.selected_test = selected_test
            self.get_standard_deviations(target, sd)

            if self.get_rule_12S():
                if self.get_rule_13S():
                    return "1:3S"
                elif self.get_rule_22S():
                    return "2:2S"
                elif self.get_rule_R4S():
                    return "R:4S"
                elif self.get_rule_41S():
                    return "4:1S"
                elif self.get_rule_10X():
                    return "10:X"
                else:
                    return "1:2S"
            else:
                if self.get_rule_41S():
                    return "4:1S"
                else:
                    if self.get_rule_10X():
                        return "10:x"
                    else:
                        return "Accept"
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_westgard_violation_rule: {e}",
            )
            return None  # Or raise an exception, depending on your needs

    def get_standard_deviations(self, target, sd):
        try:
            self.sd1 = target + sd
            self.sd2 = target + (2 * sd)
            self.sd3 = target + (3 * sd)
            self.sd_1 = target - sd
            self.sd_2 = target - (2 * sd)
            self.sd_3 = target - (3 * sd)
            self.sd4 = 4 * sd
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_standard_deviations: {e}",
            )

    def get_rule_12S(self):
        """Control data start here.
        1:2s
        Check if the control limits are set as the mean plus/minus 2s
        +/- > 2sd
        If false the value is in control, otherwise we continue the evaluation.
        Refers to the control rule that is commonly used with a Levey-Jennings chart.
        @param name:
        @return: westgard rule
        @rtype: string
        """
        try:
            return self.series[-1] > self.sd2 or self.series[-1] < self.sd_2
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_12S: {e}",
            )
            return False  # Or a suitable default value

    def get_rule_13S(self):
        """1:3s
        Check if the control limits are set as the mean plus 3s and the mean minus 3..."""
        try:
            return self.series[-1] > self.sd3 or self.series[-1] < self.sd_3
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_13S: {e}",
            )
            return False

    def get_rule_22S(self):
        """2:2s
        Check if 2 consecutive control measurements exceed the same mean plus 2s
        or the same mean minus 2s control limit."""
        try:
            last_two_values = self.series[-2:]
            x = all(i > self.sd2 for i in last_two_values)
            y = all(i < self.sd_2 for i in last_two_values)
            return x or y
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_22S: {e}",
            )
            return False

    def get_rule_R4S(self):
        """R:4s
        Check if one control measurement exceeds the mean plus 2s and the other
        exceeds the mean minus 2s.
        If the rule is violated, reject the run.
        """
        try:
            last_two_values = self.series[-2:]
            a = min(last_two_values)
            b = max(last_two_values)
            value = b - a

            return value >= (self.sd4)
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_R4S: {e}",
            )
            return False

    def get_rule_41S(self):
        """4:1s
        Check if 4 consecutive control measurements
        exceed the same mean plus 1s or the same mean minus 1s control limit. """
        try:
            last_four_values = self.series[-4:]
            x = all(i > self.sd1 for i in last_four_values)
            y = all(i < self.sd_1 for i in last_four_values)

            return x or y
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_41S: {e}",
            )
            return False

    def get_rule_10X(self):
        """10:x
        Check when 10 consecutive control measurements fall on one side of the mean."""
        try:
            last_ten_values = self.series[-10:]
            x = all(i > self.target for i in last_ten_values)
            y = all(i < self.target for i in last_ten_values)

            return x or y
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error in get_rule_10X: {e}",
            )
            return False


def main():
    foo = Westgards()
    print(foo)

    # (target, sd, series)
    target = 100
    sd = 10
    series = (100, 100, 100, 100, 100, 100, 121, 90, 100, 100)
    # series = (111,112,113,114,115,116,117,118,119,129)
    # series = (89,88,87,86,85,84,83,82,81,70)
    # series = (111,112,113,114)
    # series = (89,88,87,86)
    # series = (111,112)
    # series = (89,88)
    # series = (121,)
    # series = (79,)

    print(foo.get_westgard_violation_rule(target, sd, series))


if __name__ == "__main__":
    main()
