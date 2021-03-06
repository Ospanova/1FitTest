from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from users.models import MainUser


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MainUser.objects.filter(is_deleted=0)

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
