from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from zion.articles.forms import NewArticleForm
from zion.comments.forms import NewCommentForm
from zion.signin.models import User
from zion.forums.models import Forum
from zion.articles.models import Article
from zion.comments.models import Comment
from zion.tags.models import Tag
from zion.forums.views import page_display

def new_post(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id) 
    except Forum.DoesNotExist:
         return Http404
            
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article = Article.objects.create(forum=forum,
                                       title=cd['name'].strip(),
                                       author=request.user,
                                       text=cd['body'],
                                       post_date=datetime.now())
            forum.article_set.add(article)
            Forum.objects.filter(id=forum_id).update(articles = forum.article_set.count())
            Forum.objects.filter(id=forum_id).update(last_author = request.user)
            Forum.objects.filter(id=forum_id).update(last_postdate = article.post_date)

            request.user.article_set.add(article)
            User.objects.filter(id=request.user.id).update(articles = request.user.article_set.count())
            # insert new tag or add article to existing tag
            keywords = request.POST['keywords'].split(',');
            for kw in keywords:
                if kw != '':
                    if Tag.objects.filter(keyword=kw).count() == 0:
                        tag = Tag.objects.create(keyword=kw, article_count=1, proposed_date=article.post_date);
                        tag.articles.add(article)
                    else:
                        tag = Tag.objects.get(keyword=kw)
                        tag.articles.add(article)
                        Tag.objects.filter(keyword=kw).update(article_count=tag.articles.count())
                        
                        
            return HttpResponseRedirect('/forum/{0}/'.format(forum_id))

    else:
        form = NewArticleForm()

    return render(request, 
                  'new_article_form.html',
                  {'user': request.user,
                   'forum_id': forum.id,
                   'forum_topic': forum.topic,
                   'forum_name': forum.name,
                   'form': form,
                  })
                
def article_detailview(request, forum_id, article_id, page=1, **kwargs):
    try:
        page = int(page)
    except ValueError:
        raise Http404

    pages = page_display(page, forum_id, article_id=article_id)

    comment_form = NewCommentForm()

    if 'error_form' in kwargs:
        comment_form = kwargs['error_form']
    if 'comment_success' in kwargs:
        is_success = True 
        page = pages['count']
        pages = page_display(page, forum_id, article_id=article_id)
        
    else:
        is_success = False

    
    article = Article.objects.get(id=article_id)
    tag_list = article.tag_set.all()
        

    been_commented = True 
    been_collected = True
    if request.user.is_authenticated:
        try:
            Comment.objects.get(poster_id=request.user.id, article_id=pages['article'].id) 
        except Comment.DoesNotExist:
            been_commented = False

        count = article.collected_users.filter(id=request.user.id).count()
        if count ==  0:   # not yet collected
            been_collected = False
            
    

    return render(request,
                  'article_view.html',
                  { 'user': request.user,
                    'form': comment_form,
                    'forum':pages['forum'],
                    'article':article,
                    'tag_list': tag_list,
                    'page':page,
                    'prev_page':page - 1,
                    'next_page':page + 1,
                    'page_count':pages['count'],
                    'comment_list':pages['list'],
                    'comment_success':is_success,
                    'been_commented': been_commented,
                    'been_collected': been_collected,
                  })

def collect(request, forum_id, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        count = article.collected_users.filter(id=request.user.id).count()
        if count ==  0:   # not yet collected
            request.user.collected_articles.add(article) 
        else:
            request.user.collected_articles.remove(article)
        return HttpResponseRedirect('/forum/{0}/article/{1}'.format(forum_id, article_id))
    else:
        raise Http404


@ajax
@csrf_exempt
def flip_thumb(request, forum_id, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(id=article_id)
        count = article.agreed_users.filter(id=request.user.id).count()
        if count > 0:
            return {'been_agreed': 1}
        else:
            article.agreed_users.add(request.user)
            Article.objects.filter(id=article_id).update(likes = article.agreed_users.count())
            return {'been_agreed': 0, 'likes':article.agreed_users.count()}
