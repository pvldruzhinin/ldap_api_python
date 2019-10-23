import json

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api_service.utils import get_user_pnac_groups, get_group_users


class PnacGroups(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        incoming_data = request.body
        if incoming_data:
            data = json.loads(incoming_data)
            account_name = data.get('account_name')
            if account_name:
                groups_list = get_user_pnac_groups(account_name)
                return JsonResponse({'groups': groups_list})

            return JsonResponse(
                status=400,
                data={'message': 'Only {"account_name": account_name} in request body is allowed'}
            )
        return JsonResponse(
            status=400,
            data={'message': 'Empty body. Only {"account_name": account_name} in request body is allowed'}
        )


class GroupUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        incoming_data = request.body
        if incoming_data:
            data = json.loads(incoming_data)
            group_name = data.get('group_name')
            if group_name:
                users_list = get_group_users(group_name)
                return JsonResponse({'users': users_list})

            return JsonResponse(
                status=400,
                data={'message': 'Only {"group_name": group_name} in request body is allowed'}
            )
        return JsonResponse(
            status=400,
            data={'message': 'Empty body. Only {"group_name": group_name} in request body is allowed'}
        )
