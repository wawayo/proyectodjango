from django.contrib import admin

# Register your models here.

# Todos lo usuarion podrán en sus propias recetas editar, eliminar y crear recetas.

from .models import Post, Comentario, Favorito

admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Favorito)