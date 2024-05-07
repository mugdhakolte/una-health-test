import pandas as pd

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from glucose.serializer import UserSerializer, GlucoseLevelSerializer
from glucose.models import User, Device, GlucoseLevel
from glucose.paginate import StandardResultsSetPagination
from glucose.filters import GlucoseLevelFilter


class DataViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        creates data in DB which reads from csv files
    """

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"detail": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(
                csv_file,
                encoding="utf-8",
                skiprows=1,
            )
            df = df.fillna(0)
        except Exception as e:
            return Response(
                {"detail": f"Error reading CSV file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for index, row in df.iterrows():
            user_id = csv_file.name.split(".")[0]
            user, _ = User.objects.get_or_create(user_id=user_id)
            device_serial_no = row["Seriennummer"]
            device, _ = Device.objects.get_or_create(
                serial_no=device_serial_no,
                defaults={"name": row["Gerät"], "user": user},
            )

            GlucoseLevel.objects.create(
                device=device,
                device_timestamp=pd.to_datetime(row["Gerätezeitstempel"]),
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

        return Response(
            {"detail": "Data uploaded successfully"}, status=status.HTTP_201_CREATED
        )


class LevelViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    list:
        Returns lists of glucose levels of user ids

    retrieve:
        Retrieves particular glucose level by user id
    """

    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GlucoseLevelFilter
    pagination_class = StandardResultsSetPagination
