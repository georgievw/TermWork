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
    tags = Tag.objects.all()
    context = {'articles': articles, 'sites': sites, 'tags': tags}
    return render(request, 'content.html', context)
    
def by_site(request, site_id):
    articles = Article.objects.filter(site=site_id)
    sites = Site.objects.all()
    tags = Tag.objects.all()
    #current_site = Site.objects.get(pk=site_id)
    context = {'articles': articles, 'sites': sites, 'tags': tags}
    return render(request, 'content.html', context)
    
def by_tags(request, tag1_id, tag2_id):
    tag1 = Tag.objects.get(pk=tag1_id) if tag1_id != 0 else 0
    tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
    tag1 = tag2 if tag1_id == 0 else tag1
    
    articles1 = tag1.article_set.all().order_by()
    articles2 = tag2.article_set.all().order_by()
    articles = articles1 & articles2
    sites = Site.objects.all()
    tags = Tag.objects.all()
    context = {'articles': articles.order_by('-published'), 'sites': sites, 'tags': tags}
    return render(request, 'content.html', context)

