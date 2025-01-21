from django.shortcuts import render
from django.views.generic import FormView
from common.forms import SearchForm

# class SearchFormView(FormView):
#     form_class = SearchForm
#     template_name = 'blog/post_search.html'

#     def form_valid(self, form):
#         searchWord = form.cleaned_data['search_word']
#         game_list = Game.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

#         context = {}
#         context['form'] = form
#         context['search_term'] = searchWord
#         context['object_list'] = game_list

def home(request):
    return render(request, "common/home.html")