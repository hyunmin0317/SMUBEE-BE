from rest_framework import permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from ecampus import login
from .models import Profile
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer


# 회원가입
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        id, password = request.data["username"], request.data["password"]
        if login(id, password) == -1:
            body = {"message": "ecampus login error"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profile(user=user, password=password)
        profile.save()
        _, token = AuthToken.objects.create(user)
        return Response(
            {
                "username": user.username,
                "token": token
            }
        )


# 로그인
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "token": AuthToken.objects.create(user)[1],
            }
        )


# 접속 유지중인지 확인
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user