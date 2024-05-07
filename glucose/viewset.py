from rest_framework import viewsets, mixins


class DataViewset(mixins.CreateModelMixin):
    """
    create:
        creates data in DB which reads from csv files
    """

    pass


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

    pass
