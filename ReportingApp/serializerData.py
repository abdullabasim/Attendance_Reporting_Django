from rest_framework import serializers
from .models.appModels import (
                            EmployeeInfo,
                            EmployeeAbsences,
                            AttendanceReport
                            )
from datetime import datetime


class EmployeeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeInfo
        exclude = ['id','created_at']

class EmployeeAbsencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeAbsences
        exclude = ['id']

class AttendanceReportSerializer(serializers.ModelSerializer):
    employee_details = EmployeeInfoSerializer(source='employee_info',many=False)
    absence_details = EmployeeAbsencesSerializer(source='employee_absences',many=False)
    employee_id = serializers.DateTimeField(source='employee_number', read_only=True)



    class Meta:
        model = AttendanceReport
        fields = [ 'employee_id', 'date', 'time_in', 'time_out', 'working_hours', 'late', 'shift',
                  'shift_start_date', 'shift_end_date', 'exception_type', 'justification', 'tech_exception',
                  'pa_comment', 'absence_details', 'employee_details', 'created_at']


    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        if date_from:
            try:
                datetime.strptime(date_from, '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Invalid date format for date_from. Use YYYY-MM-DD")

        if date_to:
            try:
                datetime.strptime(date_to, '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Invalid date format for date_to. Use YYYY-MM-DD")

        return data



