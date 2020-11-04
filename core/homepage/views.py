from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    # -> vista generica
    template_name = 'index.html'
