from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from celery import chain

from .forms import SongModelForm
from .tasks import chain_tasks


class IndexView(generic.CreateView):
    template_name = 'website/index.html'
    form_class = SongModelForm
    success_url = reverse_lazy('music:index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            chain_tasks(form.cleaned_data['link'], form.cleaned_data['email']).apply_async()
            form.save()
            posted = True
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form, 'posted': posted})
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
