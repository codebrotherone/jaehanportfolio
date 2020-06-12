from django.contrib import admin
from .models import Post, ProfileCard

# Register your models here.
# Add Post Model for Blog
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'status', 'created_on')
	list_filter = ("status", )
	search_fields = ['title', 'content']
	prefilled_fields = {'slug': ("title", )}

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('name', 'languages', 'years_exp')
	list_filter = ("years_exp", "languages")
	search_fields = ['name', 'languages']


admin.site.register(Post, PostAdmin)
admin.site.register(ProfileCard, ProfileAdmin)