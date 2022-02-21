from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .models import Article, Site, Tag
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt   
def index(request):
  if request.GET.get("id_ar", 0) != 0:
    article_id = request.GET.get("id_ar") #("id_ar", 1000)
    article = Article.objects.get(pk=article_id)
    if request.user in article.users.all():
      article.users.remove(request.user)
    else:
      article.users.add(request.user)
#    return HttpResponseRedirect('')
    
  else:
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    articles = Article.objects.all()
    
    filter_ids = {}
    
    if tag1_id != 0:
        filter_ids['tag1_id'] = tag1_id
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        filter_ids['tag2_id'] = tag2_id
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        filter_ids['site_id'] = site_id
        articles = articles.filter(site=site_id)

    sites = Site.objects.all()
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    
    paginator = Paginator(articles, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    string = ""
    for tag in filter_ids:
        string = string + "&" + tag + "=" + filter_ids.get(tag)
  
  
    context = {'articles': page.object_list, 'sites': sites, 'tags1': tags1, 'tags2': tags2, 'filter_ids': string, 'page': page}
    return render(request, 'content.html', context)

@csrf_exempt       
@login_required
def my_news(request):
    if not request.user.is_authenticated:
        redirect_to_login('/account/login')
        
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    sites = request.user.site_set.all()         
    articles = Article.objects.filter(site=sites.first())
    filter_ids = {}
    
    for new_site in sites:
        articles = articles | Article.objects.filter(site=new_site)
 
    if tag1_id != 0:
        filter_ids['tag1_id'] = tag1_id    
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        filter_ids['tag2_id'] = tag2_id    
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        filter_ids['site_id'] = site_id
        articles = articles.filter(site=site_id)     
    
    sites = request.user.site_set.all()   
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    
    paginator = Paginator(articles, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    string = ""
    for tag in filter_ids:
        string = string + "&" + tag + "=" + filter_ids.get(tag)
       
    context = {'articles': page.object_list, 'sites': sites, 'tags1': tags1, 'tags2': tags2, 'filter_ids': string, 'page': page}
    return render(request, 'content.html', context)
    
@csrf_exempt      
@login_required    
def my_saved(request):
    if not request.user.is_authenticated:
        redirect_to_login('/account/login')
        
    tag1_id = request.GET.get("tag1_id", 0)
    tag2_id = request.GET.get("tag2_id", 0)
    site_id = request.GET.get("site_id", 0)
    
    articles = request.user.article_set.all()
    filter_ids = {}
    
    if tag1_id != 0:
        filter_ids['tag1_id'] = tag1_id    
        tag1 = Tag.objects.get(pk=tag1_id) 
        articles1 = tag1.article_set.all().order_by()
        articles = articles & articles1
    if tag2_id != 0:
        filter_ids['tag2_id'] = tag2_id   
        tag2 = Tag.objects.get(pk=tag2_id) if tag2_id != 0 else tag1
        articles2 = tag2.article_set.all().order_by()
        articles = articles & articles2
    if site_id != 0:
        filter_ids['site_id'] = site_id
        articles = articles.filter(site=site_id)      
   
    sites = Site.objects.all()
    tags1 = Tag.objects.filter(tag='Мир') | Tag.objects.filter(tag='Россия')
    tags2 = Tag.objects.exclude(tag='Мир') & Tag.objects.exclude(tag='Россия')
    
    paginator = Paginator(articles, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    string = ""
    for tag in filter_ids:
        string = string + "&" + tag + "=" + filter_ids.get(tag)    
    
    context = {'articles': page.object_list, 'sites': sites, 'tags1': tags1, 'tags2': tags2, 'filter_ids': string, 'page': page}
    return render(request, 'content.html', context)

@csrf_exempt     
@login_required    
def my_settings(request):
    if not request.user.is_authenticated:
        redirect_to_login('/account/login')
        
    del_sites = request.GET.get("del_sites", 0)
    add_sites = request.GET.get("add_sites", 0)
    if del_sites != 0:
      Site.objects.get(pk=del_sites).users.remove(request.user)
    if add_sites != 0:
      Site.objects.get(pk=add_sites).users.add(request.user)
      
    my_sites = request.user.site_set.all().order_by()
    all_sites = Site.objects.all().order_by().difference(my_sites)
    context = {'my_sites': my_sites, 'all_sites': all_sites}
    return render(request, 'settings.html', context)


