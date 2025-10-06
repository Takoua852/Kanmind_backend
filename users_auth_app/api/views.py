
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import AllowAny

class RegistrationView(APIView):

    """
    User Registration Endpoint.

    POST /registration/
    - Registers a new user
    - Returns auth token, user ID, fullname, and email on success
    - Returns validation errors on failure
    """
    permission_classes = [AllowAny]
    def post(self, request):
     
        serializer = RegistrationSerializer(data=request.data)
       
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.fullname,
                "email": user.email,
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):

    """
    User Login Endpoint.

    POST /login/
    - Authenticates user with email and password
    - Returns auth token, user ID, fullname, and email on success
    - Returns validation errors on failure

    Permissions:
    - Allow any user (authenticated or not)
    """
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        data   = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': user.fullname
            }
        else:
            data = serializer.errors
        return Response(data)

