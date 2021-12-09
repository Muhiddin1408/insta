from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.signals import user_logged_in
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer,
    CommentSerializer,
    ImageSerializer,
    UserUpdateSerializer,
    RegisterSerializer,
    LocationSerializer
)
from .models import Image, Comment
from account.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ImageViewSet(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CreateImageViewSet(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CreateCommentView(generics.CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserView(generics.ListAPIView):
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UpdateView(APIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    # a = SELECT * FROM User

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            try:
                poyload = jwt_payload_handler(user)
                token = jwt_encode_handler(poyload)
                user_detail = {}
                user_detail['status'] = 1
                user_detail['msg'] = 'User signin'
                user_detail['username'] = UserSerializer(user, many=False).data
                user_detail['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_detail, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please provide a login and a password'
        }
        return Response(res)


class ImageIdComment(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        image = self.request.GET.get('image_id')
        image = Image.objects.filter(id=image).first()
        return Comment.objects.filter(image=image)


class UserImageView(generics.ListAPIView):

    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        users = User.objects.filter(pk=user).first().followers.all()
        # print(Image.objects.filter(user_id__in=users), users)
        return Image.objects.filter(user__in=users)


class AddFollower(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self):
        user = User.objects.get(user_id=self.request.data.get('user_id'))
        follow = User.objects.get(user_id=self.request.data.get('follow'))
        user.following.add(follow)
        user.save()
        follow.followers.add(user)
        follow.save()
        print(str(user)+" "+str(follow))
        return Response({'status': status.HTTP_200_OK, 'data': '', 'massage': 'follow'+str(follow.username)})

#
class LocationView(generics.CreateAPIView):
    serializer_class = LocationSerializer
