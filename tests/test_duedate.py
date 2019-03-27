# Description for used dates
#
#     2018.12.24 Monday
#     2018.12.25 Tuesday
#     2018.12.26 Wednesday
#     2018.12.27 Thursday
#     2018.12.28 Friday
#     2018.12.29 Saturday
#     2018.12.30 Sunday
#
#     2019.12.31 Monday
#     2019.01.01 Tuesday
#

import unittest
from datetime import datetime

from duedate.duedate import DueDate
from duedate.duedate import WORK_ENDING_HOUR
from duedate.duedate import WORK_HOURS
from duedate.duedate import WORK_STARTING_HOUR


class TestGlobals(unittest.TestCase):
    def test_globals(self):
        self.assertIsNotNone(WORK_ENDING_HOUR)
        self.assertIsNotNone(WORK_STARTING_HOUR)
        self.assertIsNotNone(WORK_HOURS)

        self.assertGreater(WORK_STARTING_HOUR, 0)
        self.assertGreater(WORK_ENDING_HOUR, 0)
        self.assertGreater(WORK_ENDING_HOUR, WORK_STARTING_HOUR)

        self.assertEqual(WORK_ENDING_HOUR - WORK_STARTING_HOUR, WORK_HOURS)


class TestDueDate(unittest.TestCase):
    def setUp(self):
        self.calculator = DueDate()

    def test__next_monday(self):
        next_monday = self.calculator._next_monday

        with self.assertRaises(AttributeError):
            next_monday(None)

        self.assertEqual(next_monday(datetime(2018, 12, 25)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 26)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 27)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 28)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 29)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 30)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 30)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_monday(datetime(2018, 12, 31)),
                         datetime(2019, 1, 7))

    def test__next_workday(self):
        next_workday = self.calculator._next_workday

        with self.assertRaises(AttributeError):
            next_workday(None)

        self.assertEqual(next_workday(datetime(2018, 12, 25)),
                         datetime(2018, 12, 26))
        self.assertEqual(next_workday(datetime(2018, 12, 26)),
                         datetime(2018, 12, 27))
        self.assertEqual(next_workday(datetime(2018, 12, 27)),
                         datetime(2018, 12, 28))
        self.assertEqual(next_workday(datetime(2018, 12, 28)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_workday(datetime(2018, 12, 29)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_workday(datetime(2018, 12, 30)),
                         datetime(2018, 12, 31))
        self.assertEqual(next_workday(datetime(2018, 12, 31)),
                         datetime(2019, 1, 1))

        with self.assertRaises(AttributeError):
            next_workday('asd')

    def test__in_work_hours(self):
        in_work_hours = self.calculator._in_work_hours
        valid_datetime = datetime(2019, 1, 1, 9, 0)
        self.assertTrue(in_work_hours(valid_datetime))

        invalid_datetime = datetime(2019, 1, 1, 8, 59)
        self.assertFalse(in_work_hours(invalid_datetime))

        with self.assertRaises(AttributeError):
            in_work_hours(None)
            in_work_hours(12)
            in_work_hours([])
            in_work_hours({})

        self.assertTrue(in_work_hours(datetime(2019, 1, 1, 17, 0)))
        self.assertFalse(in_work_hours(datetime(2019, 1, 1, 17, 1)))

    def test__add_work_hours(self):
        add_work_hours = self.calculator._add_work_hours

        with self.assertRaises(ValueError):
            add_work_hours(datetime(2019, 12, 12), 8)
            add_work_hours(datetime(2019, 12, 12), 32)

        one_hour = 1
        self.assertEqual(add_work_hours(datetime(2019, 1, 1, 9), one_hour),
                         datetime(2019, 1, 1, 10))
        self.assertEqual(add_work_hours(datetime(2019, 1, 1, 10), one_hour),
                         datetime(2019, 1, 1, 11))
        self.assertEqual(add_work_hours(datetime(2019, 1, 1, 9, 30), one_hour),
                         datetime(2019, 1, 1, 10, 30))
        self.assertEqual(add_work_hours(datetime(2019, 1, 1, 16), one_hour),
                         datetime(2019, 1, 1, 17))
        self.assertEqual(add_work_hours(datetime(2019, 1, 1, 16, 30), one_hour),
                         datetime(2019, 1, 2, 9, 30))

    def test__add_work_days(self):
        add_work_days = self.calculator._add_work_days
        self.assertEqual(add_work_days(datetime(2018, 12, 25), 4),
                         datetime(2018, 12, 31))
        self.assertEqual(add_work_days(datetime(2018, 12, 10), 10),
                         datetime(2018, 12, 24))
        self.assertEqual(add_work_days(datetime(2018, 12, 28), 1),
                         datetime(2018, 12, 31))
        self.assertEqual(add_work_days(datetime(2018, 12, 10), 9),
                         datetime(2018, 12, 21))

    def test_calculate(self):
        do_calculate = self.calculator.calculate

        monday_2pm = datetime(2018, 12, 24, 14, 0)
        two_work_days = 16
        self.assertEqual(do_calculate(monday_2pm, two_work_days),
                         datetime(2018, 12, 26, 14, 0))

        friday_4pm = datetime(2018, 12, 28, 14, 0)
        self.assertEqual(do_calculate(friday_4pm, two_work_days),
                         datetime(2019, 1, 1, 14, 0))

        friday_4_30_pm = datetime(2018, 12, 28, 16, 30)
        self.assertEqual(do_calculate(friday_4_30_pm, 41),
                         datetime(2019, 1, 7, 9, 30))

        monday_5pm = datetime(2018, 12, 24, 17, 0)
        self.assertEqual(do_calculate(monday_5pm, two_work_days),
                         datetime(2018, 12, 26, 17, 0))

        one_month_work_hours = 160
        self.assertEqual(
            do_calculate(datetime(2019, 1, 1, 9, 0), one_month_work_hours),
            datetime(2019, 1, 29, 9, 0))
        self.assertEqual(
            do_calculate(datetime(2019, 1, 8, 9, 0), one_month_work_hours),
            datetime(2019, 2, 5, 9, 0))

        self.assertEqual(
            do_calculate(datetime(2018, 12, 24, 16, 0), 2),
            datetime(2018, 12, 25, 10, 0))


if __name__ == '__main__':
    unittest.main()
