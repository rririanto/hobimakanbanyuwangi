from django.contrib import admin
from django.forms import ModelForm
from culinary.models import CulinaryPlace as Culinary

class CulinaryAdmin(admin.ModelAdmin):  
  list_display = [field.name for field in Culinary._meta.fields if field.name not in ["id", "watchcount", "slug", "unique_id", "shortcode", "typename", "verified", "photo", "date_created", "date_modified"]]
  search_fields = ('name',)
  ordering = ('-id',) # The negative sign indicate descendent order
  def get_queryset(self, request):
        return super(CulinaryAdmin, self).get_queryset(request).prefetch_related('tags')

admin.site.register(Culinary, CulinaryAdmin)

