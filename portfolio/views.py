import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import DatabaseError
from django.db.utils import OperationalError, ProgrammingError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm
from .models import AboutMe, PortfolioCategory, PortfolioPhoto, SiteInfo

logger = logging.getLogger(__name__)
DB_EXCEPTIONS = (DatabaseError, OperationalError, ProgrammingError)


def safe_db_call(callback, default, label):
    try:
        return callback()
    except DB_EXCEPTIONS:
        logger.exception("%s failed.", label)
        return default


def get_site_info():
    return safe_db_call(lambda: SiteInfo.objects.first(), None, "Loading site info")


def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")


def informacje(request):
    site_info = get_site_info()
    featured_photos = safe_db_call(
        lambda: list(PortfolioPhoto.objects.filter(is_featured=True)[:6]),
        [],
        "Loading featured photos",
    )
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
    about = safe_db_call(lambda: AboutMe.objects.first(), None, "Loading about section")
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
    categories = safe_db_call(
        lambda: list(PortfolioCategory.objects.all()),
        [],
        "Loading portfolio categories",
    )
    active_category = None

    if slug:
        try:
            active_category = get_object_or_404(PortfolioCategory, slug=slug)
            photos = list(PortfolioPhoto.objects.filter(category=active_category))
        except DB_EXCEPTIONS:
            logger.exception("Loading portfolio category failed.")
            active_category = None
            photos = []
    else:
        photos = safe_db_call(
            lambda: list(PortfolioPhoto.objects.all()),
            [],
            "Loading portfolio photos",
        )

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
