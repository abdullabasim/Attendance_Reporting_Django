from django.db import models

class UNISTenter(models.Model):

    C_Date = models.DateField()
    C_Time = models.TimeField()
    L_UID = models.CharField(max_length=200)
    C_Name = models.CharField(max_length=200)

    C_Unique = models.CharField(max_length=10)
    C_Office = models.CharField(max_length=200)
    C_Post = models.CharField(max_length=200)
    created = models.CharField(max_length=200)



    class Meta:
        managed = False
        db_table = 'tenter'

class UNISTechException(models.Model):
            employee_Id = models.CharField(max_length=200)
            C_Date = models.DateField()
            body = models.CharField(max_length=200)
            created_at = models.CharField(max_length=200)
            updated_at = models.CharField(max_length=10)


            class Meta:
                managed = False
                db_table = 'tech_exception'

class UNISExceptionEmployeeList(models.Model):
    C_Unique = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'exception_id'

class UNISAttendanceExceptation(models.Model):
    employee_Id = models.CharField(max_length=200)
    justification = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    exception_type = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'exceptation'

class UNISPaComment(models.Model):
    employee_Id = models.CharField(max_length=200)
    C_Date = models.DateField()
    comment = models.CharField(max_length=200)


    class Meta:
        managed = False
        db_table = 'pa_comment_v2'

class UNISHolidayCalendar(models.Model):
    calendar_id = models.IntegerField()
    calendar_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'calendars'

class UNISHoliday(models.Model):
        holiday_id = models.IntegerField()
        calendar_id = models.CharField(max_length=200)
        effective_date = models.DateField()
        holiday_name = models.CharField(max_length=200)

        class Meta:
            managed = False
            db_table = 'holidays'

class UNISWorkingShift(models.Model):
    C_Code = models.CharField(max_length=200)
    C_Name = models.CharField(max_length=200)
    L_InoutMode = models.IntegerField()
    L_RangeTime1 = models.IntegerField()
    L_RangeTime2 = models.IntegerField()
    L_IgnoreAbsent = models.IntegerField()
    L_MultiRange = models.IntegerField()
    L_LateTime = models.IntegerField()
    L_LackTime = models.IntegerField()
    L_AutoInTime = models.IntegerField()
    L_AutoOutTime = models.IntegerField()
    L_Range1TM1 = models.IntegerField()
    L_Range1TM2 = models.IntegerField()
    L_Range2TM1	 = models.IntegerField()

    L_Range2TM2 = models.IntegerField()
    L_Range3TM1 = models.IntegerField()
    L_Range3TM2 = models.IntegerField()
    L_Range4TM1 = models.IntegerField()
    L_Range4TM2 = models.IntegerField()
    L_ExceptExit = models.IntegerField()
    L_ExceptRtnMode = models.IntegerField()
    L_ExceptOut = models.IntegerField()
    L_ExceptInMode = models.IntegerField()
    L_Except1TM1 = models.IntegerField()
    L_Except1TM2 = models.IntegerField()

    L_Except2TM1 = models.IntegerField()
    L_Except2TM2 = models.IntegerField()
    L_Except3TM1 = models.IntegerField()
    L_Except3TM2 = models.IntegerField()
    L_Except4TM1 = models.IntegerField()
    L_Except4TM2 = models.IntegerField()
    L_Except5TM1 = models.IntegerField()
    L_Except5TM2 = models.IntegerField()

    L_SF1Work = models.IntegerField()
    L_SF1Time1 = models.IntegerField()
    L_SF1Time2 = models.IntegerField()
    L_SF1Range = models.IntegerField()
    L_SF1AutoOut = models.IntegerField()

    L_SF1Unit = models.IntegerField()
    L_SF1Min = models.IntegerField()
    L_SF1Max = models.IntegerField()
    L_SF1Rate = models.IntegerField()
    L_SF2Work = models.IntegerField()
    L_SF2Time1 = models.IntegerField()

    L_SF2Time2 = models.IntegerField()
    L_SF2Range = models.IntegerField()
    L_SF2AutoOut = models.IntegerField()
    L_SF2Unit = models.IntegerField()
    L_SF2Min = models.IntegerField()
    L_SF2Max = models.IntegerField()

    L_SF2Rate = models.IntegerField()
    L_SF3Work = models.IntegerField()
    L_SF3Type = models.IntegerField()
    L_SF3Time1 = models.IntegerField()
    L_SF3Time2 = models.IntegerField()
    L_SF3Range = models.IntegerField()
    L_SF3AutoOut = models.IntegerField()

    L_SF3Unit = models.IntegerField()
    L_SF3Min = models.IntegerField()
    L_SF3Max = models.IntegerField()
    L_SF3Rate = models.IntegerField()
    L_SF4Work = models.IntegerField()
    L_SF4Type = models.IntegerField()
    L_SF4Time1 = models.IntegerField()

    L_SF4Time2 = models.IntegerField()
    L_SF4Range = models.IntegerField()
    L_SF4AutoOut = models.IntegerField()
    L_SF4Unit = models.IntegerField()
    L_SF4Min = models.IntegerField()
    L_SF4Max = models.IntegerField()
    L_SF4Rate = models.IntegerField()

    L_SF5Work = models.IntegerField()
    L_SF5Type	 = models.IntegerField()
    L_SF5Time1 = models.IntegerField()
    L_SF5Time2 = models.IntegerField()
    L_SF5Range = models.IntegerField()
    L_SF5AutoOut = models.IntegerField()
    L_SF5Unit = models.IntegerField()

    L_SF5Min = models.IntegerField()
    L_SF5Max = models.IntegerField()
    L_SF5Rate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wworkshift'

class UNISEmployee(models.Model):
        L_UID = models.IntegerField()
        C_Work = models.CharField(max_length=200)


        class Meta:
            managed = False
            db_table = 'temploye'


class UNISWorkingShiftType(models.Model):
    C_Code = models.CharField(max_length=200)
    C_Name = models.CharField(max_length=200)
    C_BasicDay = models.CharField(max_length=200)
    L_SpinCount = models.CharField(max_length=200)
    C_ShiftCode = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tworktype'