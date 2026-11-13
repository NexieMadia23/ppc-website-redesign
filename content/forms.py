"""Public-facing forms.

Kept small and explicit so the prototype's validation rules are easy to audit:
residents can stay anonymous, but a named complaint needs at least one way to
reach them, and consent is always required.
"""

from django import forms

from .constants import BARANGAY_CHOICES
from .models import (
    ATTACHMENT_EXTENSIONS,
    ATTACHMENT_MAX_BYTES,
    Complaint,
    ContactMessage,
)

MAX_ATTACHMENTS = 3


class MultipleFileInput(forms.FileInput):
    """Django's FileInput refuses ``multiple`` unless this flag is set."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """A FileField that accepts and validates a list of uploads."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        clean_one = super().clean
        if isinstance(data, (list, tuple)):
            return [clean_one(item, initial) for item in data]
        return clean_one(data, initial)


class ComplaintForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        label="Photos",
        help_text="Up to 3 photos, 5 MB each. JPG, PNG, or WebP. Location data is removed automatically.",
        widget=MultipleFileInput(
            attrs={
                "accept": "image/jpeg,image/png,image/webp",
                "data-max-files": MAX_ATTACHMENTS,
            }
        ),
    )
    # Honeypot: hidden from people, irresistible to bots. It must stay empty.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "class": "hp-field",
            }
        ),
    )

    class Meta:
        model = Complaint
        fields = [
            "category",
            "subject",
            "barangay",
            "landmark",
            "details",
            "name",
            "email",
            "phone",
            "is_anonymous",
            "consent",
        ]
        labels = {
            "category": "What is this about?",
            "subject": "Short title",
            "barangay": "Barangay",
            "landmark": "Landmark or street (optional)",
            "details": "What happened?",
            "name": "Your name",
            "email": "Email",
            "phone": "Mobile number",
            "is_anonymous": "Submit anonymously",
            "consent": "I agree to the privacy notice",
        }
        help_texts = {
            "subject": "One line, for example “Broken street light on Rizal Avenue”.",
            "barangay": "Where the concern happened, so the right team can respond.",
            "landmark": "For example “near Barangay Hall” or “corner Valencia Street”.",
            "details": "Include the date and time when you can. Do not include ID numbers or other sensitive personal data.",
            "email": "Optional if you give a mobile number.",
            "phone": "Optional if you give an email address.",
        }
        widgets = {
            "details": forms.Textarea(attrs={"rows": 6}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"}),
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "subject": forms.TextInput(attrs={"maxlength": 200}),
            "landmark": forms.TextInput(attrs={"maxlength": 200}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The model keeps barangay blank for old rows; every new request needs it.
        self.fields["barangay"].required = True
        self.fields["barangay"].choices = [("", "Choose a barangay")] + list(BARANGAY_CHOICES)

    def clean(self):
        cleaned = super().clean()
        anonymous = cleaned.get("is_anonymous")
        name = (cleaned.get("name") or "").strip()
        email = (cleaned.get("email") or "").strip()
        phone = (cleaned.get("phone") or "").strip()
        files = self.files.getlist("attachments")

        if cleaned.get("website"):
            self.add_error(None, "Something went wrong. Please try again.")

        if len(files) > MAX_ATTACHMENTS:
            self.add_error("attachments", f"Attach up to {MAX_ATTACHMENTS} photos.")
        for upload in files[:MAX_ATTACHMENTS]:
            suffix = "." + upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else ""
            if suffix not in ATTACHMENT_EXTENSIONS:
                self.add_error("attachments", "Upload JPG, PNG, or WebP photos only.")
                break
            if upload.size > ATTACHMENT_MAX_BYTES:
                self.add_error("attachments", "Each photo must be 5 MB or smaller.")
                break

        if not anonymous:
            if not name:
                self.add_error("name", "Add your name, or choose to submit anonymously.")
            if not email and not phone:
                self.add_error(
                    "email",
                    "Add an email or mobile number so we can update you, or submit anonymously.",
                )
        if not cleaned.get("consent"):
            self.add_error("consent", "Please agree to the privacy notice before submitting.")

        cleaned["name"] = name
        cleaned["email"] = email
        cleaned["phone"] = phone
        return cleaned


class ContactForm(forms.ModelForm):
    """Public contact form; stores messages for staff follow-up."""

    topic = forms.ChoiceField(required=False)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "topic", "message", "consent"]
        labels = {
            "name": "Full name",
            "email": "Email address",
            "phone": "Phone number (optional)",
            "topic": "What is this about?",
            "message": "Message",
            "consent": "I agree that the city may use my details to respond to this message",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        topics = kwargs.pop("topics", None) or []
        super().__init__(*args, **kwargs)
        self.fields["topic"].choices = [(topic, topic) for topic in topics]

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise forms.ValidationError("Please agree to the privacy notice before sending.")
        return consent
