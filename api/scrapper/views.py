from django.shortcuts import render


from django.http import JsonResponse
from task import say_hello

def hello_task(request):
    task = say_hello.delay()
    return JsonResponse({
        "task_id": task.id,
        "status": "queued"
    })
