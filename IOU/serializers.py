from rest_framework import serializers
from .models import User, IOU

class IOUSerializer(serializers.ModelSerializer):
	class Meta:
		model = IOU
		fields = ("__all__")


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("__all__")


