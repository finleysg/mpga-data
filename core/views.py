from datetime import timedelta

import djoser.views
from djoser import utils
from djoser.conf import settings

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from mpga.settings import to_bool, is_development
from .models import SeasonSettings
from .serializers import SettingsSerializer


is_localhost = to_bool(is_development)

@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class SettingsViewSet(viewsets.ModelViewSet):
    queryset = SeasonSettings.objects.all()
    serializer_class = SettingsSerializer


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")


class TokenCreateView(djoser.views.TokenCreateView):
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token

        response = Response()
        data = token_serializer_class(token).data

        response.set_cookie(
            key = "mpga_access_token",
            path = "/",
            value = data["auth_token"],
            max_age = timedelta(days=180),
            secure = not is_localhost,
            httponly = True,
            samesite = "Lax",
            domain = "data.mpga.net" if not is_localhost else None,
        )

        response.data = "Welcome!"
        response.status_code = status.HTTP_200_OK
        return response


class TokenDestroyView(djoser.views.TokenDestroyView):
    """Use this endpoint to logout user (remove user authentication token)."""

    permission_classes = settings.PERMISSIONS.token_destroy

    def post(self, request):
        response = Response()
        response.delete_cookie(
            key = "mpga_access_token",
            path = "/",
            samesite = "Lax",
            domain = "data.mpga.net" if not is_localhost else None,
        )
        response.status_code = status.HTTP_204_NO_CONTENT
        utils.logout_user(request)
        return response
