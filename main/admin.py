from django.contrib import admin
import datetime

from .models import AdvUser, SuperRubric, SubRubric, AdditionalImage, Bb, Comment
from .utilities import send_activation_notification
from .forms import SubRubricForm


def send_activation_notification(modelAdmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modelAdmin.message_user(request, 'Письма с оповещениями отправлены')


send_activation_notification.short_description = 'Отправка писем с оповещениями об активации'


class NonActivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Активирован'),
            ('threedays', 'Не активировал более 3 дней'),
            ('week', 'Не активировал более недели')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonActivatedFilter,)
    fields = (
        ('username', 'email'), ('first_name', 'last_name'),
        ('send_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups', 'user_permissions',
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notification,)


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
    list_display = ('__str__', 'order')


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
    list_display = ('__str__', 'order')


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class CommentInline(admin.TabularInline):
    model = Comment


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline, CommentInline)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('bb', 'author', 'content', 'created_at')
    list_filter = ('bb', 'author', 'created_at')


admin.site.register(Bb, BbAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Comment, CommentAdmin)
