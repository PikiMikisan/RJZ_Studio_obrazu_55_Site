# Photographer Site - Django

Prosty CMS dla strony fotografa na Django.

## Lokalny start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Zmienne srodowiskowe

Przykladowe wartosci sa w pliku `.env.example`.

Najwazniejsze zmienne:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `EMAIL_HOST_USER`
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_EMAIL`

## Gmail / Google SMTP

Projekt jest ustawiony pod Gmail SMTP z OAuth2:

- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`

Ustaw:

- `EMAIL_HOST_USER`
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_EMAIL`

Checklist:

1. Utworz OAuth client w Google Cloud.
2. Wygeneruj refresh token dla konta Gmail, z ktorego maja wychodzic maile.
3. Ustaw `EMAIL_HOST_USER`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `DEFAULT_FROM_EMAIL` i `CONTACT_EMAIL`.

## Secret key

Przy `DEBUG=False` aplikacja nie wystartuje bez `SECRET_KEY`.

Mozesz wygenerowac nowy klucz poleceniem:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Ubuntu

Przykladowy start na czystym serwerze:

```bash
sudo apt update
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn photographer_site.wsgi:application --bind 127.0.0.1:8000
```

Na produkcji ustaw w srodowisku:

1. `SECRET_KEY`
2. `DEBUG=False`
3. `ALLOWED_HOSTS`
4. `CSRF_TRUSTED_ORIGINS`
5. `DATABASE_URL` - opcjonalnie, jesli chcesz wyjsc poza SQLite
6. `EMAIL_HOST_USER`
7. `GMAIL_CLIENT_ID`
8. `GMAIL_CLIENT_SECRET`
9. `GMAIL_REFRESH_TOKEN`
10. `DEFAULT_FROM_EMAIL`
11. `CONTACT_EMAIL`

Opcjonalnie:

- `SECURE_SSL_REDIRECT=False` - jesli SSL konczy sie poza aplikacja i proxy nie przekazuje `X-Forwarded-Proto`.

## Systemd

Przykladowa komenda dla uslugi:

```bash
/sciezka/do/projektu/.venv/bin/gunicorn photographer_site.wsgi:application --chdir /sciezka/do/projektu --bind 127.0.0.1:8000
```

## Static i media

- `static/` jest zrodlem assetow i podczas deployu trafia do `staticfiles/` przez `collectstatic`.
- `media/` pozostaje w repo i jest serwowane przez aplikacje Django.
- To rozwiazanie jest dobre dla gotowych, publicznych plikow dodanych do repo.
- Jesli w przyszlosci chcesz dodawac zdjecia z panelu admina juz po deployu, potrzebny bedzie zewnetrzny storage, np. S3 lub Cloudinary.
