# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
from abstract.viewset import Teste
def feed(request):
    return render(request, "feed.html")

def feed_api(request):
    page_number = request.GET.get("page", 1)

    posts = Post.objects.all()
    paginator = Paginator(posts, 20)
    page_obj = paginator.get_page(page_number)
    data = [
        {
            "titulo": p.titulo,
            "conteudo": p.conteudo,
            "criado_em": p.criado_em.strftime("%d/%m/%Y %H:%M")
        }
        for p in page_obj
    ]

    return JsonResponse({
        "posts": data,
        "has_next": page_obj.has_next()
    })

def feed_active(request):
    return render(request, "feed_active.html")