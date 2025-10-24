from rest_framework import serializers
from .models import Organization, Branch, Agency, AgencyFiles, AgencyContact


class BranchSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name", read_only=True
    )

    class Meta:
        model = Branch
        exclude = ["user"]


class OrganizationSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        exclude = ["user"]


class AgencyFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyFiles
        exclude = ["agency"]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        validated_data["id"] = data.get("id")
        return validated_data


class AgencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyContact
        exclude = ["agency"]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        validated_data["id"] = data.get("id")
        return validated_data


class AgencySerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    files = AgencyFilesSerializer(many=True, required=False)
    contacts = AgencyContactSerializer(many=True, required=False)
    

    class Meta:
        model = Agency
        fields = "__all__"

    def create(self, validated_data):
        files_data = validated_data.pop("files", [])
        contacts_data = validated_data.pop("contacts", [])
        agency = Agency.objects.create(**validated_data)

        for file_data in files_data:
            AgencyFiles.objects.create(agency=agency, **file_data)
        for contact_data in contacts_data:
            AgencyContact.objects.create(agency=agency, **contact_data)

        return agency

    def update(self, instance, validated_data):
        files_data = validated_data.pop("files", [])
        contacts_data = validated_data.pop("contacts", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle files
        existing_file_ids = [file["id"] for file in files_data if "id" in file]
        current_files = instance.files.all()

        # Delete files not included
        for file in current_files:
            if file.id not in existing_file_ids:
                file.delete()

        # Update or create
        for file_data in files_data:
            file_id = file_data.pop("id", None)
            if file_id:
                try:
                    file_instance = AgencyFiles.objects.get(id=file_id, agency=instance)
                    for attr, value in file_data.items():
                        setattr(file_instance, attr, value)
                    file_instance.save()
                except AgencyFiles.DoesNotExist:
                    continue  # or raise error
            else:
                AgencyFiles.objects.create(agency=instance, **file_data)
        # Handle contacts
        instance.contacts.all().exclude(
            id__in=[c.get("id") for c in contacts_data if "id" in c]
        ).delete()
        for contact_data in contacts_data:
            contact_id = contact_data.pop("id", None)
            if contact_id:
                AgencyContact.objects.filter(id=contact_id, agency=instance).update(
                    **contact_data
                )
            else:
                AgencyContact.objects.create(agency=instance, **contact_data)
        return instance
