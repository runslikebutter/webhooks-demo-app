from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyfcm import FCMNotification
from apns2.client import APNsClient
from apns2.payload import Payload
import os
import traceback

fcm_token = None
apns_token = None
voip_token = None

class WebhookHandlerView(APIView):

    def post(self, request):
        global fcm_token
        global voip_token
        global apns_token
        print("fcm_token - ", fcm_token)
        print("apns_token - ", apns_token)
        print("voip_token - ", voip_token)
        if fcm_token:
            try:
                guid = request.data["guid"]
                push_service = FCMNotification(api_key=os.getenv('FCM_KEY'))
                registration_id = fcm_token
                result = push_service.notify_single_device(registration_id=registration_id, data_message={"guid": guid})
                print(result)
                print("guid - ", guid)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

        if voip_token:
            try:
                guid = request.data["guid"]
                payload = Payload(badge=1, custom={"guid": guid})
                client = APNsClient(os.getenv('APPLE_VOIP_CERT_PATH'), use_sandbox=bool(os.getenv('APPLE_SANDBOX')), use_alternative_port=False)
                client.send_notification(voip_token, payload)
                print("guid - ", guid)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

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
        # {
        #     "device": "ios",
        #     "type": "voip",
        #     "token": "1234"
        # }
        if request.data["device"] == "android":
            fcm_token = request.data.get("token", "")
        if request.data["device"] == "ios":
            if request.data.get("type",'') == "voip":
                voip_token = request.data.get("token", "")
            else:
                apns_token = request.data.get("token", "")
        return Response(status=status.HTTP_200_OK)
