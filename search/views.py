from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import View
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.conf import settings
from django.db.models import Q

from blog.models import Post


class SearchView(View):
    template_name = 'search/index.html'

    def get(self, request):
        context = {}
        query = request.GET.get('q')
        if query is not None:
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                results = Post.published.filter(Q(body__icontains=query) | Q(description__icontains=query) |
                                       Q(title__icontains=query))
            else:
                results = Post.published.annotate(similarity=TrigramSimilarity('body', query),)\
                    .filter(similarity__gt=0.3).order_by('-similarity')
            context['last_question'] = '?q=%s' % query
            paginator = Paginator(results, 2)
            page = request.GET.get('page')
            try:
                context['results'] = paginator.page(page)
            except PageNotAnInteger:
                context['results'] = paginator.page(1)
            except EmptyPage:
                context['results'] = paginator.page(paginator.num_pages)

        return render(request, template_name=self.template_name, context=context)
