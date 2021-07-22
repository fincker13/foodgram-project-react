from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import ChangePasswordSerializer, UserSerializers


class SignUpAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            'Пользователь успешно создан',
            status=status.HTTP_201_CREATED
        )


class UsersViewSet(ModelViewSet):
    """ViewSet для работы с ползователями"""
    serializer_class = UserSerializers
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=['get', 'post'],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(instance=request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SetPasswordViewSet(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        return Response('user:', request.user)
