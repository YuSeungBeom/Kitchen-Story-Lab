from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from .models import Post, Category, Recipe
from .forms import PostForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )

        sort = self.request.GET.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.order_by('-view_count', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 기본 컨텍스트 데이터
        context['categories'] = Category.objects.all()
        context['sort'] = self.request.GET.get('sort', 'latest')
        context['category'] = None
        context['q'] = self.request.GET.get('q', '')

        # 카테고리 정보
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['category'] = Category.objects.filter(slug=category_slug).first()

        # 인기 게시물 (검색이나 카테고리 필터가 없을 때만)
        if not (category_slug or context['q']):
            context['popular_posts'] = Post.objects.filter(
                status='published'
            ).order_by('-view_count', '-created_at')[:3]

        return context

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        response = super().form_valid(form)
        
        # 레시피 정보가 있는 경우 저장
        if any([form.cleaned_data.get(field) for field in ['serving_size', 'cooking_time', 'ingredients', 'instructions']]):
            Recipe.objects.create(
                post=self.object,
                serving_size=form.cleaned_data.get('serving_size'),
                cooking_time=form.cleaned_data.get('cooking_time'),
                difficulty=form.cleaned_data.get('difficulty'),
                ingredients=form.cleaned_data.get('ingredients'),
                instructions=form.cleaned_data.get('instructions')
            )
        return response

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        response = super().form_valid(form)
        recipe, created = Recipe.objects.get_or_create(post=self.object)
        recipe.serving_size = form.cleaned_data.get('serving_size')
        recipe.cooking_time = form.cleaned_data.get('cooking_time')
        recipe.difficulty = form.cleaned_data.get('difficulty')
        recipe.ingredients = form.cleaned_data.get('ingredients')
        recipe.instructions = form.cleaned_data.get('instructions')
        recipe.save()
        return response

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class SearchView(generic.ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        queryset = Post.objects.filter(status='published')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['categories'] = Category.objects.all()
        return context

    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = self.object
        
        # Retrieve previous and next posts within published status
        context['previous_post'] = Post.objects.filter(
            status='published', 
            created_at__lt=current_post.created_at
        ).order_by('-created_at').first()
        
        context['next_post'] = Post.objects.filter(
            status='published', 
            created_at__gt=current_post.created_at
        ).order_by('created_at').first()

        # Fetch recipe details for the current post
        context['recipe_detail'] = Recipe.objects.filter(post=current_post).first()
        
        # Find related posts in the same category
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=current_post.category
        ).exclude(id=current_post.id).order_by('-created_at')[:3]

        return context        