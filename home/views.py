from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64
import cv2
import numpy as np
from incrementalexplainer import increx, yolo, d_rise
import uuid
from collections import defaultdict
import os

class VideoProcessor:
    def __init__(self):
        self.is_frame_processed = False
        self.model = yolo.Yolo()
        num_mutants = int(os.getenv('NUM_MUTANTS')) if os.getenv('NUM_MUTANTS') else 400
        num_divisions = int(os.getenv('SALIENCY_MAP_DIVISIONS')) if os.getenv('SALIENCY_MAP_DIVISIONS') else 100
        self.explainer = d_rise.DRise(self.model, num_mutants=num_mutants)
        self.incRex = increx.IncRex(self.model, self.explainer, saliency_map_divisions=num_divisions)

    def process_frame(self, frame):
        nparr = np.frombuffer(base64.b64decode(frame.split(',')[1]), np.uint8)
        if nparr.size == 0:
            raise ValueError('Empty frame data')
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, img_result = self.incRex.explain_frame(frame)
        img_result = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
        _, jpeg = cv2.imencode('.jpg', img_result)
        return jpeg.tobytes()


class SessionTracker:
    
    sessions = defaultdict(VideoProcessor)
    
    @staticmethod
    def create_session(processor):
        session_id = str(uuid.uuid4())
        SessionTracker.sessions[session_id] = processor
        return session_id
    
    @staticmethod
    def get_processor(session_id):
        return SessionTracker.sessions.get(session_id)
    
@csrf_exempt
def init_processor(request):
    if request.method == 'POST':
        request.session['video_processor'] = SessionTracker.create_session(VideoProcessor())
        return JsonResponse({'status': 'initialized'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        frame_data = json.loads(request.body)['frame']
        
        video_processor = SessionTracker.get_processor(request.session.get('video_processor'))
        if not video_processor:
            return JsonResponse({'error': 'Processor not initialized'}, status=400)
        
        processed_frame = video_processor.process_frame(frame_data)
        response_data = {'processed_frame': base64.b64encode(processed_frame).decode('utf-8')}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def video_stream(request):
    return render(request, 'home.html')