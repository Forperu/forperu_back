from io import BytesIO
from datetime import timedelta

from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.timezone import now
# import pyotp
# import qrcode

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


# from core.permissions import HasValidAPIKey
# from utils.ip_utils import get_client_ip

User = get_user_model()

class OTPLoginView(StandardAPIView):
    # permission_classes = [HasValidAPIKey]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return self.error("Both email and OTP code are required.")
        
        try:
            user = User.objects.get(email=email)
            
            # Verificar que el OTP es válido
            # totp = pyotp.TOTP(user.otp_base32)
            # if not totp.verify(otp_code):
            #     return self.error("Invalid OTP code.")
            
            # Actualizar el estado del OTP
            user.login_otp_used = True
            user.save()

            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            return self.response({
                "access": str(refresh.access_token), 
                "refresh": str(refresh)
            })

        except User.DoesNotExist:
            return self.response("User does not exist.", status=status.HTTP_404_NOT_FOUND)