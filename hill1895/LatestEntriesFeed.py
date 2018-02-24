# -*- coding:utf8 -*-
from django.contrib.syndication.views import Feed
from hill1895.models import Blog


class LatestEntriesFeed(Feed):
    title = u"mikelee"
    link = "hill1895.rocks"
    description = "关注mikelee的最新动态"

    def items(self):
        return Blog.objects.order_by('-pub_time')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return "/blog_detail/blog_" + str(item.id)
