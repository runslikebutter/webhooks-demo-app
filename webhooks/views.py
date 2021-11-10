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
        push_type = "call"
        call_status = "initializing"
        if guid is None:
            push_type = "status"
            call = request.data.get("call", None)
            call_status = request.data.get("status", None)
            guid = call.get("guid", None)
        token = request.GET.get('token')
        # type values: voip/apns/fcm
        type = request.GET.get('type')
        print("token - ", token)
        print("type - ", type)
        print("guid - ", guid)
        print("call_status - ", call_status)
        if type == "fcm":
            try:
                push_service = FCMNotification(api_key=os.getenv('FCM_KEY'))
                if push_type == "call":
                    result = push_service.notify_single_device(registration_id=token,
                                                               data_message={"guid": guid, "call_status": call_status})
                else:
                    result = push_service.notify_single_device(registration_id=token,
                                                               data_message={"guid": guid, "call_status": call_status})
                print(result)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

        if type == "voip":
            try:
                payload = Payload(badge=1, custom={"guid": guid})
                client = APNsClient(os.getenv('APPLE_VOIP_CERT_PATH'), use_sandbox=bool(os.getenv('APPLE_SANDBOX')), use_alternative_port=False)
                client.send_notification(token, payload)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())

        if type == "apns":
            try:
                payload = Payload(badge=1, alert="New call", custom={"guid": guid})
                client = APNsClient(os.getenv('APPLE_APNS_CERT_PATH'), use_sandbox=bool(os.getenv('APPLE_SANDBOX')), use_alternative_port=False)
                client.send_notification(token, payload)
            except Exception as ex:
                print("Exception - ", traceback.format_exc())


        return Response(status=status.HTTP_200_OK)

