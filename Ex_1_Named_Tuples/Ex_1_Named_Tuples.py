"""
Pratyush Shanbhag
CIS 41B
Exercise NamedTuples
"""

import collections

Grading_Scheme = collections.namedtuple("Grading_Scheme", "grade name labs_scores tests_scores \
                               exercises_scores diagrams_scores")

my_scores = Grading_Scheme(grade=0, name="Pratyush Shanbhag",
                           labs_scores=[96, 95, 97, 96, 97],
                           tests_scores=[97, 92, 98, 88, 96],
                           exercises_scores=[98, 93, 95, 90, 94],
                           diagrams_scores=[90, 95, 97, 87, 95])

grade_float = ((sum(my_scores.labs_scores)/len(my_scores.labs_scores)) * 0.50 + \
               (sum(my_scores.tests_scores)/len(my_scores.tests_scores)) * 0.30 + \
               (sum(my_scores.exercises_scores)/len(my_scores.exercises_scores)) * 0.10 + \
               (sum(my_scores.diagrams_scores)/len(my_scores.diagrams_scores)) * 0.10)

my_scores = my_scores._replace(grade=grade_float)
