import datetime

import jwt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt  # na to bgalw meta
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from app.models import users, logging
from app.serializers import UserSerializer


@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        log = logging()
        username = request.data['username']
        password = request.data['password']

        log.user = username
        if users.objects.filter(username=username).exists():
            user = users.objects.get(username=username)
            hashed_password = user.password
            if check_password(password, hashed_password):
                try:
                    last_id = logging.objects.latest('id')
                    last_user = logging.objects.get(id=last_id.id)
                    if username == last_user.user:
                        if last_user.result == 'success':
                            log.attempt_count = 1
                        else:
                            log.attempt_count = last_user.attempt_count + 1
                    else:
                        log.attempt_count = 1
                    log.result = 'success'
                    log.timestamp = datetime.datetime.now()
                except ObjectDoesNotExist:
                    log.result = 'success'
                    log.timestamp = datetime.datetime.now()
                    log.attempt_count = 1
                log.save()

                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                    'iat': datetime.datetime.utcnow()
                }

                jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')

                template = loader.get_template('template.html')

                response = Response()
                response.data = {
                    'jwt': jwt_token
                }
                response.set_cookie(key='jwt', value=jwt_token)
                response.accepted_renderer = TemplateHTMLRenderer()
                response.template_name = 'template.html'
                return response
            else:
                try:
                    last_id = logging.objects.latest('id')
                    last_user = logging.objects.get(id=last_id.id)
                    if username == last_user.user:
                        if last_user.result == 'success':
                            log.attempt_count = 1
                        else:
                            if last_user.attempt_count < 3:
                                log.attempt_count = last_user.attempt_count + 1
                            else:
                                # sunthiki gia lock. to minima na einai se alert
                                show_error_message(request, 'Your account has been locked!')
                    else:
                        log.attempt_count = 1
                    log.result = 'failed'
                    log.timestamp = datetime.datetime.now()
                except ObjectDoesNotExist:
                    log.result = 'failed'
                    log.timestamp = datetime.datetime.now()
                    log.attempt_count = 1
                log.save()
                show_error_message(request, 'Invalid Credentials. Please try again.')
        else:
            log.timestamp = datetime.datetime.now()
            log.attempt_count = 1
            log.result = 'failed'
            log.save()
            show_error_message(request, 'Invalid Credentials. Please try again.')
    return render(request, 'index.html')


def show_error_message(request, message):
    messages.success(request, message)
    return redirect('index')


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms={'HS256'})
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        id = payload['id']  # efoson exw 2 xristes paratirisa oti to id 19 einai gia 3180207 kai to 20 gia admin
        if id == 19:
            user = users.objects.get(username='3180207')
        elif id == 20:
            user = users.objects.get(username='admin')
        serializer = UserSerializer(user)
        return Response(serializer.data)
