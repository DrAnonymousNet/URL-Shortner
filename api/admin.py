from django.contrib import admin
from django.urls import reverse
from .models import *
from django.utils.translation import gettext_lazy as _
# Register your models here.

class UnInvitedFilter(admin.SimpleListFilter):
    title = _("Stale")

    parameter_name: str = "stale"

    def lookups(self, request, model_admin):
        return (
            ["stale", _("stale")]
        )

    def queryset(self, request, queryset):


        if self.value() == "stale":
            return queryset.filter(last_visited_date__lte = timezone.now() - timedelta(days=1))

class AnalyticInline(admin.TabularInline):
    model = Analytic
    readonly_fields = ["device", "os","browser","country","referer"]

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("owner","long_link","short_link", "visit_count",'date_created', "last_visited_date", "analytic")
    fields = ["owner","long_link", "analytic"]
    readonly_fields = ["analytic", "visit_count"]
    list_filter = (
                    ("last_visited_date",admin.EmptyFieldListFilter),
                    )
    save_as: bool = True
    list_select_related = ["analytic"]
    list_display_links = ["analytic", "owner"]
    inlines = [AnalyticInline]
    
    date_hierarchy = "last_visited_date"
    empty_value_display = "No Value"



admin.site.register(Analytic)
admin.site.register(AnalyticByDateTime)
admin.site.register(TotalRedirection)
