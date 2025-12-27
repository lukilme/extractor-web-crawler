from django.shortcuts import render
from task import sum_via_nlp
from celery.result import AsyncResult
from django.http import JsonResponse, StreamingHttpResponse
import requests

def task_status(request):
    task_id = request.GET.get("task_id")
    if not task_id:
        return JsonResponse({"error": "task_id is required"}, status=400)

    result = AsyncResult(task_id)
    return JsonResponse({
        "state": result.state,
        "result": result.result if result.ready() else None
    })
def index(request):
    context = {}

    if request.method == "POST":
        value = int(request.POST["value"])
        task = sum_via_nlp.delay(value)
        context["task_id"] = task.id
        print(task)
    task_id = request.GET.get("task_id")
    if task_id:
        result = AsyncResult(task_id)
        if result.ready():
            context["result"] = result.result

    return render(request, "default/index.html", context)


def chat_view(request):
    return render(request, "default/chat.html")


def chat_stream(request):
    question = request.GET.get("q", "").strip()

    if not question:
        return StreamingHttpResponse("Pergunta vazia", content_type="text/plain")

    def stream():
        with requests.post(
            "http://nlp-gateway:8100/summarize",
            json={"text": question},
            stream=True,
            timeout=None,
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode("utf-8")

    return StreamingHttpResponse(stream(), content_type="text/plain")