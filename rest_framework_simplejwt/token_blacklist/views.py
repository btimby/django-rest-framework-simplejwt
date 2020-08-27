from ..serializers import TokenVerifySerializer
from ..tokens import RefreshToken
from ..exceptions import InvalidToken, TokenError

from rest_framework.response import Response
from rest_framework import generics, status


class BlacklistTokenSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = RefreshToken(attrs['token'])
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


token_blacklist = BlacklistTokenView.as_view()