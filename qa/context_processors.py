from qa.models import Category


def global_context(request):
    categories = Category.objects.order_by('title')
    context = {
        'categories': categories
    }
    return context
