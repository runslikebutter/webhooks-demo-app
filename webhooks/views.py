from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyfcm import FCMNotification


fcm_token = None
apns_token = None
voip_token = None

class WebhookHandlerView(APIView):

    def post(self, request):
        global fcm_token
        global voip_token
        global apns_token
        if fcm_token:
            push_service = FCMNotification(api_key="<api-key>")
            registration_id = fcm_token
            message_title = "Test title"
            message_body = "Test body"
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return Response(status=status.HTTP_200_OK)


class RegisterDeviceView(APIView):

    def post(self, request):
        global fcm_token
        global voip_token
        global apns_token
        # {
        #     "device": "android",
        #     "type": "voip",
        #     "token": "1234"
        # }
        if request.data["device"] == "android":
            fcm_token = request.data.get("token", "")
        if request.data["device"] == "ios":
            if request.data["type"] == "voip":
                voip_token = request.data.get("token", "")
            else:
                apns_token = request.data.get("token", "")
            fcm_token = request.data.get("token", "")
        return Response(status=status.HTTP_200_OK)
