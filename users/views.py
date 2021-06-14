from admin.pagination import CustomPagination
from rest_framework.views import APIView
from users.serializers import PermissionSerializer, RoleSerializer, UserSerializer
from rest_framework import exceptions, viewsets, status, generics, mixins
# , authentication_classes, permission_classes
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Permission, Role, User
from .authentication import JWTAuthentication, generate_access_token


@api_view(['POST'])
def register(request):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):  # decrypt and check password
        raise exceptions.AuthenticationFailed('Incorrect Password!')

    response = Response()

    token = generate_access_token(user)

    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        'jwt': token
    }

    return response


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'success'
    }

    return response


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({
            'data': serializer.data
        })


class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })


# as all-in-one crud operation class
class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, _):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, _, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)
        return Response({
            'data': serializer.data
        })

    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)

    def destroy(self, _, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGenericAPIView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()  # crud operations are handled by the GenericAPIView
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        # if you want to change pagination page:
        # /api/users?page=###
        return self.list(request)

    def post(self, request):
        # defaults:
        request.data.update({
            'password': 1234,
            'role': request.data['role_id']
        })

        return Response({
            'data': self.create(request).data
        })

    def put(self, request, pk=None):
        if request.data['role_id']:
            request.data.update({
                'role': request.data['role_id']
            })

        return Response({
            # partial_update = if value not set, then don't update it
            'data': self.partial_update(request, pk).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        # partial = only updating some fields, not all
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('passwords do not match')

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def users(_):
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response(serializer.data)
