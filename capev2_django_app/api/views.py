from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.http import JsonResponse

class TaskCreateFileView(APIView):
    def post(self, request):
        # Required parameter: file
        file = request.FILES.get('file')
        if file is None:
            return Response({'error': 'File parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Optional parameters
        package = request.data.get('package', 'default')
        timeout = request.data.get('timeout')
        priority = request.data.get('priority')
        options = request.data.get('options')
        machine = request.data.get('machine')
        platform = request.data.get('platform')
        tags = request.data.get('tags')
        custom = request.data.get('custom')
        memory = request.data.get('memory')
        enforce_timeout = request.data.get('enforce_timeout')
        clock = request.data.get('clock')

        # Prepare task data payload
        task_data = {
            'package': package,
            'timeout': timeout,
            'priority': priority,
            'options': options,
            'machine': machine,
            'platform': platform,
            'tags': tags,
            'custom': custom,
            'memory': memory,
            'enforce_timeout': enforce_timeout,
            'clock': clock
        }

        # Authentication token
        token = 'd629af8a5ea6f92294d887019e7fccca554bb109'  # Replace with your actual token
        headers = {'Authorization': f'Token {token}'}

        # Open the file in binary mode
    # Prepare file payload
        multipart_file = {"file": ("temp_file_name", file)}

        # Send POST request to the third-party API
        api_url = 'http://172.174.239.25:8000/apiv2/tasks/create/file/'
        try:
            response = requests.post(api_url, files=multipart_file,data=task_data, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                # Extract task_id from the response JSON
                task_id = response.json().get('task_id')
                return JsonResponse({'task_id': task_id}, status=201)
            else:
                return JsonResponse({'error': 'Failed to create task'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
