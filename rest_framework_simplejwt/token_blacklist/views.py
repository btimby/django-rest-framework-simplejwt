from ..serializers import TokenVerifySerializer
from ..tokens import AccessToken, BlacklistMixin


class BlacklistToken(AccessToken, BlacklistMixin):
    pass


class TokenBlacklistSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = BlacklistToken(attrs['token'])
        token.blacklist()
        return token


class BlacklistTokenView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = BlacklistTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response('', status=status.HTTP_204_NO_CONTENT)
