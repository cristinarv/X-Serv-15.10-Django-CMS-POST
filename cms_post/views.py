# Cristina del Río 
from django.shortcuts import render
from cms_users_put.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
FORMULARIO= """
<form action="" method="POST">
    <u><b>Name: </b></ul><br><input type="text" name="name"><br>
    <u><b>Page: </b></ul><br><input type="text" name="page"/><br>
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
        resp +=  "<ul><li>" + pag.name + " ==> " + pag.page + "</ul></li>"
    return HttpResponse(resp)
  
@csrf_exempt
def pag(request, ident):
    if request.method == "GET":
        try:
			# Cuando existe
            page = Pages.objects.get(name=ident)
            resp = "La página que has pedido es: " + page.name + " ==> " + page.page	
        except Pages.DoesNotExist:
			# Cuando no existe
            if request.user.is_authenticated():
                resp = "Esta página no existe, puedes crearla:" + FORMULARIO
            else:
                resp = 'Not logged in: ' + "<a href='/login'>Login</a>"          
    elif request.method == "POST":
        if request.user.is_authenticated():
            name = request.POST['name']
            page = request.POST['page']
            pagina = Pages(name=name, page=page)
            pagina.save()
            resp = "Has creado la página: <b>" + name + "</b><br> Su id es : <b>" + str(pagina.id) + "</b>"
        else:
            resp = "Necesitas <a href='/admin/login'>hacer login</a>"
    else:
        resp = "Método no permitido"
    return HttpResponse(resp)
