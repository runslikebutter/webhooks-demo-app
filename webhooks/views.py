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
        print(request.data)
        guid = request.data.get("guid", None)
        if guid is None:
            call = request.data.get("call", None)
            guid = call.get("guid", None)
        token = request.GET.get('token')
        # type values: voip/apns/fcm
        type = request.GET.get('type')
        print("token - ", token)
        print("type - ", type)
        print("guid - ", guid)
        if type == "fcm":
            try:
                push_service = FCMNotification(api_key=os.getenv('FCM_KEY'))
                result = push_service.notify_single_device(registration_id=token, data_message={"guid": guid})
                print(result)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

        if type == "voip":
            try:
                guid = request.data["guid"]
                payload = Payload(badge=1, custom={"guid": guid})
                client = APNsClient(os.getenv('APPLE_VOIP_CERT_PATH'), use_sandbox=bool(os.getenv('APPLE_SANDBOX')), use_alternative_port=False)
                client.send_notification(token, payload, topic="com.butterflymx.butterflymx.voip")
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

        return Response(status=status.HTTP_200_OK)

