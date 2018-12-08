from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect


class DefaultFilterMixIn(admin.ModelAdmin):
    def changelist_view(self, request, *args, **kwargs):
        if self.default_filters:
            test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
            if test and test[-1] and not test[-1].startswith('?'):
                url = reverse('admin:{}_{}_changelist'.format(self.opts.app_label, self.opts.model_name))
                filters = []
                for filter in self.default_filters:
                    key = filter.split('=')[0]
                    if not key in request.GET:
                        filters.append(filter)
                if filters:
                    return HttpResponseRedirect("{}?{}".format(url, "&".join(filters)))

        return super(DefaultFilterMixIn, self).changelist_view(request, *args, **kwargs)
