from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

import requests

from core.settings import KHALTI_SECRET_KEY, KHALTI_VERIFY_URL


class KhaltiPaymentVerificationView(APIView):
    """API View For Verifying Payment Made By User"""
    
    def post(self, request, format=None):
        # getting token and amount from request body
        token = request.data.get("token", None)
        amount = request.data.get("amount", None)
        payload = {
            "token": token,
            "amount": amount
        }
        
        # checking both token and amount are present in the body
        if not token or not amount:
            return Response("Please Provide Both Token and Amount", status.HTTP_400_BAD_REQUEST)
        
        # sending request to khalti server for verification
        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}"
        }
        response = requests.post(KHALTI_VERIFY_URL, payload, headers = headers)
        if response.status_code == 200:
            # returning success response to user
            return Response(data={"message":"Payment Successfull","messageType":"success"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Something Went Wrong","messageType":"error"}, status=status.HTTP_400_BAD_REQUEST)