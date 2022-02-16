#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render

from .models import Article, Site, Tag

#def index(request):
#    template = loader.get_template('index.html')
#    aas = Article.objects.order_by('-published')    
#    context = {'aas': aas}    
#    return HttpResponse(template.render(context, request))
    
def index(request):
    articles = Article.objects.order_by('-published') 
    sites = Site.objects.all()
    return render(request, 'index.html', {'articles': articles, 'sites': sites})
    
def by_site(request, site_id):
    articles = Article.objects.filter(site=site_id)
    sites = Site.objects.all()
    current_site = Site.objects.get(pk=site_id)
    context = {'articles': articles, 'sites': sites, 'current_site': current_site}
    return render(request, 'by_site.html', context)
