from datetime import date,datetime, timedelta
from typing import Dict ,Optional
from django.db.models import Min, Max,  Q
from cx_Oracle import DatabaseError
from dateutil.relativedelta import relativedelta
from .models.erpModels import ErpWeeklyEnd
from .models.unisModels import (
                     UNISHoliday,
                     UNISHolidayCalendar,
                     UNISEmployee,
                     UNISWorkingShift,
                     UNISWorkingShiftType,
                     UNISTenter
                        )



class Utility:


    @staticmethod
    def get_shift(date: datetime, employee_unis_id : Optional[int], employee_erp_id: str, location: str) -> Optional[UNISWorkingShift]:
        """
        Returns the name of the working shift for the given employee at the given date and location.

        Args:

            date: A datetime object representing the date for which the shift needs to be retrieved.
            employee_unis_id: An optional integer representing the UNIS ID of the employee. If not provided, it will be retrieved using the employee ERP ID.
            employee_erp_id: A string representing the ERP ID of the employee.
            location: A string representing the location for which the shift needs to be retrieved.

        Returns:

            If a weekend shift exists for the employee in the ERP system, it returns the shift object for that weekend.
            If the location has a holiday calendar and today is a holiday, it returns the shift object with code '02'.
            If the employee does not exist in the UNIS system or the shift type object does not exist for the employee, it returns None.
            Otherwise, it calculates the number of spin cycles and the period of days to which they apply. It then finds the position of today's date in the period and returns the shift object for today.
        """

        # Check if the employee has a weekend shift in the ERP system
        erp_weekend_shift = Utility._erp_weekend(date, employee_erp_id)
        if erp_weekend_shift:
            return erp_weekend_shift

        # Check if the location has a holiday calendar
        holiday_calender = UNISHolidayCalendar.objects.using('unisDb').filter(calendar_name__contains=location).first()
        if holiday_calender:
            # Check if today is a holiday
            holiday = UNISHoliday.objects.using('unisDb').filter(calendar_id=holiday_calender.calendar_id,
                                                             effective_date=date).first()
            if holiday:
                return UNISWorkingShift.objects.using('unisDb').get(C_Code='02')

        # Get the employee UNIS id if the employee fingerprint not exists
        if employee_unis_id is None :
            employee_unis_id = UNISTenter.objects.using('unisDb').filter(
                C_Unique=employee_erp_id,
            ).values('L_UID').first()['L_UID']


        # Get the employee object from the UNIS system
        unis_employee = UNISEmployee.objects.using('unisDb').filter(L_UID=employee_unis_id).first()
        if not unis_employee:
            return None

        # Get the shift type object from the UNIS system
        shift_type = UNISWorkingShiftType.objects.using('unisDb').filter(C_Code=unis_employee.C_Work).first()
        if not shift_type:
            return None

        # Calculate the number of spin cycles and the period of days to which they apply
        spin_count = int(shift_type.L_SpinCount) - 1
        basic_day = datetime.strptime(shift_type.C_BasicDay, '%Y%m%d').date()
        today = date
        end_day = basic_day + timedelta(days=spin_count)
        period = Utility._time_range(basic_day, end_day)

        # Find the position of today's date in the period
        while today not in period:
            basic_day = period[spin_count] + timedelta(days=1)
            end_day = basic_day + timedelta(days=spin_count)
            period = Utility._time_range(basic_day, end_day)
        position = period.index(today)

        # Get the code for the shift for today
        day_shift = shift_type.C_ShiftCode
        day_shift_array = [day_shift[i:i + 2] for i in range(0, len(day_shift), 2)]
        shift_obj = UNISWorkingShift.objects.using('unisDb').filter(C_Code=day_shift_array[position]).first()

        return shift_obj

    @staticmethod
    def get_timeIn_timeOut(date: datetime, employee_erp_id: str, shift=None) -> dict:
        """
        Returns the earliest time in and the latest time out of an employee on a given date and shift.

        Args:

            date : A datetime object representing the date for which time in and time out is to be returned.
            employee_erp_id: A string representing the ID of the employee.
            shift (optional): A shift object representing the shift for which time in and time out is to be returned.

        Return:

            A dictionary containing the earliest time in and the latest time out of an employee on a given date and shift.
        """
        times = {'time_in': None, 'time_out': None}

        # Check if shift is provided
        if shift is None:
            return times

        # Parse shift start and end times
        L_RangeTime1 = Utility._parse_unis_time(shift.L_RangeTime1)
        L_RangeTime2 = Utility._parse_unis_time(shift.L_RangeTime2)

        # If shift is for more than 24 hours
        if shift.L_RangeTime2 > 2880:

            # Get the earliest time in for the employee on the given date
            times['time_in'] = UNISTenter.objects.using('unisDb').filter(C_Unique=employee_erp_id, C_Date=date,
                                                                         C_Time__gte=L_RangeTime1).aggregate(
                min_time=Min('C_Time'))['min_time']

            # Get the latest time out for the employee on the given date or the next day if the time is after midnight
            times['time_out'] = UNISTenter.objects.using('unisDb').filter(C_Unique=employee_erp_id).filter(
                Q(C_Date=date) |
                Q(C_Date=date + timedelta(days=1), C_Time__lte=L_RangeTime2)
            ).aggregate(max_time=Max('C_Time'))['max_time']

        # If shift is for less than 24 hours
        elif shift.L_RangeTime2 >= 1440 and shift.L_RangeTime2 <= 2880:

            # Get the earliest time in and latest time out for the employee on the given date
            first_last_fingerprint = UNISTenter.objects.using('unisDb').filter(C_Date=date, C_Unique=employee_erp_id)
            times['time_in'] = first_last_fingerprint.aggregate(min_time=Min('C_Time'))['min_time']
            times['time_out'] = first_last_fingerprint.aggregate(max_time=Max('C_Time'))['max_time']

        return times

    @staticmethod
    def get_shift_period (shift_obj=None) -> Dict[str, str]:
        """
        Returns the start and end time of a shift object.

         Args:

            shift_obj (optional): a shift object that contains information about the shift's time ranges.


        Return:

            A dictionary containing the start and end time of the shift in the format {"shift_start_time": str, "shift_end_time": str}.
        """
        if shift_obj:
            # If the shift has only one time range
            if shift_obj.L_SF1Time1 == 0 and shift_obj.L_SF2Time1 == 0:
                shift_start_time = Utility._parse_unis_time(shift_obj.L_RangeTime1)
                shift_end_time = Utility._parse_unis_time(shift_obj.L_RangeTime2)
            # If the shift has two time ranges
            else:
                shift_start_time = Utility._parse_unis_time(shift_obj.L_SF2Time1)
                shift_end_time = Utility._parse_unis_time(shift_obj.L_SF2Time2)

            # If shift end time is earlier than the shift start time, it means the shift ends on the next day.
            if datetime.strptime(shift_end_time, "%H:%M:%S").time() <= datetime.strptime(shift_start_time,
                                                                                         "%H:%M:%S").time():
                shift_end_time = f"+{str(shift_end_time)}"

            return {
                "shift_start_time": shift_start_time,
                "shift_end_time": shift_end_time,
            }

    @staticmethod
    def get_time_difference(times):
        """
          Args:

            times: a dictionary containing two time objects: time_in and time_out.

        Returns:

           a formatted string representing the time difference between time_out and time_in in hours and minutes. If time_out is None, an empty string is returned.
        Output:

           a string representing the time difference in the format "HH:MM".

        """

        if times['time_out'] is None:
            return ""

        # Combine time objects with a dummy date to create datetime objects
        datetime_in = datetime.combine(date.today(), times['time_in'])
        datetime_out = datetime.combine(date.today(), times['time_out'])

        if datetime_out <= datetime_in:
            datetime_out += timedelta(days=1)

        # Calculate the difference
        diff = datetime_out - datetime_in

        # Convert the timedelta to hours and minutes
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Format the result as H:M
        return f"{hours:02}:{minutes:02}"

    @staticmethod
    def check_late(time_in: str, time_out: str, shift_obj: any, hours: str) -> Optional[str]:

        """
         Determines if an employee was late based on their time in and out, shift information, and hours worked.

         Args:
             time_in: The time the employee clocked in.
             time_out: The time the employee clocked out.
             shift_obj: An object containing shift information.
             hours: The number of hours worked in the shift.

         Returns:
             A string indicating the type of lateness detected, or 'Less than 8 hours' if no lateness was detected but the hours worked were less than 8.
             Returns None if there is no shift object or no time in.
         """
        # if there is no shift object or no time in, return None
        if not shift_obj or not time_in:
            return None

        late_start_time = late_end_time = late = ''

        # If shift start and end times are not provided
        if shift_obj.L_SF2Time1 == 0 and shift_obj.L_SF2Time2 == 0:
            if not time_out:
                return 'Less than 8 hours'
            elif datetime.strptime(hours, '%H:%M:%S') < datetime.strptime('07:50:00', '%H:%M:%S'):
                return 'Less than 8 hours'
            else:
                return None

        # Determine the late start and end times based on the shift object
        if shift_obj.L_LateTime != -1 and shift_obj.L_LackTime != -1:
            late_start_time = Utility._parse_unis_time(shift_obj.L_LateTime)
            late_end_time = Utility._parse_unis_time(shift_obj.L_LackTime)
        elif shift_obj.L_SF2Time1 != 0 and shift_obj.L_SF2Time2 != 0:
            late_start_time = Utility._parse_unis_time(shift_obj.L_SF2Time1)
            late_end_time = Utility._parse_unis_time(shift_obj.L_SF2Time2)
        else:
            late_start_time = Utility._parse_unis_time(shift_obj.L_RangeTime1)
            late_end_time = Utility._parse_unis_time(shift_obj.L_RangeTime2)

        # Convert late start and end times to datetime objects
        late_start_time = datetime.strptime(late_start_time, '%H:%M:%S').time()
        late_end_time = datetime.strptime(late_end_time, '%H:%M:%S').time()

        # Check if time out is on the next day
        if time_out:
            if time_out <= time_in:
                time_out += timedelta(days=1)

        # Check if time in is late
        if time_in and time_in > late_start_time:
            late += 'Late in Morning '

        # Check if time out is late
        if time_out and time_out != 'None' and time_out < late_end_time:
            late += 'Late in Last Hours '

        # If no lateness was detected but hours are less than 8
        if not late and datetime.strptime(hours, '%H:%M:%S') < datetime.strptime('07:50:00', '%H:%M:%S'):
            return 'Less than 8 hours'

        return late


    @staticmethod
    def _parse_unis_time(unis_time: int) -> Optional[str]:

        """
        Converts a given unis time to a string representing the time of day, using the 2018-01-01 date as reference.

        Args:
            unis_time (int): The unis time to convert.

        Returns:
            str or None: A string representing the time of day, in the format 'HH:MM:SS', or None if the input is invalid.
        """


        # Subtract 2880 from the given unis_time if it is greater than or equal to 2880
        # (2880 is equivalent to 2 days or 48 hours)
        if unis_time >= 2880:
            unis_time -= 2880

        # Subtract 1440 from the given unis_time if it is greater than or equal to 1440
        # (1440 is equivalent to 1 day or 24 hours)
        elif unis_time >= 1440:
            unis_time -= 1440

        # Divide the remaining unis_time into hours and minutes
        hours, minutes = divmod(unis_time, 60)

        # Create a datetime object using 2018-01-01 as the date and the calculated hours and minutes
        time = datetime(2018, 1, 1, int(hours), int(minutes), 0)

        # Format the datetime object into a string with the format 'YYYY-MM-DD HH:MM:SS'
        times = time.strftime('%Y-%m-%d %H:%M:%S').split("01 ")

        # Split the resulting string at '01 ' and check if the resulting list has more than 1 element
        if len(times) > 1:
            # Split the second element of the resulting list at '.000000' to remove the microseconds
            time_temp = times[1].split(".000000")
            # Set the resulting string as the time variable
            time = time_temp[0]
        else:
            # Set the time variable as None if the resulting list has only one element
            time = None

        # Return the time as a string or None if it is None
        return time

    @staticmethod
    def _erp_weekend(date: datetime, employee_erp_id: str) -> Optional[str]:

        """
           Given a date and an employee ID, retrieves the ErpWeeklyEnd record from the database for that month,
           and checks if the given date is a weekend day based on the record.

           Args:
               date (datetime): A datetime object representing the date to check.
               employee_erp_id (str): A string representing the employee ID.

           Returns:
               str: A string representing the day of the week if the given date is a weekend day based on the ErpWeeklyEnd record,
                    or None if no record is found for the given date and employee ID.
                    If there's an error while connecting to the database, returns "Error connecting to database".
           """


        # Retrieve the ErpWeeklyEnd object for the given date and employee ID
        try:
            holiday = ErpWeeklyEnd.objects.using('erpDb').get(
                effective_start_date=date.replace(day=1).strftime('%Y-%m-%d'),
                effective_end_date=(date + relativedelta(day=31)).strftime('%Y-%m-%d'),
                employee_number=employee_erp_id
            )
        except ErpWeeklyEnd.DoesNotExist:
            # If no ErpWeeklyEnd object is found for the given date and employee ID, return None
            return None
        except DatabaseError:
            # Handle database connection errors here
            return "Error connecting to database"

        # Create a dictionary mapping week number to a list of days in that week
        week_days = {
            1: [holiday.w1_d1, holiday.w1_d2],
            2: [holiday.w2_d1, holiday.w2_d2],
            3: [holiday.w3_d1, holiday.w3_d2],
            4: [holiday.w4_d1, holiday.w4_d2]
        }

        # Get the week number in the month for the given date
        week_num_in_month = Utility._week_of_month(date)

        # Check if the week number is in the week_days dictionary
        if week_num_in_month in week_days:
            # If the week number is in the dictionary, check if the given date is in the list of days for that week
            return Utility._check_day_in_erp_weekEnd(date.strftime('%A').upper(), week_days[week_num_in_month])
        else:
            # If the week number is not in the dictionary, return None
            return None

    @staticmethod
    def _week_of_month(date: datetime) -> int:
        """
        Returns the week number of the month for a given date.

        Args:

            date: A datetime object representing the date.

        Return:

            An integer representing the week number of the month.
        """
        # Get the first day of the month
        first_day_of_month = date.replace(day=1)

        # Calculate the adjusted day of the month by adding the weekday of the first day of the month
        day_of_month = date.day
        adjusted_day_of_month = day_of_month + first_day_of_month.weekday()

        # Calculate the quotient and remainder of the adjusted day of the month divided by 7
        quotient, remainder = divmod(adjusted_day_of_month, 7)

        # Check if there is a remainder and adjust the week number accordingly
        if remainder > 0:
            week_number = quotient + 1
        else:
            week_number = quotient

        return week_number

    @staticmethod
    def _check_day_in_erp_weekEnd(today_str: str, week_holiday: list) -> str:

        """
                This function checks if the given day is a weekly holiday for the employee, and returns the UNISWorkingShift object representing the holiday shift if it is. The function first checks if the input parameters are valid, and returns None if they are not. Then, it checks if the given day is one of the weekly holidays of the employee by comparing it to the list of week_holiday. If the day is a weekly holiday, the function returns a UNISWorkingShift object representing the holiday shift with code '02' and name 'None'. If the day is not a weekly holiday, the function returns None.

                Args:

                    today_str (str): A string representing the current date in "YYYY-MM-DD" format.
                    week_holiday (list): A list of strings representing the days of the week that the employee has off.

                Return:

                    If the input parameters are not valid, return None.
                    If the given day is one of the weekly holidays of the employee, return a UNISWorkingShift object representing the holiday shift.
                    If the given day is not a weekly holiday, return None.
                """


        # Check if the input parameters are valid or not
        if not isinstance(today_str, str) or not isinstance(week_holiday, list):
            return None

        # Check if the given day is one of the weekly holidays of the employee
        if today_str in week_holiday:
            # If yes, then return a UNISWorkingShift object representing the holiday shift
            shift_obj = UNISWorkingShift.objects.using('unisDb').get(C_Code='02', C_Name='None')
            return shift_obj

        # If the given day is not a weekly holiday, return None
        return None

    @staticmethod
    def _time_range(start_date: datetime, end_date: datetime) -> list:

        """
        This function takes in two datetime objects as input and returns a list of all the dates between the start and end dates, inclusive. It does this by iterating over each date between the two input dates and appending them to a list. Finally, the function returns the list of dates.

         Args:

            start_date (datetime): the starting date of the time range.
            end_date (datetime): the end date of the time range.

         Return:

            A list containing all the dates between start_date and end_date, inclusive.

        """

        # Initialize an empty list to store the date range
        date_list = []

        # While the start date is less than or equal to the end date
        while start_date <= end_date:
            # Add the start date to the list
            date_list.append(start_date)
            # Increment the start date by one day
            start_date += timedelta(days=1)

        # Return the date range list
        return date_list
