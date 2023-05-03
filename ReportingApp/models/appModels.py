from django.db import models


class EmployeeInfo(models.Model):

    full_name = models.CharField(max_length=255)
    full_name_ar = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    supervisor_full_name = models.CharField(max_length=255)
    supervisor_email_address = models.EmailField()
    location_code = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'employee_info'

class EmployeeAbsences(models.Model):

    absence_creation_date = models.DateField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    absence_days = models.CharField(max_length=100,null=True)
    start_time = models.CharField(max_length=100,null=True)
    end_time = models.CharField(max_length=100,null=True)
    absence_hours = models.CharField(max_length=200,null=True)
    absence_type = models.CharField(max_length=100,null=True)
    absence_category = models.CharField(max_length=100,null=True)
    absence_approved = models.CharField(max_length=255,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'employee_absences'

class AttendanceReport(models.Model):

            employee_number = models.CharField(max_length=50)
            date = models.DateField(max_length=200)
            time_in = models.CharField(max_length=100,null=True)
            time_out = models.CharField(max_length=100,null=True)
            working_hours = models.CharField(max_length=100,null=True)
            shift = models.CharField(max_length=200,null=True)
            shift_start_date = models.CharField(max_length=100,null=True)
            shift_end_date = models.CharField(max_length=100,null=True)
            late = models.CharField(max_length=255,null=True)
            exception_type = models.CharField(max_length=255,null=True)
            justification = models.CharField(max_length=255,null=True)
            tech_exception = models.CharField(max_length=255,null=True)
            pa_comment = models.CharField(max_length=255,null=True)
            employee_info = models.OneToOneField(EmployeeInfo, related_name='employeeinfo',unique=False,
                                                     on_delete=models.CASCADE)
            employee_absences = models.OneToOneField(EmployeeAbsences, related_name='employeeabsence',unique=False, null=True,
                                                     on_delete=models.CASCADE)
            created_at = models.DateTimeField(auto_now_add=True)


            class Meta:
                managed = True
                db_table = 'attendance_report'

            def __str__(self):
                return f"{self.full_name} ({self.employee_number})"