from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class WebhookHandlerView(APIView):

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class RegisterDeviceView(APIView):

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
