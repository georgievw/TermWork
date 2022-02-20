from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required

from .models import Article, Site, Tag
from django.contrib.auth.models import User
   
def index(request):
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    articles = Article.objects.all()
    
    if tag1_id != 0:
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        articles = articles.filter(site=site_id)
    
    sites = Site.objects.all()
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    context = {'articles': articles, 'sites': sites, 'tags1': tags1, 'tags2':tags2}
    return render(request, 'content.html', context)
    
@login_required
def my_news(request):
    if not request.user.is_authenticated:
        redirect_to_login('/account/login')
        
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    sites = request.user.site_set.all()         
    articles = Article.objects.filter(site=sites.first())
    for new_site in sites:
        articles = articles | Article.objects.filter(site=new_site)
 
    if tag1_id != 0:
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        articles = articles.filter(site=site_id)     
    
    sites = request.user.site_set.all()   
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    context = {'articles': articles, 'sites': sites, 'tags1': tags1, 'tags2':tags2}
    return render(request, 'content.html', context)
   
@login_required    
def my_saved(request):
    if not request.user.is_authenticated:
        redirect_to_login('/account/login')
        
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    articles = request.user.article_set.all()
    
    if tag1_id != 0:
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        articles = articles.filter(site=site_id)      
   
    sites = Site.objects.all()
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    context = {'articles': articles, 'sites': sites, 'tags1': tags1, 'tags2':tags2}
    return render(request, 'content.html', context)

def my_settings(request):
    return render(request, 'settings.html')


