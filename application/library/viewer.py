from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
def page(data,page_num):
    paginator =  Paginator(data, settings.PAGE_SIZE)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
