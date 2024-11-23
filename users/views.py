from dj_rest_auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .models import CustomUser  # Importă modelul tău de utilizator personalizat
from .serializers import GoogleAuthSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token  # Importă modelul Token pentru autentificare
from allauth.account.models import EmailAddress

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID


class GoogleLoginView(APIView):
    """
    View pentru autentificarea utilizatorului cu token-ul Google.
    """

    def post(self, request):
        # Validăm token-ul folosind serializer-ul
        serializer = GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Preluăm token-ul validat
        token = serializer.validated_data['token']

        try:
            # Verificăm și decodificăm token-ul
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            # Extragem informațiile despre utilizator
            email = idinfo.get('email')
            name = idinfo.get('name')

            # Căutăm utilizatorul după `email` în loc de `username`
            user, created = CustomUser.objects.get_or_create(email=email, defaults={
                'first_name': name.split()[0],
                'last_name': " ".join(name.split()[1:]) if len(name.split()) > 1 else "",
            })

            # Dacă utilizatorul este creat nou, setăm parola și creăm o înregistrare de e-mail verificată
            if created:
                user.set_password(settings.SECRET_KEY)
                user.save()

                # Adăugăm adresa de e-mail ca verificată
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    verified=True,
                    primary=True
                )

            # Generăm token-ul de autentificare
            auth_token, _ = Token.objects.get_or_create(user=user)

            # Returnăm token-ul de autentificare către frontend
            return Response({"key": auth_token.key}, status=status.HTTP_200_OK)

        except ValueError:
            raise AuthenticationFailed("Token-ul Google este invalid.")


User = get_user_model()


class CustomLoginView(LoginView):
    """
    View pentru autentificare care verifică dacă emailul există deja în baza de date.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        # Căutăm utilizatorul după email
        if email:
            try:
                user = User.objects.get(email=email)
                # Dacă utilizatorul există, returnăm un mesaj de eroare
                if user:
                    return Response(
                        {"detail": "Adresa de email există deja în baza de date. Poți încerca opțiunea de resetare a parolei."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                # Dacă utilizatorul nu există, continuăm cu autentificarea normală
                pass

        # Continuăm cu autentificarea normală dacă emailul nu este găsit
        return super().post(request, *args, **kwargs)



