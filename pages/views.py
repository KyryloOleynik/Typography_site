from django.shortcuts import render
from banners.models import Banner
from catalog.models import Service, ServiceCategory
from core.utils import get_base_info
from news.models import News

def about_us(request):
    main_data = get_base_info(request)
    return render(request, 'pages/about_us.html', {**main_data })

def main(request):
    target_category = None
    main_data = get_base_info(request)
    popular_categories = ServiceCategory.objects.prefetch_related('services').filter(services__isnull=False).distinct()[:6]
    news_about_store = News.objects.filter(related_to_store=True).order_by('-created_at').first()
    recent_news = News.objects.order_by('-created_at')[:4]
    
    if request.method == "GET":
        category_slug = request.GET.get('category')
        if category_slug:
            try:
                target_category = ServiceCategory.objects.get(slug=category_slug)
            except ServiceCategory.DoesNotExist:
                target_category = None
        else:
            target_category = list(popular_categories)[0] if popular_categories else None

    new_banners = Banner.objects.all().order_by('-created_at')[:4]

    return render(request, 'pages/main.html', {'new_banners': new_banners, 'target_category': target_category, 'popular_categories': popular_categories, 'news_about_store': news_about_store, 'recent_news': recent_news, **main_data})

def pay_delivery(request):
    main_data = get_base_info(request)
    return render(request, 'pages/pay_delivery.html', {**main_data })

def question_answer(request):
    main_data = get_base_info(request)
    return render(request, 'pages/question_answer.html', {**main_data })

def portfolio_view(request):
    main_data = get_base_info(request)
    return render(request, 'pages/portfolio.html', {**main_data})

def return_policy_view(request):
    main_data = get_base_info(request)
    return render(request, 'pages/return_policy.html', {**main_data})

def terms_of_use_view(request):
    main_data = get_base_info(request)
    return render(request, 'pages/terms_of_use.html', {**main_data})

def privacy_policy_view(request):
    main_data = get_base_info(request)
    return render(request, 'pages/privacy_policy.html', {**main_data})