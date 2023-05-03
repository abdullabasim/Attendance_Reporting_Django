from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'general-report', views.GeneralReportViewSet)
router.register(r'normalLate-report', views.NormalLateReportViewSet)
router.register(r'absence-report', views.AbsenceReportViewSet)

urlpatterns = [
      path('', include(router.urls)),
      path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]