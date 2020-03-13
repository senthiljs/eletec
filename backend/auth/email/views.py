from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.conf import settings

from rest_framework.response import Response
from rest_framework import views, generics
from rest_framework import throttling
from rest_framework import status

from service.sms.message import SmsMessage

from .models import EmailToken
from .serializers import EmailTokenSerializer, EmailTokenValidateSerializer

from .utils import user_detail

class GenerateOTP(generics.CreateAPIView):
    
    queryset = EmailToken.objects.all()
    
    serializer_class = EmailTokenSerializer
    
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request, format=None):
        token = self.serializer_class(data=request.data, context={'request': request})
        
        if token.is_valid():
            otp = get_random_string(4, '0123456789')
            email = token.data.get('email')

            try: 
                email_token = EmailToken.objects.get(email=email)
                email_token.otp = otp
                email_token.save()
            except EmailToken.DoesNotExist:
                EmailToken.objects.create(email=email, otp=otp)

            from_phone = getattr(settings, 'SENDSMS_FROM_NUMBER')

            message = SmsMessage(
                body='[Eletec] Your verification code is %s' % otp,
                from_phone=from_phone,
                to=email
            ).send()
            
            if message.ok:
                return Response(token.data)
            else:
                return Response({'error': 'failed to send'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(token.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateOTP(generics.CreateAPIView):
    queryset = EmailToken.objects.all()
    serializer_class = PhoneTokenValidateSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request, format=None):
        token = self.serializer_class(data=request.data, context={'request': request})
        if token.is_valid():

            email = token.data.get("email")
            otp = token.data.get("otp")
            
            user = authenticate(request, email=email, otp=otp)

            if user:
                last_login = user.last_login
                login(request, user)
                response = user_detail(user, last_login)
                return Response(response, status=status.HTTP_200_OK)

        return Response(token.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Create your views here.
# send_mail('Subject here', 'Here is the message.', 'mobileapp@eletec.ae', ['mars.jinxing@gmail.com'], fail_silently=False)
# from django.core.mail import send_mail, BadHeaderError

