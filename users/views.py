from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    GroupSerializer,
    PermissionSerializer,
    UserSerializer,
)
from .models import PermissionExtension


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id", None)
        branch_id = self.request.query_params.get("branch_id", None)
        query_filters = Q()
        if organization_id:
            query_filters &= Q(organizations=organization_id)
        if branch_id:
            query_filters &= Q(branches=branch_id)
        queryset = User.objects.filter(query_filters)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id", None)
        type = self.request.query_params.get("type", None)

        query_filters = Q()
        if organization_id:
            query_filters &= Q(extended__organization_id=organization_id)
        if type:
            query_filters &= Q(extended__type=type)
        queryset = Group.objects.filter(query_filters)
        return queryset


class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer

    def get_queryset(self):
        queryset = Permission.objects.all().select_related("extended")
        content_type_id = self.request.query_params.get("content_type")
        page_type = self.request.query_params.get("page_type")
        if page_type:
            queryset = queryset.filter(extended__type=page_type)
        if content_type_id:
            queryset = queryset.filter(content_type_id=content_type_id)
        return queryset


class PermissionGroupedByTypeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        grouped_permissions = PermissionExtension.objects.values("type").distinct()
        result = {}
        for group in grouped_permissions:
            type_name = group["type"]
            permissions = Permission.objects.filter(extended__type=type_name).values()
            permission_list = list(permissions)
            result[type_name] = permission_list
        return Response(result, status=status.HTTP_200_OK)


class UserPermissionsAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_permissions = user.user_permissions.all()
        group_permissions = Permission.objects.filter(group__user=user)

        permissions = list(user_permissions) + list(group_permissions)
        permissions = list(set(permissions))

        permission_codename = [permission.codename for permission in permissions]

        return Response({"permissions": permission_codename}, status=status.HTTP_200_OK)


class UploadPermissionsFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload handling

    def post(self, request):
        """
        Accepts a .txt file, reads permission codenames, generates names, and creates permissions.
        """
        uploaded_file = request.FILES.get("file")  # Expecting a file field named 'file'

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not uploaded_file.name.endswith(".txt"):
            return Response(
                {"error": "Invalid file type. Please upload a .txt file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        codenames = [
            line.decode("utf-8").strip() for line in uploaded_file if line.strip()
        ]

        if not codenames:
            return Response(
                {"error": "File is empty or invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

            # Dummy content type for now
        created_permissions = []
        for codename in codenames:
            name = codename.replace("_", " ").title()  # Convert to proper name format
            last_word = name.split()[-1]
            # Check if permission already exists
            permission, created = Permission.objects.get_or_create(
                codename=codename, content_type_id=4, defaults={"name": name}
            )
            if created or permission:
                # Create associated PermissionExtension
                PermissionExtension.objects.create(
                    permission=permission, type=last_word
                )

                created_permissions.append(
                    {"codename": codename, "name": name, "type": last_word}
                )

            if created:
                created_permissions.append({"codename": codename, "name": name})

        return Response(
            {
                "message": "Permissions created successfully.",
                "permissions": created_permissions,
            },
            status=status.HTTP_201_CREATED,
        )
