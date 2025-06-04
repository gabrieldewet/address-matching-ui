from django import forms

from .utils import Address


class AddressForm(forms.Form):
    raw_text = forms.CharField(
        label="Raw Address Text",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
                "hx-trigger": "keyup changed delay:500ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
                "style": "resize: none; height: 100px;",
            }
        ),
    )
    street_name = forms.CharField(
        label="Street Name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )
    street_number = forms.CharField(
        label="Street Number",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )
    box_number = forms.CharField(
        label="Box Number",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )
    zipcode = forms.CharField(
        label="Zipcode",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )
    city = forms.CharField(
        label="City",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )
    country = forms.CharField(
        label="Country",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "hx-trigger": "keyup changed delay:200ms",
                "hx-post": "field-update/",
                "hx-target": "#comparison-results",
                "hx-swap": "innerHTML",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = Address()

    def update_field(self, field_name: str):
        """Update structured fields from raw text"""
        full_field_name = f"{self.prefix}-{field_name}"
        if full_field_name in self.data:
            value = self.data[full_field_name]

            self.address.update_field(field_name, value)
            self.data = self.data.copy()  # Make mutable

            if field_name == "raw_text":
                self.data[f"{self.prefix}-street_name"] = self.address.street_name
                self.data[f"{self.prefix}-street_number"] = self.address.street_number
                self.data[f"{self.prefix}-box_number"] = self.address.box_number
                self.data[f"{self.prefix}-zipcode"] = self.address.zipcode
                self.data[f"{self.prefix}-city"] = self.address.city
                self.data[f"{self.prefix}-country"] = self.address.country
            else:
                self.data[f"{self.prefix}-raw_text"] = self.address.raw_text
