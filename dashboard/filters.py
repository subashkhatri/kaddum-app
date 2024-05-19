import django_filters
from .models import DairyRecord, DayTracking, CostTracking, WeeklyReportList
from .models_resource_cost import ResourceCost

class DayTrackingFilter(django_filters.FilterSet):
     