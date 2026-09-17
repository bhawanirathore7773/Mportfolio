from django import forms

from .models import ContactInquiry, HireRequest


class HoneypotMixin(forms.Form):
    """A hidden field real visitors never fill in. Kept purely client-side
    invisible via CSS in the template — no JS required."""

    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value


class ContactForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional"}),
            "message": forms.Textarea(attrs={"placeholder": "How can I help?", "rows": 5}),
        }


class HireRequestForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = [
            "full_name", "email", "phone", "company", "project_type", "budget_range",
            "timeline", "project_details", "reference_file", "preferred_contact_method",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional"}),
            "company": forms.TextInput(attrs={"placeholder": "Optional"}),
            "budget_range": forms.TextInput(attrs={"placeholder": "e.g. ₹15,000 – ₹40,000"}),
            "timeline": forms.TextInput(attrs={"placeholder": "e.g. Within 3 weeks"}),
            "project_details": forms.Textarea(
                attrs={"placeholder": "Tell me about the collection, references and requirements.", "rows": 6}
            ),
        }
