import django_filters

from glucose.models import GlucoseLevel


class GlucoseLevelFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(
        field_name="device__user__user_id",
        help_text="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    )
    start_timestamp = django_filters.DateTimeFilter(
        field_name="device_timestamp",
        lookup_expr="gte",
        help_text="2021-02-14 16:50:00+00:00",
    )
    end_timestamp = django_filters.DateTimeFilter(
        field_name="device_timestamp",
        lookup_expr="lte",
        help_text="2021-02-25 17:08:00+00:00",
    )

    class Meta:
        model = GlucoseLevel
        fields = ["user_id", "start_timestamp", "end_timestamp"]
