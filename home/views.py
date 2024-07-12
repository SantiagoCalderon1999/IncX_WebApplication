from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64
import cv2
import numpy as np
from incrementalexplainer import increx, yolo, d_rise

class VideoProcessor:
    is_frame_processed = False
    model = yolo.Yolo()
    explainer = d_rise.DRise(model, num_mutants=500)
    incRex = increx.IncRex(model, explainer, saliency_map_divisions=100)

    @staticmethod
    def process_frame(frame):
        # Convert the frame to an OpenCV image
        nparr = np.frombuffer(base64.b64decode(frame.split(',')[1]), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, img_result = VideoProcessor.incRex.explain_frame(frame)
        img_result = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
        _, jpeg = cv2.imencode('.jpg', img_result)
        return jpeg.tobytes()

@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        frame_data = json.loads(request.body)['frame']
        processed_frame = VideoProcessor.process_frame(frame_data)
        response_data = {'processed_frame': base64.b64encode(processed_frame).decode('utf-8')}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def video_stream(request):
    return render(request, 'home.html')
