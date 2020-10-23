

# Register your models here.
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from django.contrib import admin
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):  # StackedInline 样式不同
    fields = (
        'title',
        'desc'
    )
    extra = 1  # 控制额外多几个
    model = Post



@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = (
        'name',
        'status',
        'is_nav',
        'post_count',
        'created_time'
    )
    fields = (
        'name',
        'status',
        'is_nav',
        'owner'
    )

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"



@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = (
        'name',
        'status',
        'created_time'
    )
    fields = (
        'name',
        'status'
    )

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)



class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户的分类"""

    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset



@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = (
        'title',
        'category',
        'status',
        'owner',
        'created_time',
        'operator'
    )
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = [
        'title',
        'category__name'
    ]

    # actions_on_top = False
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    exclude = ('owner',)

    filter_horizontal = ('tag',)
    # filter_vertical = ('tag', )

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )

    fieldsets = (
        ('基础配置', {
           'description': '基础配置描述',
           'fields': (
               ('title', 'category'),
               'status',
           ) ,
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'


    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)


    class Media:
        css = {
            # 'all': ("https://cdn.jsdelivr.net/npm/bootstrap@4.5.0/dist/css/bootstrap.min.css", ),
        }
        js = (
            # 'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js',
            # 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
            # 'https://cdn.jsdelivr.net/npm/bootstrap@4.5.0/dist/js/bootstrap.min.js'
        )


