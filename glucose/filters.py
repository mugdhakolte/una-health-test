import django_filters

from glucose.models import GlucoseLevel


class GlucoseLevelFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(field_name="device__user__user_id")
    start_timestamp = django_filters.DateTimeFilter(
        field_name="device_timestamp", lookup_expr="gte"
    )
    end_timestamp = django_filters.DateTimeFilter(
        field_name="device_timestamp", lookup_expr="lte"
    )

    class Meta:
        model = GlucoseLevel
        fields = ["user_id", "start_timestamp", "end_timestamp"]
