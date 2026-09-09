from rest_framework import serializers
from .models import User
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,min_length=8)
 class Meta: model=User; fields=('id','username','email','phone','password','first_name','last_name')
 def create(self,v): p=v.pop('password'); return User.objects.create_user(password=p,**v)
class UserSerializer(serializers.ModelSerializer):
 class Meta: model=User; fields=('id','username','email','phone','first_name','last_name','role')
class FirebaseAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(
        required=True
    )


class FirebaseAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    device_token = serializers.CharField(required=False, allow_blank=True, allow_null=True)    
class CompleteRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]

        extra_kwargs = {
            "first_name": {
                "required": True,
                "allow_blank": False,
            },
            "last_name": {
                "required": True,
                "allow_blank": False,
            },
            "email": {
                "required": True,
                "allow_blank": False,
            },
            "phone": {
                "required": False,
                "allow_blank": True,
            },
        }

    def validate_email(self, value):
        value = value.strip().lower()

        # Don't allow another user to use this email
        queryset = User.objects.filter(
            email__iexact=value
        ).exclude(
            id=self.instance.id
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def validate_first_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "First name is required."
            )

        return value

    def validate_last_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Last name is required."
            )

        return value    