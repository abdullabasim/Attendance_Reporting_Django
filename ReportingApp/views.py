
from rest_framework.response import Response
from .serializerData import  AttendanceReportSerializer
from .models.appModels import AttendanceReport
from rest_framework import viewsets, mixins
from.paginationData import AttendanceReportPagination
from rest_framework.permissions import IsAuthenticated


class GeneralReportViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
       A ViewSet for handling fetching operation for AttendanceReport objects.

       list:
       Retrieve a paginated list of AttendanceReport objects.
    """
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    pagination_class = AttendanceReportPagination
    permission_classes  = [IsAuthenticated]
    def get_queryset(self):
        """
             Get the queryset for this view. This queryset will be paginated
             and filtered based on query parameters.

             Returns:
                 QuerySet: the filtered queryset
             """
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee_id')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if employee_id:
            queryset = queryset.filter(employee_number=employee_id)

        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def list(self, request, *args, **kwargs):
        """
              List all the AttendanceReport objects. This method will handle pagination
              and return a paginated response if necessary.

              Returns:
                  Response: the paginated response containing the serialized AttendanceReport objects
              """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class NormalLateReportViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
       A ViewSet for handling fetching operation for AttendanceReport objects with late field not null (Normal Late)

       list:
       Retrieve a paginated list of AttendanceReport objects.
    """
    queryset = AttendanceReport.objects.filter(late__isnull=False)
    serializer_class = AttendanceReportSerializer
    pagination_class = AttendanceReportPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
             Get the queryset for this view. This queryset will be paginated
             and filtered based on query parameters.

             Returns:
                 QuerySet: the filtered queryset
             """
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee_id')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if employee_id:
            queryset = queryset.filter(employee_number=employee_id)

        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def list(self, request, *args, **kwargs):
        """
              List all the AttendanceReport objects. This method will handle pagination
              and return a paginated response if necessary.

              Returns:
                  Response: the paginated response containing the serialized AttendanceReport objects
              """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AbsenceReportViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
       A ViewSet for handling fetching operation for AttendanceReport objects with time in field not null (Absence)

       list:
       Retrieve a paginated list of AttendanceReport objects.
    """
    queryset = AttendanceReport.objects.filter(time_in__isnull=True)
    serializer_class = AttendanceReportSerializer
    pagination_class = AttendanceReportPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
             Get the queryset for this view. This queryset will be paginated
             and filtered based on query parameters.

             Returns:
                 QuerySet: the filtered queryset
             """
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee_id')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if employee_id:
            queryset = queryset.filter(employee_number=employee_id)

        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def list(self, request, *args, **kwargs):
        """
              List all the AttendanceReport objects. This method will handle pagination
              and return a paginated response if necessary.

              Returns:
                  Response: the paginated response containing the serialized AttendanceReport objects
              """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)