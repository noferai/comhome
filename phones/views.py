from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import PhoneNumber
from .forms import PhoneForm
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import PhoneTable
from users.views import AdminRequiredMixin


class PhonesListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, ListView):
    model = PhoneNumber
    table_class = PhoneTable
    template_name = "crm/list.html"
    export_name = "Telefony"

    def get_context_data(self, **kwargs):
        context = super(PhonesListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'phones:create',
            }
        }
        return {**context, **custom_context}


class PhoneAddView(AdminRequiredMixin, CreateView):
    model = PhoneNumber
    form_class = PhoneForm
    template_name = "crm/create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        if self.request.POST.get("save_new"):
            return redirect("phones:create")
        else:
            return redirect("phones:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(PhoneAddView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'phones:list',
            }
        }
        return {**context, **custom_context}


class PhoneEditView(PhoneAddView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect("phones:list")


class PhoneDeleteView(AdminRequiredMixin, DeleteView):
    model = PhoneNumber

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("phones:list")
