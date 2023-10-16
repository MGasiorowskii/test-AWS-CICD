from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import PhotoSerializer, CreateUpdateSerializer
from .models import Photo
from .utils import import_data_from_api, import_data_from_file, save_photos, update_photo


class PhotosViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    action_serializers = {
        'update': CreateUpdateSerializer,
        'create': CreateUpdateSerializer,
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(PhotosViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        save_photos([serializer.data])

    def perform_update(self, serializer):
        if serializer.validated_data.get('url'):
            update_photo([serializer.validated_data], self.kwargs['pk'])
        else:
            serializer.save()

    @action(detail=False, methods=['get'], url_path="import/api", url_name='import-api')
    def import_photos_from_api(self, request, *args, **kwargs):
        import_data_from_api()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="import/json", url_name='import-json')
    def import_photos_from_file(self, request, *args, **kwargs):
        import_data_from_file()
        return Response(status=status.HTTP_200_OK)
