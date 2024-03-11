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
                task_id = response.json()
                return JsonResponse({'task_id': task_id}, status=201)
            else:
                return JsonResponse({'error': 'Failed to create task'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# create a url view
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

        # Authentication token
        token = 'd629af8a5ea6f92294d887019e7fccca554bb109'  # Replace with your actual token
        headers = {'Authorization': f'Token {token}'}

        # Send POST request to the third-party API
        api_url = 'http://172.174.239.25:8000/apiv2/tasks/create/url/'
        try:
            response = requests.post(api_url, data={'url': url, **data}, headers=headers)
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

#Task list
class TaskListView(APIView):
    def get(self, request, limit=None, offset=None):
        # Parameters
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        # Authentication token
        token = 'd629af8a5ea6f92294d887019e7fccca554bb109'  # Replace with your actual token
        headers = {'Authorization': f'Token {token}'}

        # Send GET request to the third-party API
        api_url = 'http://172.174.239.25:8000/apiv2/tasks/list/'
        try:
            response = requests.get(api_url, params=params, headers=headers)
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
        

#Task view
class TaskView(APIView):
    def get(self,request,id):
        
        # Authentication token
        token = 'd629af8a5ea6f92294d887019e7fccca554bb109'  # Replace with your actual token
        headers = {'Authorization': f'Token {token}'}
        # Send GET request to the third-party API
        api_url = f'http://172.174.239.25:8000/apiv2/tasks/view/{id}/'
        try:
            response = requests.get(api_url, headers=headers)
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

#Task view
class TaskView(APIView):
    def get(self,request,id):
        
        # Authentication token
        token = 'd629af8a5ea6f92294d887019e7fccca554bb109'  # Replace with your actual token
        headers = {'Authorization': f'Token {token}'}
        # Send GET request to the third-party API
        api_url = f'http://172.174.239.25:8000/apiv2/tasks/view/{id}/'
        try:
            response = requests.get(api_url, headers=headers)
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


            