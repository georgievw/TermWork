#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from .models import Article

#def index(request):
#    template = loader.get_template('index.html')
#    aas = Article.objects.order_by('-published')    
#    context = {'aas': aas}    
#    return HttpResponse(template.render(context, request))
    
def index(request):
    aas = Article.objects.order_by('-published') 
    return render(request, 'index.html', {'aas': aas})
