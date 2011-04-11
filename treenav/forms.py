from django import forms
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator

from treenav.models import MenuItem
from mptt.forms import TreeNodeChoiceField


class MenuItemForm(forms.ModelForm):
    new_parent = TreeNodeChoiceField(
        queryset=MenuItem.tree.all(),
        required=False,
    )

    class Meta:
        model = MenuItem

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['new_parent'].queryset = \
                MenuItem.objects.exclude(pk=self.instance.pk)

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
        super(MenuItemForm, self).clean()
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if (content_type and not object_id) or (not content_type and object_id):
            raise forms.ValidationError(
                "Both 'Content type' and 'Object id' must be specified to use generic relationship"
            )
        if content_type and object_id:
            try:
                obj = content_type.get_object_for_this_type(pk=object_id)
            except ObjectDoesNotExist, e:
                raise forms.ValidationError(str(e))
            try:
                obj.get_absolute_url()
            except AttributeError, e:
                raise forms.ValidationError(str(e))

        if 'is_enabled' in self.cleaned_data and \
          self.cleaned_data['is_enabled'] and \
          'link' in self.cleaned_data and \
          self.cleaned_data['link'].startswith('^'):
            raise forms.ValidationError('Menu items with regular expression '
                                        'URLs must be disabled.')
        return self.cleaned_data

    def save(self, commit=True):
        # ## WARNING ##
        # (1) respect the caller's commit argument, so that the form will
        # have a save_m2m method when commit=False
        instance = super(MenuItemForm, self).save(commit=commit)
        # (2) if commit is False, we have to save the form anyway, because
        # the instance must be saved to call move_to
        if not commit:
            instance.save()
        # reorganize if necessary
        if self.cleaned_data['new_parent']:
            parent = self.cleaned_data['new_parent']
        else:
            parent = instance.parent
        if parent:# pragma: no cover
            try:
                node = parent.get_children().order_by('order').filter(
                    order__gte=instance.order
                ).exclude(pk=instance.id)[0]
                position = 'left'
            except IndexError:
                node = parent
                position = 'last-child'
            instance.move_to(node, position=position)
        return instance


class GenericInlineMenuItemForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=MenuItem.tree.all()
    )
    class Meta:
        model = MenuItem
        fields = ('parent', 'label', 'slug', 'order', 'is_enabled')

