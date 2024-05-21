import json
from datetime import datetime
from uuid import UUID

import pandas as pd
from django.db.models import Max, Min
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from glucose.filters import GlucoseLevelFilter
from glucose.models import Device, GlucoseLevel, User
from glucose.paginate import StandardResultsSetPagination
from glucose.serializer import (
    FileUploadSerializer,
    GlucoseLevelMixMaxSerializer,
    GlucoseLevelSerializer,
    UserSerializer,
)


@extend_schema_view(
    create=extend_schema(description="creates data in DB which reads from csv files")
)
class DataViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    @staticmethod
    def process_csv(self, df, csv_file):
        for index, row in df.iterrows():
            user_id = UUID(csv_file.name.split(".")[0])
            user, _ = User.objects.get_or_create(user_id=user_id)
            device_serial_no = row["Seriennummer"]
            device, _ = Device.objects.get_or_create(
                serial_no=device_serial_no,
                defaults={"name": row["Gerät"], "user": user},
            )

            GlucoseLevel.objects.create(
                device=device,
                device_timestamp=timezone.make_aware(
                    pd.to_datetime(row["Gerätezeitstempel"], dayfirst=True)
                ),
                recording_type=row["Aufzeichnungstyp"],
                glucose_value_history=row["Glukosewert-Verlauf mg/dL"],
                glukose_scan_mg_dL=row["Glukose-Scan mg/dL"],
                nicht_numerisches_schnellwirkendes_insulin=row[
                    "Nicht numerisches schnellwirkendes Insulin"
                ],
                schnellwirkendes_insulin=row["Schnellwirkendes Insulin (Einheiten)"],
                nicht_numerische_nahrungsdaten=row["Nicht numerische Nahrungsdaten"],
                kohlenhydrate_gramm=row["Kohlenhydrate (Gramm)"],
                kohlenhydrate_portionen=row["Kohlenhydrate (Portionen)"],
                nicht_numerisches_depotinsulin=row["Nicht numerisches Depotinsulin"],
                depotinsulin=row["Depotinsulin (Einheiten)"],
                notizen=row["Notizen"],
                glukose_teststreifen_mg_dL=row["Glukose-Teststreifen mg/dL"],
                keton_mmol_L=row["Keton mmol/L"],
                mahlzeiteninsulin=row["Mahlzeiteninsulin (Einheiten)"],
                korrekturinsulin=row["Insulin-Änderung durch Anwender (Einheiten)"],
            )

    @extend_schema(request=FileUploadSerializer)
    def create(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_file = serializer.validated_data["file"]
        if not csv_file:
            return Response(
                {"detail": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(
                csv_file,
                low_memory=True,
                encoding="utf-8",
                skiprows=1,
            )
            df = df.fillna(0)
        except Exception as e:
            return Response(
                {"detail": f"Error reading CSV file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        DataViewset.process_csv(self, df, csv_file)

        return Response(
            {"detail": "Data uploaded successfully"}, status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    list=extend_schema(description="Returns lists of glucose levels of user ids"),
    retrieve=extend_schema(description="Retrieves particular glucose level by id"),
    export_to_csv=extend_schema(description="export response to csv format"),
    export_to_json=extend_schema(description="export response to json format"),
)
class LevelViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GlucoseLevelFilter
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name="start_timestamp", type=str),
            OpenApiParameter(name="end_timestamp", type=str),
            OpenApiParameter(name="user_id", type=str),
        ]
    )
    @action(detail=False, methods=["get"])
    def min_max_glucose(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        min_max_levels = queryset.aggregate(
            min_glucose_level=Min("glucose_value_history"),
            max_glucose_level=Max("glukose_scan_mg_dL"),
        )
        serializer = GlucoseLevelMixMaxSerializer(data=min_max_levels)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="start_timestamp", type=str),
            OpenApiParameter(name="end_timestamp", type=str),
            OpenApiParameter(name="user_id", type=str),
        ]
    )
    @action(detail=False, methods=["get"])
    def export_to_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GlucoseLevelSerializer(queryset, many=True)
        df = pd.DataFrame(serializer.data)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="glucose_levels_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"'
        )
        df.to_csv(path_or_buf=response, index=False)
        return response

    @extend_schema(
        parameters=[
            OpenApiParameter(name="start_timestamp", type=str),
            OpenApiParameter(name="end_timestamp", type=str),
            OpenApiParameter(name="user_id", type=str),
        ]
    )
    @action(detail=False, methods=["get"])
    def export_to_json(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GlucoseLevelSerializer(queryset, many=True)
        response_data = json.dumps(serializer.data)
        response = HttpResponse(response_data, content_type="application/json")
        response["Content-Disposition"] = (
            f'attachment; filename="glucose_levels_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"'
        )
        return response
