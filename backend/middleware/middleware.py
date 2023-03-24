from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.contrib.auth.models import User

import jwt
import environ

# Load environment variables
env = environ.Env()
environ.Env.read_env()


class JWTTokenDecodeMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # User methods don't require bearer token auth, so leave them alone for now.
        if request.path_info.startswith('/user'):
            return

        authorization_header = request.headers.get('Authorization')
        if authorization_header is not None:
            try:
                bearer_token = jwt.decode(
                    authorization_header,
                    env('JWT_SECRET'),
                    env('JWT_ALGORITHM')
                )

                user_id = bearer_token['user_id']

                user = User.objects.get(pk=user_id)

                if user is not None:
                    # Set the user on the request object
                    request.user = user

                    return
                else:
                    return JsonResponse(
                        {
                            'message': 'Error authenticating user',
                        },
                        status=403
                    )

            except jwt.exceptions.DecodeError:
                return JsonResponse(
                    {
                        'message': 'Error decoding auth token',
                    },
                    status=403,
                )
        else:
            return JsonResponse(
                {
                    'message': 'No bearer token found in request. User not authorized.'
                },
                status=403,
            )
