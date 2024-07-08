from rest_framework import generics, status, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .utils import fetch_location
from .serializers import ChangePasswordSerializer
from django.contrib import messages


User = get_user_model()

class UserDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
        print("User authenticated:", self.request.user.is_authenticated)
        print("User:", self.request.user)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, 'Профиль успешно обновлен.')
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, 'Профиль успешно обновлен.')
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        messages.success(request, 'Профиль успешно удален.')
        return Response(status=204)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Неправильный пароль."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Пароль успешно обновлен.',
            }
            messages.success(request, 'Пароль успешно обновлен.')
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def location_view(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        ip_address = body.get('ip', '127.0.0.1')
        location_data = fetch_location(ip_address)
        return JsonResponse(location_data)
    else:
        ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
        location_data = fetch_location(ip_address)
        return JsonResponse(location_data)

