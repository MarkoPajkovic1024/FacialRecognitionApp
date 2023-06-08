"""
Views for the patients APIs
"""
from distutils.command.upload import upload
from typing import Generic
from rest_framework import (
    viewsets,
    mixins,
    status,
    generics,
    
)
from rest_framework.generics import GenericAPIView,CreateAPIView

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from core.models import (
    Image_File,
    Patients,
    Tag,
    Treatment,
)
from patients import serializers

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'treatments',
                OpenApiTypes.STR,
                description='Comma separated list of treatment IDs to filter',
            ),
        ]
    )
)


class AllPatientsViewSet(viewsets.ModelViewSet):
    """View for All manage patients APIs."""
    serializer_class = serializers.AllPatientSerializer
    queryset = Patients.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @action(methods = ['GET'],detail = True,url_path = 'get_images')
    def get_images(self,request,*args, **kwargs):
        patients = self.get_object()
        serializer = serializers.PatientsImageListSerializer(patients,data = request.data)
        if serializer.is_valid():
            context = serializer.data
            return Response(context,status = status.HTTP_201_CREATED)


class PatientsViewSet(viewsets.ModelViewSet):
    """View for manage patients APIs."""
    serializer_class = serializers.PatientsDetailSerializer
    queryset = Patients.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipatientspes for authenticated user."""
        tags = self.request.query_params.get('tags')
        treatment = self.request.query_params.get('treatment')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if treatment:
            treatmen_ids = self._params_to_ints(treatment)
            queryset = queryset.filter(treatment__id__in=treatmen_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
          return serializers.PatientsSerializer
        elif self.action == 'upload_image':
          return serializers.PatientsImageListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new patients."""
        serializer.save(user=self.request.user)


    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, *args, **kwargs):
        """Upload an image to patients."""
        
        files = request.FILES.getlist('image_lists')
        uploaded_images = []
        if files:
            request.data.pop('image_lists')
        for file in files:
               content = Image_File.objects.create(user=self.request.user ,image=file)
               uploaded_images.append(content)

        patients = self.get_object()
        serializer = serializers.PatientsImageListSerializer(patients,data = request.data)
        if serializer.is_valid():
            patients.image_lists.add(*uploaded_images)
            patients.save()
            context = serializer.data
            return Response(context,status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to patients.',
            ),
        ]
    )
)

class BasePatientsAttrViewSet(mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(patients__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BasePatientsAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class TreatmentViewSet(BasePatientsAttrViewSet):

    """Manage treatment in the database."""
    serializer_class = serializers.TreatmentSerializer
    queryset = Treatment.objects.all()



