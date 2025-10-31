# Serializer for PaxMovement
from rest_framework import serializers
from .models import PaxMovement, UniversalRegistration
from django.db import transaction

class PaxMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaxMovement
        fields = '__all__'


TYPE_REQUIRED_FIELDS = {
    "organization": ["name"],
    "branch": ["name", "parent"],
    "agent": ["name", "parent"],
    "employee": ["name", "parent"],
}


class UniversalRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversalRegistration
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_email(self, value):
        if not value:
            return value
        qs = UniversalRegistration.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already registered for another entity.")
        return value

    def validate(self, data):
        t = data.get("type") or getattr(self.instance, "type", None)
        parent = data.get("parent") or getattr(self.instance, "parent", None)

        # Basic type validation
        if t not in [c[0] for c in UniversalRegistration.TYPE_CHOICES]:
            raise serializers.ValidationError({"type": "Invalid type"})

        # Parent type constraints
        if t == UniversalRegistration.TYPE_BRANCH:
            if not parent:
                raise serializers.ValidationError({"parent": "Branch must have an organization parent"})
            if parent.type != UniversalRegistration.TYPE_ORGANIZATION:
                raise serializers.ValidationError({"parent": "Branch parent must be an organization"})

        if t == UniversalRegistration.TYPE_AGENT:
            if not parent:
                raise serializers.ValidationError({"parent": "Agent must have a branch parent"})
            if parent.type != UniversalRegistration.TYPE_BRANCH:
                raise serializers.ValidationError({"parent": "Agent parent must be a branch"})

        if t == UniversalRegistration.TYPE_EMPLOYEE:
            if not parent:
                raise serializers.ValidationError({"parent": "Employee must have an organization or branch parent"})
            if parent.type not in [
                UniversalRegistration.TYPE_ORGANIZATION,
                UniversalRegistration.TYPE_BRANCH,
                UniversalRegistration.TYPE_AGENT,
            ]:
                raise serializers.ValidationError({"parent": "Employee parent must be organization, branch, or agent"})

        # Enforce required fields per type
        required = TYPE_REQUIRED_FIELDS.get(t, [])
        missing = [f for f in required if not data.get(f) and not getattr(self.instance, f, None)]
        if missing:
            raise serializers.ValidationError({"missing_fields": missing})

        return data

    def create(self, validated_data):
        # Auto-fill organization_id and branch_id based on parent linkage
        parent = validated_data.get("parent")
        if parent:
            if parent.type == UniversalRegistration.TYPE_ORGANIZATION:
                validated_data.setdefault("organization_id", parent.id)
            elif parent.type == UniversalRegistration.TYPE_BRANCH:
                validated_data.setdefault("branch_id", parent.id)
                # inherit organization from branch's parent if available
                if parent.parent and parent.parent.type == UniversalRegistration.TYPE_ORGANIZATION:
                    validated_data.setdefault("organization_id", parent.parent.id)
            elif parent.type == UniversalRegistration.TYPE_AGENT:
                # agent parent may have branch and org
                validated_data.setdefault("branch_id", parent.branch_id)
                validated_data.setdefault("organization_id", parent.organization_id)

        # default status
        validated_data.setdefault("status", UniversalRegistration.STATUS_ACTIVE)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # When parent changes, ensure inheritance updates
        parent = validated_data.get("parent")
        if parent:
            if parent.type == UniversalRegistration.TYPE_ORGANIZATION:
                validated_data.setdefault("organization_id", parent.id)
            elif parent.type == UniversalRegistration.TYPE_BRANCH:
                validated_data.setdefault("branch_id", parent.id)
                if parent.parent and parent.parent.type == UniversalRegistration.TYPE_ORGANIZATION:
                    validated_data.setdefault("organization_id", parent.parent.id)

        return super().update(instance, validated_data)


# Serializer for RegistrationRule
from .models import RegistrationRule

class RegistrationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRule
        fields = '__all__'
