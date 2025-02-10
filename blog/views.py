from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q, Count
from django.urls import reverse_lazy
from .models import Post, Category, Recipe, Comment, PostLike
from .forms import PostForm, CommentForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(status='published') |
                Q(status='draft', author=self.request.user)
            )
        else:
            queryset = queryset.filter(status='published')

        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_slug:
            if category_slug != '전체':  # '전체'가 아닐 때만 필터링
                queryset = queryset.filter(category__id=category_slug)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )

        sort = self.request.GET.get('sort', 'latest')
        if sort == 'popular':
            queryset = queryset.annotate(
                popularity_score=Count('likes') + F('view_count')
            ).order_by('-popularity_score', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 기본 컨텍스트 데이터
        context['categories'] = Category.objects.all().order_by('order','name')
        context['sort'] = self.request.GET.get('sort', 'latest')
        context['category'] = None
        context['q'] = self.request.GET.get('q', '')

        # 카테고리 정보
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != '전체':
            context['category'] = get_object_or_404(Category, id=category_slug)

        # 인기 게시물 (검색이나 카테고리 필터가 없을 때만)
        if not (category_slug or context['q']):
            context['popular_posts'] = Post.objects.filter(
                status='published'
            ).annotate(
                popularity_score=Count('likes') + F('view_count')
            ).order_by('-popularity_score')[:3]

        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TINYMCE_JS_URL'] = settings.TINYMCE_JS_URL
        context['TINYMCE_CONFIG'] = settings.TINYMCE_DEFAULT_CONFIG
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'origin'
        return response

    def form_valid(self, form):
        # User 모델 가져오기
        User = get_user_model()

        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = 'draft'
        else:
            form.instance.status = 'published'

        # 현재 사용자를 직접 작성자로 설정
        form.instance.author = self.request.user

        # 포스트 저장
        self.object = form.save()

        # Recipe 생성 로직
        if any([form.cleaned_data.get(field) for field in ['serving_size', 'cooking_time', 'difficulty']]):
            Recipe.objects.create(
                post=self.object,
                serving_size=form.cleaned_data.get('serving_size'),
                cooking_time=form.cleaned_data.get('cooking_time'),
                difficulty=form.cleaned_data.get('difficulty')
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TINYMCE_JS_URL'] = settings.TINYMCE_JS_URL
        context['TINYMCE_CONFIG'] = settings.TINYMCE_DEFAULT_CONFIG
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'origin'  # 추가된 부분
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        
        action = self.request.POST.get('action')
        if action == 'draft':
            form.instance.status = 'draft'
        else:
            form.instance.status = 'published'

        response = super().form_valid(form)
        recipe, created = Recipe.objects.get_or_create(post=self.object)
        recipe.serving_size = form.cleaned_data.get('serving_size')
        recipe.cooking_time = form.cleaned_data.get('cooking_time')
        recipe.difficulty = form.cleaned_data.get('difficulty')
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

        if obj.status == 'draft' and obj.author != self.request.user:
            raise PermissionDenied

        if obj.status == 'published' and self.request.user.is_authenticated and self.request.user != obj.author:
            obj.view_count += 1
            obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 현재 로그인한 사용자 확인
        if self.request.user.is_authenticated:
            context['is_liked'] = PostLike.objects.filter(
                post=self.object,
                user_id=self.request.user.id
            ).exists()
        else:
            context['is_liked'] = False

        # 댓글 폼과 댓글 목록 추가
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')

        # 이전글, 다음글 조회
        context['previous_post'] = Post.objects.filter(
            status='published', 
            created_at__lt=self.object.created_at
        ).order_by('-created_at').first()
        
        context['next_post'] = Post.objects.filter(
            status='published', 
            created_at__gt=self.object.created_at
        ).order_by('created_at').first()

        # 레시피 정보 조회
        context['recipe_detail'] = Recipe.objects.filter(post=self.object).first()
        
        # 관련 게시물 조회
        if self.object.category:
            context['related_posts'] = Post.objects.filter(
                status='published',
                category=self.object.category
            ).exclude(id=self.object.id).order_by('-created_at')[:3]
        else:
            context['related_posts'] = []

        # 좋아요 수 추가
        context['like_count'] = PostLike.objects.filter(post=self.object).count()

        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


@login_required
@require_POST
def toggle_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    try:
        # 좋아요가 이미 있는지 확인
        like = PostLike.objects.get(post=post, user=request.user)
        # 있으면 삭제
        like.delete()
        is_liked = False
    except PostLike.DoesNotExist:
        # 없으면 생성
        PostLike.objects.create(
            post=post,
            user=request.user
        )
        is_liked = True
    
    # 좋아요 수 계산
    like_count = PostLike.objects.filter(post=post).count()
    
    return JsonResponse({
        'is_liked': is_liked,
        'like_count': like_count
    })