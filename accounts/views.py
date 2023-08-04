from rest_framework.viewsets import ModelViewSet
from .models import User, Incident
from .serializers import UserSerializer, IncidentSerializer
from rest_framework.filters import SearchFilter
from permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class SignupAPIView(APIView):
    def post(self, request, format=None):
        name = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not (name and password and email):
            return Response({'error': 'Please provide username, password, and email.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(name=name, password=password, email=email)
        user.is_active = True
        user.save()

        return Response({'success': 'Account created successfully.'},
                        status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        if not (email and password):
            return Response({'error': 'Please provide username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'message': 'Login Successfully',
                             'access_token': access_token},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permissions = {'default': [IsAuthenticated, IsOwner],
                   'list': [IsAuthenticated],
                   'create': [IsAuthenticated]}

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super(UserViewSet, self).get_permissions()


class IncidentViewSet(ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['id']
    authentication_classes = [JWTAuthentication]
    permissions = {'default': [IsAuthenticated, IsOwner],
                   'list': [IsAuthenticated],
                   'create': [IsAuthenticated]}

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super(IncidentViewSet, self).get_permissions()


