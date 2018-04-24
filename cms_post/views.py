# Cristina del Río
from django.shortcuts import render
from cms_post.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

FORMULARIO = """
<form action="" method="POST">
    <u>Contenido:</u><br>
    <input type="text" name="page"/>
    <input type="submit" value="Enviar"/>
</form>"""


def inicio_pag(request):
    if request.user.is_authenticated():
        resp = "-Logged in as: <b>" + request.user.username
        resp += "</b> ==> <a href='/logout'>Logout</a><br>"
    else:
        resp = "Not logged in: <a href='/login'>Login</a><br>"
    resp += "<u><h4>La lista de las paginas es:</h4></u>"
    list_pags = Pages.objects.all()
    for pag in list_pags:
        resp += "<ul><li>" + pag.name + " ==> " + pag.page + "</ul></li>"
    return HttpResponse(resp)


@csrf_exempt
def edit_pag(request, name):
    if request.method == "GET":
        try:
            # Cuando existe
            page = Pages.objects.get(name=name)
            resp = "La página que has pedido es: " + page.name
            resp += " ==> " + page.page + "<br>"
            if request.user.is_authenticated():
                resp += "Puedes editar esta página: " + FORMULARIO
            else:
                resp += "<br>Not logged in, para editar la pag:"
                resp += "<a href='/login'>Login</a>"
        except Pages.DoesNotExist:
            # Cuando no existe
            if request.user.is_authenticated():
                resp = "Esta página no existe, puedes crearla:"
                resp += FORMULARIO
            else:
                resp = "Not logged in, para crear la pag:"
                resp += " <a href='/login'>Login</a>"
    elif request.method == "POST":
        if request.user.is_authenticated():
            page = request.POST['page']
            try:
                pagina = Pages.objects.get(name=name)
                pagina.page = page  # Write en el cont de la pag lo del formu
                pagina.save()
                resp = "Has modificado la página: <b>"
            except Pages.DoesNotExist:
                pagina = Pages(name=name, page=page)
                pagina.save()
                resp = "Has creado la página: <b>"
            resp += name + "</b><br> Su id es : <b>" + str(pagina.id) + "</b>"
        else:
            resp = "Not logged in: <a href='/login'>Login</a>"
    else:
        resp = "Método no permitido"
    return HttpResponse(resp)
