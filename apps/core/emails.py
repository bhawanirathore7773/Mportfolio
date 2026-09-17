from django.conf import settings
from django.core.mail import send_mail


def send_contact_notifications(inquiry):
    """Confirmation to the visitor + notification to the admin inbox.
    Silently no-ops if EMAIL_HOST_USER / ADMIN_NOTIFICATION_EMAIL aren't
    configured yet (e.g. during local development) so the form still works.
    """
    if settings.ADMIN_NOTIFICATION_EMAIL:
        send_mail(
            subject=f"New contact message from {inquiry.name}",
            message=(
                f"Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\n\n"
                f"{inquiry.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    send_mail(
        subject="Thanks for reaching out",
        message=(
            f"Hi {inquiry.name},\n\nThank you for reaching out. Your message has been received "
            "and I'll get back to you shortly.\n\nBest,\nManish"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[inquiry.email],
        fail_silently=True,
    )


def send_hire_notifications(hire_request):
    if settings.ADMIN_NOTIFICATION_EMAIL:
        send_mail(
            subject=f"New project enquiry — {hire_request.get_project_type_display()}",
            message=(
                f"Name: {hire_request.full_name}\nEmail: {hire_request.email}\n"
                f"Phone: {hire_request.phone}\nCompany: {hire_request.company}\n"
                f"Project type: {hire_request.get_project_type_display()}\n"
                f"Budget: {hire_request.budget_range}\nTimeline: {hire_request.timeline}\n\n"
                f"{hire_request.project_details}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    send_mail(
        subject="Thank you for reaching out",
        message=(
            f"Hi {hire_request.full_name},\n\nThank you for reaching out. Your project enquiry has "
            "been received successfully and I'll be in touch soon to discuss next steps.\n\n"
            "Best,\nManish"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[hire_request.email],
        fail_silently=True,
    )
