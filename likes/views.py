from django.shortcuts import render
from django.http.response import JsonResponse

from likes.models import Post
from likecounter.producer import send_likes_event

def post_like(request,post_id):
    send_likes_event(post_id=post_id)
    # post = Post.objects.get(id=post_id)
    # post.like += 1
    # post.save()
    return JsonResponse({
        "status" : True,
        "message" : "post liked"
    })