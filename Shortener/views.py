from django.shortcuts import render, get_object_or_404,Http404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect


from .forms import submitURL
from .models import URL
#from analytics.models import ClickEvent

# Create your views here.

class home(View):
    def get(self, request, *args, **kwargs):
        the_form = submitURL()
        context={
            "title":"URL Shortener",
            "form":the_form
        }
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        form=submitURL(request.POST)

        context = {
            "title": "TerseURL",
            "form": form,
        }

        template = "home.html"
        if form.is_valid():
            new_url=form.cleaned_data.get("url")
            obj, created=URL.objects.get_or_create(url=new_url)

            context={
                "object": obj,
                "created": created
            }

            if created:
                template="success.html"
            else:
                template="already_exists.html"


        return render(request, template, context)

    def redirect_view(request, shortCode=None, *args, **kwargs):

        obj = get_object_or_404(URL, shortCode=shortCode)
        return HttpResponseRedirect(obj.url)

class URLRedirectView(View):
    def get(self, request, shortCode=None, *args, **kwargs):
        qs=URL.objects.filter(shortCode__iexact=shortCode)
        if  qs.count()!=1 and not qs.exists():
            raise Http404

        obj=qs.first()
        #print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
