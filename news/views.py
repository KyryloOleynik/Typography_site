from django.shortcuts import render, redirect
from core.utils import get_base_info
from .models import News
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def news_main(request):
    main_data = get_base_info(request)
    news = News.objects.all().order_by('-created_at')
    paginator = Paginator(news, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/main.html', {'news': page_obj, 'page_obj': page_obj, **main_data, })

def view_news(request, slug):
    main_data = get_base_info(request)
    
    try:
        target_news = News.objects.get(slug=slug)
    except News.DoesNotExist:
        messages.error(request, 'Новину не знайдено.')
        return redirect('news:main_news')

    recomended_news = News.objects.exclude(id=target_news.id)[:4] 
    
    return render(request, 'news/view_news.html', {'target_news': target_news, 'recomended_news': recomended_news, **main_data })
