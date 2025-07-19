# admin_login/serializers.py
from rest_framework import serializers
from .models import AdminAccount

class AdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccount
        fields = ['account_id', 'email', 'name', 'img_path', 'permission']
        read_only_fields = ['account_id']