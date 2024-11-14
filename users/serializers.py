from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from users.models import CustomUser


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if not value:
            raise serializers.ValidationError("Token-ul este necesar.")
        return value


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        # Verifică dacă email-ul există deja
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Această adresă de email este deja înregistrată. "
                "Dacă ai creat contul cu Google, te rugăm să te autentifici prin Google "
                "sau poți utiliza opțiunea de resetare a parolei."
            )
        return email
