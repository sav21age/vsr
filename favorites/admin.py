from django.contrib import admin
from favorites.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)\
            .prefetch_related('content_object')

    list_display = ('id', 'get_user', 'get_content_object')
    readonly_fields = ('object_id', 'user', 'content_type', 'content_object')
    search_fields = ('user__username', )

    def get_user(self, obj=None):
        if obj:
            return f"{obj.user}"
        return ''
    get_user.short_description = 'пользователь'

    def get_content_object(self, obj=None):
        if obj:
            return f"{obj.content_object}"
        return ''
    get_content_object.short_description = 'товар'

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False
    