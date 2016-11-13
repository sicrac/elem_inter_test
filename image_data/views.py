import os
from django.db.models import Q
from django.http.response import HttpResponse
from rest_framework import decorators
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from image_data import models
from image_data import serializers


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def index(request):
    """
    List all images. An optional `search` parameters may be passed as a query string argument, it will be
    used to search against "title" and "description" in OR condition.

    :param request: current request [rest_framework.request.Request]
    :return:
    """
    search = request.query_params.get('search', '').strip()
    condition = Q(title__icontains=search) | Q(description__icontains=search) if search else Q()
    serializer = serializers.DataEntrySerializer(models.ImageData.objects.filter(condition), many=True)
    return Response(serializer.data)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def image_raw(request, pk):
    """
    Returns the binary data of the image with id `pk`.

    :param request: current request [rest_framework.request.Request]
    :param pk: image id [int]
    :return: image raw data [django.http.response.HttpResponse]
    """
    try:
        image = models.ImageData.objects.get(pk=pk)
        if not hasattr(image.image, 'path'):
            return Response(status=status.HTTP_404_NOT_FOUND)
        extension = os.path.splitext(image.image.name)[1][1:]
        return HttpResponse(image.image, content_type="image/%s" % extension)
    except models.ImageData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
