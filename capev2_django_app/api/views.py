# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

# Global variables for URL and token
API_URL = 'http://172.174.239.25:8000/apiv2/'
TOKEN = 'd629af8a5ea6f92294d887019e7fccca554bb109'

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

        # Authentication headers
        headers = {'Authorization': f'Token {TOKEN}'}

        # Prepare file payload
        multipart_file = {"file": ("temp_file_name", file)}

        # Send POST request to the third-party API
        try:
            response = requests.post(API_URL + 'tasks/create/file/', files=multipart_file, data=task_data, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                # Extract task_id from the response JSON
                task_id = response.json()
                return Response({'task_id': task_id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to create task'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskCreateUrlView(APIView):
    def post(self, request):
        # Required parameter: URL
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Optional parameters
        data = {
            'package': request.data.get('package', 'default'),
            'timeout': request.data.get('timeout'),
            'priority': request.data.get('priority'),
            'options': request.data.get('options'),
            'machine': request.data.get('machine'),
            'platform': request.data.get('platform'),
            'tags': request.data.get('tags'),
            'custom': request.data.get('custom'),
            'memory': request.data.get('memory'),
            'enforce_timeout': request.data.get('enforce_timeout'),
            'clock': request.data.get('clock')
        }

        # Authentication headers
        headers = {'Authorization': f'Token {TOKEN}'}

        # Send POST request to the third-party API
        try:
            response = requests.post(API_URL + 'tasks/create/url/', data={'url': url, **data}, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                # Extract task_id from the response JSON
                task_id = response.json()
                return Response({'task_id': task_id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to create task'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskListView(APIView):
    def get(self, request, limit=None, offset=None):
        # Parameters
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        # Authentication headers
        headers = {'Authorization': f'Token {TOKEN}'}

        # Send GET request to the third-party API
        try:
            response = requests.get(API_URL + 'tasks/list/', params=params, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                # Extract tasks from the response JSON
                tasks = response.json()
                return Response({'tasks': tasks}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to retrieve tasks'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskView(APIView):
    def get(self, request, id):
        # Authentication headers
        headers = {'Authorization': f'Token {TOKEN}'}

        # Send GET request to the third-party API
        try:
            response = requests.get(API_URL + f'tasks/view/{id}/', headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                # Extract task details from the response JSON
                task_details = response.json()
                return Response({'task_details': task_details}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to retrieve task details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDeleteView(APIView):
    def get(self, request, id):
        # Authentication headers
        headers = {'Authorization': f'Token {TOKEN}'}

        # Send DELETE request to the third-party API
        try:
            response = requests.get(API_URL + f'tasks/delete/{id}/', headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check if response is successful
            if response.status_code == 200:
                task_details = response.json()
                return Response({'message': task_details}, status=status.HTTP_200_OK)
            elif response.status_code == 404:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unable to delete the task'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
