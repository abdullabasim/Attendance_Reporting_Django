from rest_framework.pagination import PageNumberPagination

class AttendanceReportPagination(PageNumberPagination):
    page_size = 10  # number of records to be displayed per page
    page_size_query_param = 'page_size'
    max_page_size = 100