from datetime import timedelta

# Following threshold values are in 24-hour format
WORK_STARTING_HOUR = 9
WORK_ENDING_HOUR = 17

WORK_HOURS = WORK_ENDING_HOUR - WORK_STARTING_HOUR


class NotWorkHour(Exception):
    """Date time is not within working hours"""


class NotWorkday(Exception):
    """Date time is not within work days"""


class DueDate(object):
    """Dealing with date transformation and due date calculation
    """
    weekdays = (
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        "Sunday")

    workdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

    @classmethod
    def _next_monday(cls, base_date):
        """Determines the next Monday date

        Args:
            base_date: datetime.datetime
        Returns:
           next monday date
        """
        return base_date + timedelta(abs(base_date.weekday() - 7))

    @classmethod
    def _next_workday(cls, date):
        """Determines the next work day

        Args:
             date: datetime.datetime
        Returns:
            date : datetime.datetime, next work day date
        """
        if date.weekday() < 4:
            date = date + timedelta(days=1)
        else:
            date = cls._next_monday(date)
        return date

    @staticmethod
    def _in_work_hours(date):
        """Determines if the current date happens within work time.

        Args:
            date: datetime.datetime
        Returns:
            Boolean indicating whether or not the current date within working
                hours
        """
        return (date.hour == WORK_ENDING_HOUR and date.minute == 0) or \
               (WORK_STARTING_HOUR <= date.hour < WORK_ENDING_HOUR)

    @classmethod
    def _add_work_hours(cls, submit_date, working_hours):
        """
        Args:
            submit_date: datetime.datetime, this date is desired to increase.
            working_hours: int, in hours format. 'submit_date' is going to be
                increased by this working hours.
        Raises:
            ValueError: working_hours has to be less than a day of work.
        Returns:
            finished: datetime.datetime, submitted date + working_hours
            hours equation
        """
        if working_hours >= WORK_HOURS:
            raise ValueError

        finished = submit_date + timedelta(hours=working_hours)

        if cls._in_work_hours(finished):
            return finished
        else:
            day_end_time = submit_date.replace(hour=WORK_ENDING_HOUR, minute=0)
            remaining = day_end_time - timedelta(hours=submit_date.hour,
                                                 minutes=submit_date.minute)

            next_workday = cls._next_workday(submit_date)
            next_workday_date = next_workday.replace(hour=WORK_STARTING_HOUR,
                                                     minute=0)
            finished = next_workday_date + timedelta(hours=remaining.hour,
                                                     minutes=remaining.minute)
            return finished

    @classmethod
    def _add_work_days(cls, date, workdays):
        """Increasing the given date by workdays.

        Args:
            date : datetime.datetime, this date is desired to increase.
            workdays : int, 'date' will be increased by these days.
        Returns:
            date : datetime.datetime, date + workdays
        """
        for _ in range(workdays):
            date = cls._next_workday(date)
        return date

    @classmethod
    def calculate(cls, submit_date, working_hours):
        """Preforms the due date calculation.

        bug is resolved when -> done_datetime = submit_date + working_hours

        Args:
            submit_date : datetime.datetime, when the bug has been created
            working_hours : int, in hours format. Working hours on the current
                bug.
        Raises:
            NotWorkday: if the submitted date happened not on work day.
            NotWorkHour: if the submitted date happened not within work hours.

        Returns:
            done_datetime: datetime.datetime, when the bug has been resolved
        """
        submit_hour = submit_date.hour
        submit_day = submit_date.weekday()
        submit_day_string = cls.weekdays[submit_day]

        if submit_day_string not in cls.workdays:
            raise NotWorkday
        if not (WORK_STARTING_HOUR <= submit_hour <= WORK_ENDING_HOUR):
            raise NotWorkHour

        worked_days = working_hours // WORK_HOURS
        worked_hours = working_hours % WORK_HOURS

        done_date = cls._add_work_days(submit_date, worked_days)
        done_datetime = cls._add_work_hours(done_date, worked_hours)

        return done_datetime
