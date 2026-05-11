from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Follow
from .serializers import UserSerializer, ProfileSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = UserSerializer(
            data=request.data,
            context={'request': request}
        )
        if ser.is_valid():
            user = ser.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(
                    user, context={'request': request}
                ).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=201)
        return Response(ser.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if not user:
            return Response(
                {'error': 'Wrong username or password'}, status=400
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(
                user, context={'request': request}
            ).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser = UserSerializer(request.user, context={'request': request})
        return Response(ser.data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        ser = ProfileSerializer(
            profile, data=request.data,
            partial=True, context={'request': request}
        )
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=400)


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if target == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=400)
        Follow.objects.get_or_create(follower=request.user, following=target)
        return Response({'status': 'followed'})

    def delete(self, request, user_id):
        Follow.objects.filter(
            follower=request.user, following_id=user_id
        ).delete()
        return Response({'status': 'unfollowed'})


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        ser = UserSerializer(user, context={'request': request})
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()
        data = ser.data
        data['is_following'] = is_following
        return Response(data)


class SuggestUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Users the current user is NOT following
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
        users = User.objects.exclude(
            id__in=list(following_ids) + [request.user.id]
        )[:10]
        ser = UserSerializer(users, many=True, context={'request': request})
        return Response(ser.data)


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response([])
        users = User.objects.filter(username__icontains=q)[:10]
        data = []
        for u in users:
            d = UserSerializer(u, context={'request': request}).data
            d['is_following'] = Follow.objects.filter(
                follower=request.user, following=u
            ).exists()
            data.append(d)
        return Response(data)