from django.db import models


class SiteInfo(models.Model):
    """Informacje ogólne o stronie / fotografie - sekcja 'Informacje'"""
    title = models.CharField("Tytuł strony", max_length=200, default="Fotograf")
    logo = models.ImageField("Logo (w nawigacji)", upload_to='logo/', blank=True, null=True,
                             help_text="Zalecana wysokość: 40–50px. Jeśli nie wgrasz logo, wyświetli się tekst.")
    tagline = models.CharField("Podtytuł / hasło", max_length=300, blank=True)
    hero_image = models.ImageField("Zdjęcie główne (hero)", upload_to='hero/', blank=True, null=True)
    info_content = models.TextField("Treść sekcji Informacje")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informacje o stronie"
        verbose_name_plural = "Informacje o stronie"

    def __str__(self):
        return self.title


class AboutMe(models.Model):
    """Sekcja 'O mnie'"""
    photo = models.ImageField("Zdjęcie profilowe", upload_to='about/', blank=True, null=True)
    content = models.TextField("Treść sekcji O mnie")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O mnie"
        verbose_name_plural = "O mnie"

    def __str__(self):
        return "O mnie"


class PortfolioCategory(models.Model):
    """Kategoria portfolio (np. Śluby, Portrety, Krajobrazy)"""
    name = models.CharField("Nazwa kategorii", max_length=100)
    slug = models.SlugField("Slug URL", unique=True)
    order = models.PositiveIntegerField("Kolejność", default=0)

    class Meta:
        verbose_name = "Kategoria portfolio"
        verbose_name_plural = "Kategorie portfolio"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class PortfolioPhoto(models.Model):
    """Zdjęcie w portfolio"""
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='photos',
        verbose_name="Kategoria"
    )
    title = models.CharField("Tytuł", max_length=200, blank=True)
    description = models.TextField("Opis", blank=True)
    image = models.ImageField("Zdjęcie", upload_to='portfolio/')
    order = models.PositiveIntegerField("Kolejność", default=0)
    is_featured = models.BooleanField("Wyróżnione (na stronie głównej)", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zdjęcie portfolio"
        verbose_name_plural = "Zdjęcia portfolio"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f"Zdjęcie #{self.pk}"


class ContactMessage(models.Model):
    """Wiadomości z formularza kontaktowego"""
    name = models.CharField("Imię i nazwisko", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Telefon", max_length=30, blank=True)
    subject = models.CharField("Temat", max_length=300)
    message = models.TextField("Wiadomość")
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField("Przeczytano", default=False)

    class Meta:
        verbose_name = "Wiadomość kontaktowa"
        verbose_name_plural = "Wiadomości kontaktowe"
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.name} – {self.subject} ({self.sent_at.strftime('%d.%m.%Y')})"
