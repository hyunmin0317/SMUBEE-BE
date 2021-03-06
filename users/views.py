from django.contrib.auth.models import User
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from crawling import login, infomation
from .models import Profile
from .serializers import UserSerializer


# 이캠퍼스 로그인
class LoginAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        id, password = request.data["username"], request.data["password"]
        session = login(id, password)
        if session == -1:
            body = {"message": "ecampus login error"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        updated_rows = User.objects.filter(username=id)
        if not updated_rows:
            User.objects.create(username=id)
        user = User.objects.get(username=id)

        updated_rows = Profile.objects.filter(user=user).update(password=password)
        if not updated_rows:
            name, major = infomation(session)
            Profile.objects.create(user=user, password=password, name=name, major=major)
        profile = Profile.objects.get(user=user)

        _, token = AuthToken.objects.create(user)
        return Response(
            {
                "name": profile.name,
                "major": profile.major,
                "token": token
            }
        )

# 접속 유지중인지 확인
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user