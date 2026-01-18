from django.shortcuts import render, redirect
from pathlib import Path
from .service import CodeService

BASE_DIR = Path(__file__).resolve().parent


def editor(request):
    if request.method == "POST":
        code = request.POST.get("code", "")

        service = CodeService(BASE_DIR)
        # service.save_code("saved_code.py", code)
        print(code)

        return redirect("/code/editor")

    return render(request, "editor.html")
