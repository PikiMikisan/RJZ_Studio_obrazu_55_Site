import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm
from .models import AboutMe, PortfolioCategory, PortfolioPhoto, SiteInfo

logger = logging.getLogger(__name__)


def get_site_info():
    return SiteInfo.objects.first()


def informacje(request):
    site_info = get_site_info()
    featured_photos = PortfolioPhoto.objects.filter(is_featured=True)[:6]
    return render(
        request,
        "portfolio/informacje.html",
        {
            "site_info": site_info,
            "featured_photos": featured_photos,
            "active": "informacje",
        },
    )


def o_mnie(request):
    about = AboutMe.objects.first()
    site_info = get_site_info()
    return render(
        request,
        "portfolio/o_mnie.html",
        {
            "about": about,
            "site_info": site_info,
            "active": "o_mnie",
        },
    )


def portfolio_view(request, slug=None):
    site_info = get_site_info()
    categories = PortfolioCategory.objects.all()
    active_category = None

    if slug:
        active_category = get_object_or_404(PortfolioCategory, slug=slug)
        photos = PortfolioPhoto.objects.filter(category=active_category)
    else:
        photos = PortfolioPhoto.objects.all()

    return render(
        request,
        "portfolio/portfolio.html",
        {
            "photos": photos,
            "categories": categories,
            "active_category": active_category,
            "site_info": site_info,
            "active": "portfolio",
        },
    )


def send_contact_notification(request, contact_message, site_info):
    site_name = site_info.title if site_info and site_info.title else "Fotograf"
    site_tagline = site_info.tagline if site_info and site_info.tagline else ""
    home_url = request.build_absolute_uri("/")

    context = {
        "contact_message": contact_message,
        "site_name": site_name,
        "site_tagline": site_tagline,
        "home_url": home_url,
    }

    text_body = render_to_string("portfolio/emails/contact_notification.txt", context)
    html_body = render_to_string("portfolio/emails/contact_notification.html", context)

    try:
        email = EmailMultiAlternatives(
            subject=f"[{site_name}] Nowa wiadomosc: {contact_message.subject}",
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[contact_message.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Contact email could not be sent.")
        return False


def kontakt(request):
    site_info = get_site_info()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            email_sent = send_contact_notification(request, contact_message, site_info)
            if email_sent:
                messages.success(request, "Wiadomosc zostala wyslana. Odpowiem wkrotce.")
            else:
                messages.warning(
                    request,
                    "Nie udalo sie wyslac maila. Twoja wiadomosc zostala zapisana, "
                    "sprobuj ponownie za chwile.",
                )
            return redirect("kontakt")

        messages.error(request, "Popraw bledy w formularzu.")

    return render(
        request,
        "portfolio/kontakt.html",
        {
            "form": form,
            "site_info": site_info,
            "active": "kontakt",
        },
    )
