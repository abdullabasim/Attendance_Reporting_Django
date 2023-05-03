from django.db import models

class ErpEmployee(models.Model):
    person_id =  models.CharField(primary_key=True, serialize=False, verbose_name='ID',max_length=200)
    employee_number = models.CharField(max_length=32,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    full_name_a = models.CharField(max_length=200)
    current_employee_flag = models.CharField(max_length=10)
    email_address = models.CharField(max_length=200)
    hire_date = models.DateField()
    actual_termination_date = models.DateField(null=True)
    organization_name = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    supervisor_employee_number = models.CharField(max_length=255)
    supervisor_full_name = models.CharField(max_length=255)
    supervisor_email_address = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    grade_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    location_code = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'XX_HR_ZIQ_EMPLOYEES_MV'

class ErpWeeklyEnd(models.Model):

            employee_number = models.CharField(primary_key=True,max_length=200)
            effective_start_date = models.DateField()
            effective_end_date = models.DateField()
            w1_d1 = models.CharField(max_length=200)
            w1_d2 = models.CharField(max_length=200)

            w2_d1 = models.CharField(max_length=200)
            w2_d2 = models.CharField(max_length=200)

            w3_d1 = models.CharField(max_length=200)
            w3_d2 = models.CharField(max_length=200)

            w4_d1 = models.CharField(max_length=200)
            w4_d2 = models.CharField(max_length=200)
            creation_date = models.DateTimeField()

            class Meta:
                managed = False
                db_table = 'XX_HR_INT_ZIQ_WEEKENDS_V'

class ErpAbsences(models.Model):

    person_id = models.CharField(primary_key=True, serialize=False, verbose_name='ID', max_length=200)
    employee_number = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField()
    absence_days = models.CharField(max_length=200)
    time_start = models.TimeField()
    time_end = models.TimeField()
    absence_hours = models.CharField(max_length=200)
    absence_attendance_type = models.CharField(max_length=200)
    absence_category = models.CharField(max_length=200)
    approved_flag = models.CharField(max_length=5)
    creation_date = models.DateTimeField()


    creation_date = models.DateTimeField()


    class Meta:
        managed = False
        db_table = 'XX_HR_ZIQ_ABSENCES_MV'