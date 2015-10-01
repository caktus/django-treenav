from django import forms
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator

from treenav.models import MenuItem
from mptt.forms import TreeNodeChoiceField, MPTTAdminForm


class MenuItemFormMixin(object):

    def clean_link(self):
        link = self.cleaned_data['link'] or ''
        # It could be a fully-qualified URL -- try that first b/c reverse()
        # chokes on "http://"
        if any([link.startswith(s) for s in ('http://', 'https://')]):
            URLValidator()(link)
        elif link and not any([link.startswith(s) for s in ('^', '/')]):
            # Not a regex or site-root-relative absolute path -- see if it's a
            # named URL or view
            try:
                reverse(link)
            except NoReverseMatch:
                raise forms.ValidationError('Please supply a valid URL, URL '
                                            'name, or regular expression.')
        return self.cleaned_data['link']

    def clean(self):
        super(MenuItemFormMixin, self).clean()
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if (content_type and not object_id) or (not content_type and object_id):
            raise forms.ValidationError(
                "Both 'Content type' and 'Object id' must be specified to use generic relationship"
            )
        if content_type and object_id:
            try:
                obj = content_type.get_object_for_this_type(pk=object_id)
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(str(e))
            try:
                obj.get_absolute_url()
            except AttributeError as e:
                raise forms.ValidationError(str(e))

        if 'is_enabled' in self.cleaned_data and \
           self.cleaned_data['is_enabled'] and \
           'link' in self.cleaned_data and \
           self.cleaned_data['link'].startswith('^'):
            raise forms.ValidationError('Menu items with regular expression '
                                        'URLs must be disabled.')
        return self.cleaned_data


class MenuItemForm(MenuItemFormMixin, MPTTAdminForm):

    class Meta:
        model = MenuItem
        fields = "__all__"


class MenuItemInlineForm(MenuItemFormMixin, forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = "__all__"


class GenericInlineMenuItemForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=MenuItem.objects.all(),
        required=False
    )

    class Meta:
        model = MenuItem
        fields = ('parent', 'label', 'slug', 'order', 'is_enabled')
