from django.shortcuts import redirect
from users.views import AdminRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .models import Document
from .forms import DocumentForm
from .tables import DocumentTable, DocumentFilter


class DocumentsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Document
    table_class = DocumentTable
    template_name = "crm/list.html"
    export_name = "Documenty"
    filterset_class = DocumentFilter

    def get_context_data(self, **kwargs):
        context = super(DocumentsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'documents:create',
            }
        }
        return {**context, **custom_context}


class DocumentAddView(AdminRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "crm/create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.POST.get("save_new"):
            return redirect("documents:create")
        else:
            return redirect("documents:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(DocumentAddView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'documents:list',
            }
        }
        return {**context, **custom_context}


class DocumentEditView(DocumentAddView, UpdateView):
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
        return redirect("documents:list")


class DocumentDeleteView(AdminRequiredMixin, DeleteView):
    model = Document

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("documents:list")
