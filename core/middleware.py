def auth_token(get_response):
    def middleware(request):
        token = request.COOKIES.get('mpga_access_token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'

        return get_response(request)

    return middleware