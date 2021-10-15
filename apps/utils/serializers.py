# -*- coding: utf-8 -*-
# Django
from django.utils.encoding import smart_text
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.urls import reverse, NoReverseMatch
# Third Parties
from rest_framework.relations import RelatedField


class CustomSlugRelatedField(RelatedField):
    """
    A read-write field the represents the target of the relationship
    by a unique 'slug' attribute.
    """
    default_error_messages = {
        'does_not_exist': _('Object with {slug_name}={value} does not exist.'),
        'invalid': _('Invalid value.'),
        'required_select': _("You've got to select a value"),
    }

    lookup_field = 'pk'

    def __init__(self,
                 slug_field=None,
                 if_not_exists_return_data=False,
                 if_not_exists_return_obj=False,
                 view_name=None,
                 **kwargs):
        assert slug_field is not None, 'The `slug_field` argument is required.'
        self.slug_field = slug_field

        self.view_name = view_name
        self.if_not_exists_return_data = if_not_exists_return_data
        self.if_not_exists_return_obj = if_not_exists_return_obj
        self.allow_empty = kwargs.pop('allow_empty', True)
        self.format = kwargs.pop('format', None)
        self.additional_fields = kwargs.pop('additional_fields', [])

        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)
        self.reverse = reverse

        self.many_related = kwargs.pop('many_related', False)

        super(CustomSlugRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if self.many_related:
            if isinstance(data, type('')) or not hasattr(data, '_iter_'):
                self.fail('not_a_list', input_type=type(data).__name__)

            if not self.allow_empty and len(data) == 0:
                self.fail('empty')

            objects = []

            for item in data:
                if 'id' in item:
                    objects.append(self.get_queryset().get(pk=item['id']))
                else:
                    self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(item))
            return objects
        else:
            if self.if_not_exists_return_data and not 'id' in data:
                return data

            if self.if_not_exists_return_obj and not 'id' in data:
                obj = self.queryset.model()
                for field in self.queryset.model._meta.get_fields():
                    if field.name in data:
                        setattr(obj, field.name, data[field.name])
                return obj

            try:
                data = int(float(data))
                return self.get_queryset().get(pk=data)
            except Exception as e:
                if type(data).__name__ == "int":
                    raise e

            try:
                if 'id' in data:
                    if not data['id'] > 0:
                        self.fail('required_select')
                    return self.get_queryset().get(pk=data['id'])
                else:
                    if data == "None":
                        return None
                    self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))

            except ObjectDoesNotExist:
                self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
            except (TypeError, ValueError):
                self.fail('invalid')

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if obj.pk is None:
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)

    def to_representation(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)

        assert request is not None, (
                "`%s` requires the request in the serializer"
                " context. Add `context={'request': request}` when instantiating "
                "the serializer." % self._class.name_
        )

        if self.many_related:
            data = []
            for o in obj.all():
                object_dict = {}
                try:
                    if self.view_name:
                        url = self.get_url(o, self.view_name, request, format)
                    else:
                        url = "not_configured"

                    object_dict = {
                        'id': o.pk,
                        'get_unicode': getattr(o, self.slug_field),
                        'url': url
                    }

                    for field in self.additional_fields:
                        if field == 'url' and self.view_name is None:
                            msg = "URL Field without view_name in CustomSlugRelatedField"
                            raise ImproperlyConfigured(msg)

                        if isinstance(field, dict):
                            nested_data = {}
                            nested_o = getattr(o, field['name'])

                            for nested_field in field['fields']:
                                nested_data[nested_field] = getattr(nested_o, nested_field)

                            object_dict[field['name']] = nested_data
                        else:
                            object_dict[field] = getattr(o, field)

                except NoReverseMatch:
                    msg = (
                        'Could not resolve URL for hyperlinked relationship using '
                        'view name "%s". You may have failed to include the related '
                        'model in your API, or incorrectly configured the '
                        '`lookup_field` attribute on this field.'
                    )
                    raise ImproperlyConfigured

                data.append(object_dict)
            return data
        else:
            try:
                if self.view_name:
                    url = self.get_url(obj, self.view_name, request, format)
                else:
                    url = "not_configured"

                data = {
                    'id': obj.pk,
                    'get_unicode': getattr(obj, self.slug_field),
                    'url': url
                }

                for field in self.additional_fields:
                    if field == 'url' and self.view_name is None:
                        msg = "URL Field without view_name in CustomSlugRelatedField"
                        raise ImproperlyConfigured(msg)

                    if isinstance(field, dict):
                        nested_data = {}
                        nested_obj = getattr(obj, field['name'])

                        if nested_obj:
                            for nested_field in field['fields']:
                                try:
                                    nested_data[nested_field] = getattr(nested_obj, nested_field)
                                except Exception as e:
                                    if isinstance(nested_field, dict):
                                        nested_data[nested_field['name']] = {}
                                        for nested_field_2 in nested_field['fields']:
                                            nested_obj_2 = getattr(nested_obj, nested_field['name'])
                                            nested_data[nested_field['name']][nested_field_2] = getattr(nested_obj_2,
                                                                                                        nested_field_2)
                                    else:
                                        nested_data[nested_field] = "Mal configurado"
                        else:
                            nested_data = None
                        data[field['name']] = nested_data
                    else:
                        data[field] = getattr(obj, field)
                return data
            except NoReverseMatch:
                msg = (
                    'Could not resolve URL for hyperlinked relationship using '
                    'view name "%s". You may have failed to include the related '
                    'model in your API, or incorrectly configured the '
                    '`lookup_field` attribute on this field.'
                )
                raise ImproperlyConfigured(msg % self.view_name)
