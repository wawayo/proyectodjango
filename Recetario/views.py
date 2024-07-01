from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

def welcome_view(request):
    return render(request, 'Recetario/welcome.html')

def recetas_view(request):
    recetas = Post.objects.order_by('-fecha_creacion')
    return render(request, 'Recetario/recetas.html', {'recetas': recetas})

def perfil_view(request):
    recetas = Post.objects.filter(autor_id=request.user.id)
    return render(request, 'Recetario/perfil.html', {'recetas': recetas})

def detalle_receta(request, id):
    try:
        receta = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(receta_id=id)
        return render(request, 'Recetario/detalle_receta.html', {'receta': receta, 'comentarios': comentarios})
    except Post.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')
def receta_create(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        ingredientes = request.POST['ingredientes']
        descripcion = request.POST['descripcion']
        instrucciones = request.POST['instrucciones']
        autor_id = request.POST['autor_id']
        imagen = request.FILES.get('imagen')
        receta = Post(titulo=titulo, ingredientes=ingredientes, descripcion=descripcion, instrucciones=instrucciones, autor_id=autor_id, imagen=imagen)
        receta.save()

        return redirect('perfil')
    else:
        return render(request, 'Recetario/crear_receta.html')

@login_required(login_url='/accounts/login/')  
def receta_edit(request, id):
    if request.user.id != Post.objects.get(id=id).autor_id:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes editar esta receta'})
    try:
        receta = Post.objects.get(id=id)
        if request.method == 'POST':
            receta.titulo = request.POST['titulo']
            receta.ingredientes = request.POST['ingredientes']
            receta.descripcion = request.POST['descripcion']
            receta.instrucciones = request.POST['instrucciones']

            nueva_imagen = request.FILES.get('imagen')
            if nueva_imagen:
                receta.imagen = nueva_imagen

            receta.save()
            return redirect('detalle-receta', id=id)
        else:
            return render(request, 'Recetario/editar_receta.html', {'receta': receta})
    except Post.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')
def receta_delete (request, id):
    if request.user.id != Post.objects.get(id=id).autor_id:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes eliminar esta receta'})
    try:
        receta = Post.objects.get(id=id)
        receta.delete()
        return redirect('perfil')
    except Post.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')   
def comentario_create(request):
    if request.method == 'POST':
        autor_id = request.POST['autor_id']
        receta_id = request.POST['receta_id']
        texto = request.POST['texto']
        comentario = Comentario(autor_id=autor_id, receta_id=receta_id, texto=texto)
        comentario.save()
        return redirect('detalle-receta', id=receta_id)
    else:
        return redirect('recetas')
    
@login_required(login_url='/accounts/login/')
def comentario_delete(request, id):
    try:
        comentario = Comentario.objects.get(id=id)
        receta_id = comentario.receta_id

        if request.user.id == comentario.autor_id or request.user.id == Post.objects.get(id=receta_id).autor_id:
            comentario.delete()
            return redirect('detalle-receta', id=receta_id)
        else:
            return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes eliminar este comentario'})
    except Comentario.DoesNotExist:
        return redirect('detalle-receta', id=receta_id)
   
def buscar_receta(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        nombre = Post.objects.filter(titulo__contains=titulo)
        ingredientes = Post.objects.filter(ingredientes__contains=titulo)
        descripcion = Post.objects.filter(descripcion__contains=titulo)
        recetas = nombre.union(ingredientes, descripcion)

        if recetas.count() == 0:
            return render(request, 'Recetario/recetas.html', {'recetas': recetas, 'mensaje': 'No se encontraron resultados'})
        
        return render(request, 'Recetario/recetas.html', {'recetas': recetas})

    else:
        return redirect('recetas')