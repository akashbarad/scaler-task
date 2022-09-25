import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import *
from .serializers import interviewSerializer, participantSerializer

## Participants API
## Get Participant /participant/get/
@api_view(['GET'])
def getParticipants(request):
    participants = Participant.objects.all()
    participants_serialized = []
    for participant in participants:
        participants_serialized.append(participantSerializer(participant))
    return JsonResponse({'data': participants_serialized})
## Add Participant /participant/add/
@api_view(['POST'])
def addParticipants(request):
    name = request.data.get('name')
    mail = request.data.get('mail')

    if name and mail:
        participant, created = Participant.objects.get_or_create(name=name, mail=mail)
        print(participant)
        return JsonResponse({'data': participantSerializer(participant), created: created})
    else:
        return JsonResponse({'error': 'Please provide name and participants'})

## Interviews API
## Search Interviews /interview/search/ 
@api_view(['POST'])
def search(request):
    search_term = request.data.get('searched')
    final_interviews_list = []
    if search_term:
        interviews = Interview.objects.filter(name__contains=search_term)

        for interview in interviews:
            final_interviews_list.append(interviewSerializer(interview))

    return JsonResponse({'data': final_interviews_list, 'keyword': search_term})
## Get Interviews /interview/get/ 
@api_view(['GET'])
def getInterviews(request):
    interviews = Interview.objects.all()
    final_result = []
    for interview in interviews:
        final_result.append(interviewSerializer(interview))
    return JsonResponse({'data': final_result})
## Add Interviews /interview/add/ 
@api_view(['POST'])
def addInterviews(request):
    name = request.data.get('name')
    participant_ids = request.data.get('participant_ids')
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')

    if name and participant_ids:
        interview = Interview.objects.create(name=name)
        for participant_id in participant_ids:
            participant = Participant.objects.get(id=participant_id)
            interview.participants.add(participant)
        interview.start_time = start_time
        interview.end_time = end_time
        interview.save()
        return JsonResponse({'data': interviewSerializer(interview)})
    else:
        return JsonResponse({'error': 'Please provide name and participants'})
## Edit Interviews /interview/edit/ 
@api_view(['POST'])
def editInterviews(request, id):
    interview = Interview.objects.get(id=id)
    name = request.data.get('name')
    participant_ids = request.data.get('participant_ids')
    
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')
    format = "%Y-%m-%d %H:%M:%S"
    start_object = datetime.datetime.strptime(start_time, format)
    end_object = datetime.datetime.strptime(end_time, format)

    if name and participant_ids and type(participant_ids) == list and len(participant_ids) >= 2 and start_time <= end_time:
        interview.name = name
        interview.start_time = start_object
        interview.end_time = end_object
        interview.participants.clear()
        for participant_id in participant_ids:
            participant = Participant.objects.filter(id=participant_id).first()
            interviews = Interview.objects.filter(participants__name=participant_id)
            for participant_interview in interviews:
                if not (participant_interview.start_time >= end_time or participant_interview.end_time <= start_time):
                    return JsonResponse({'error': 'Participant is busy at this time'})

            if participant:
                interview.participants.add(participant)
        
        interview.save()
        return JsonResponse({'data': interviewSerializer(interview)})
    else:
        return JsonResponse({'error': 'Please provide name and participants'})