from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Projeto Senac</h1><p>Servidor Django em execução.</p>"
    )
