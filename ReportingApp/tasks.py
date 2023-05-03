from .models.unisModels import (UNISTenter,
                     UNISTechException,
                     UNISExceptionEmployeeList,
                     UNISAttendanceExceptation,
                     UNISPaComment,
                        )
from .models.erpModels import  (
                            ErpEmployee,
                            ErpAbsences,

                            )
from .models.appModels import (
                            EmployeeInfo,
                            EmployeeAbsences,
                            AttendanceReport
                            )

from datetime import date
from .utility import Utility

def attendance_report_generator():
    """
    This function generates an attendance report for employees for the current date . It is triggered by a cron job that runs twice every day at 06:00 and 16:00
    """

    current_date = date.today()

    # Get the list of employees who are not in the exceptions list and whose hire date is on or before the current date.
    exceptions_unis_employee = list(
        UNISExceptionEmployeeList.objects.using('unisDb')
            .values_list('C_Unique', flat=True)
    )

    employees = ErpEmployee.objects.using('erpDb').filter(
        hire_date__lte=current_date
    ).exclude(
        employee_number__in=exceptions_unis_employee
    )

    # For each employee, get their fingerprint data, exception information, comments, shift information, and absence information.
    for employee in employees:

        # Get the fingerprint data for the current date.
        finger_print_data = UNISTenter.objects.using('unisDb').filter(
            C_Unique=employee.employee_number,
            C_Date=current_date
        ).order_by('C_Time').first()

        # Get the most recent exception object for the employee that includes the exception type and justification.
        exception_obj = UNISAttendanceExceptation.objects.using('unisDb').filter(
            employee_Id=employee.employee_number,
            start_date__lte=current_date,
            end_date__gte=current_date
        ).order_by('-id').values(
            'exception_type',
            'justification'
        ).first()

        # Get the comment object for the employee that includes the PA comment.
        pa_comment_obj = UNISPaComment.objects.using('unisDb').filter(
            employee_Id=employee.employee_number,
            C_Date=current_date
        ).values('comment').first()

        # Get the comment object for the employee that includes the tech exception comment.
        tech_comment_obj = UNISTechException.objects.using('unisDb').filter(
            employee_Id=employee.employee_number,
            C_Date=current_date
        ).values('body').first()

        # Set some initial values to None for the shift object, shift period, working hours, late details, times in/out, employee absences, and L_UID.
        shift_obj, shift_period, working_hours, late_details, times_in_out, employee_absences, l_uid = None, None, None, None, None, None, None

        # Get the shift object for the current date based on the fingerprint data, employee number, and location code.
        shift_obj = Utility.get_shift(
            current_date,
            finger_print_data.L_UID if finger_print_data else None,
            employee.employee_number,
            employee.location_code
        )

        # Get the shift period based on the shift object.
        shift_period = Utility.get_shift_period(shift_obj)

        # If there is fingerprint data available for the employee, get the times in/out and working hours based on the fingerprint data and shift object.
        if finger_print_data:
            times_in_out = Utility.get_timeIn_timeOut(
                current_date,
                employee.employee_number,
                shift_obj
            )

            working_hours = Utility.get_time_difference(times_in_out)

            # Get the late details based on the times in/out, shift object, and working hours.
            late_details = Utility.check_late(
                times_in_out['time_in'],
                times_in_out['time_out'],
                shift_obj,
                working_hours
            )

        # Get or create an EmployeeInfo object for the employee.
        employee_info, created = EmployeeInfo.objects.get_or_create(
            full_name=employee.full_name,
            full_name_ar=employee.full_name_a,
            email=employee.email_address,
            mobile=employee.mobile,
            nationality=employee.nationality,
            date_of_birth=employee.date_of_birth,
            position=employee.position_name,
            grade=employee.grade_name,
            organization=employee.organization_name,
            division=employee.division,
            department=employee.department,
            section=employee.section,
            religion=employee.religion,
            supervisor_full_name=employee.supervisor_full_name,
            supervisor_email_address=employee.supervisor_email_address,
            location_code=employee.location_code,

        )
        # Get  an Employee Absences object for the employee based on current date and employee number.
        absence = ErpAbsences.objects.using('erpDb').filter(employee_number=employee.employee_number,
                                                            date_start__gte=current_date,
                                                            date_end__lte=current_date).first()

        if absence is not None:
            # Get or create an EmployeeAbsences object for the employee.
            employee_absences, created = EmployeeAbsences.objects.get_or_create(
                absence_creation_date=absence.creation_date,
                start_date=absence.date_start,
                end_date=absence.date_end,
                absence_days=absence.absence_days,
                start_time=absence.time_start,
                end_time=absence.time_end,
                absence_hours=absence.absence_hours,

                absence_type=absence.absence_attendance_type,
                absence_category=absence.absence_category,
                absence_approved=absence.approved_flag,

            )
        # Get or create an AttendanceReport object for the employee.
        employee_attendance, created = AttendanceReport.objects.get_or_create(
            employee_number=employee.employee_number,
            date=current_date,
            time_in = times_in_out.get('time_in') if times_in_out else None,
            time_out= times_in_out.get('time_out') if times_in_out else None,
            working_hours= working_hours,
            shift=shift_obj.C_Name if shift_obj else None,
            shift_start_date= shift_period.get('shift_start_time') if shift_period else None,
            shift_end_date= shift_period.get('shift_end_time') if shift_period else None,
            late=late_details,
            exception_type= exception_obj.get('exception_type') if exception_obj else None,
            justification= exception_obj.get('justification') if exception_obj else None,
            tech_exception= tech_comment_obj.get('body') if tech_comment_obj else None,
            pa_comment= pa_comment_obj.get('comment') if pa_comment_obj else None,
            employee_info= employee_info,
            employee_absences= employee_absences,

        )