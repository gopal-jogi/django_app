from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from magika import Magika
from django.core.files.uploadedfile import UploadedFile
from pathlib import Path
import tempfile
import os

m = Magika()

@csrf_exempt
def MagikaApi(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'error': 'No files uploaded'}, status=400)
        
        try:
            results = []
            for file in files:
                if not isinstance(file, UploadedFile):
                    return JsonResponse({'error': 'Invalid file uploaded'}, status=400)
                
                # Create a temporary file to write the uploaded file's contents into
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    
                    # Close the temporary file and get its path
                    temp_file_path = Path(temp_file.name)
                
                # Identify content type using Magika
                res = m.identify_path(temp_file_path)
                
                # Clean up the temporary file
                os.unlink(temp_file_path)
                
                results.append({'filename': file.name, 'content_type': res.output.ct_label})
            
            return JsonResponse({'results': results}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
