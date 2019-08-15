from django import template
from ComfortableHome import settings
# from django.utils.formats import dateformat
# from django.urls import reverse

register = template.Library()


@register.simple_tag
def website_title(_objects=False):
    if _objects:
        return _objects.model._meta.verbose_name_plural.title() + " - " + settings.TITLE
    else:
        return settings.TITLE


@register.simple_tag
def verbose_name_plural(_model):
    return _model._meta.verbose_name_plural.title()
#
# @register.simple_tag
# def get_field(_object, _field_name):
#     return _object._meta.get_field(_field_name)
#
#
# @register.simple_tag
# def field_label(_field):
#     if _field.is_relation:
#         return _field.related_model._meta.verbose_name
#     else:
#         return _field.verbose_name
#
#
# @register.simple_tag
# def field_value(_object, _field):
#     if _field.is_relation:
#         if _field.many_to_many:
#             kwargs = {_field.m2m_field_name() if _field.concrete else _field.field.name: _object}
#             if _field.related_model.objects.filter(**kwargs).exists():
#                 return _field.related_model.objects.filter(**kwargs)[0]
#             else:
#                 return False
#         else:
#             _id = _field.value_from_object(_object)
#             return _field.related_model.objects.get(pk=_id)
#     elif _field.get_internal_type() == 'DateField':
#         return dateformat.format(_field.value_from_object(_object), "d.m.Y")
#     else:
#         return _field.value_from_object(_object)
#
#
# @register.simple_tag(takes_context=True)
# def related_url(context, _object, _field):
#     url = context['urls'][str(_field.name)]
#     if _field.many_to_many:
#         kwargs = {_field.m2m_field_name() if _field.concrete else _field.field.name: _object}
#         if _field.related_model.objects.filter(**kwargs).exists():
#             _id = _field.related_model.objects.filter(**kwargs)[0].id
#             return reverse(url, args=[_id])
#         else:
#             return False
#     else:
#         _id = _field.value_from_object(_object)
#         if url and _id:
#             return reverse(url, args=[_id])
#         else:
#             return False
