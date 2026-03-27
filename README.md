# Photographer Site - Django

Prosty CMS dla strony fotografa na Django z deployem przygotowanym pod Render.

## Lokalny start

```bash
python -m venv .venv
.venv\Scripts\activate
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
.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Render

Repo zawiera plik `render.yaml`, wiec mozesz zrobic deploy jako Blueprint albo recznie jako Web Service.

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Start command:

```bash
python manage.py migrate && gunicorn photographer_site.wsgi:application --bind 0.0.0.0:$PORT
```

Na Renderze ustaw:

1. `SECRET_KEY`
2. `DATABASE_URL` - opcjonalnie, jesli chcesz wyjsc poza lokalne SQLite
3. `EMAIL_HOST_USER`
4. `GMAIL_CLIENT_ID`
5. `GMAIL_CLIENT_SECRET`
6. `GMAIL_REFRESH_TOKEN`
7. `DEFAULT_FROM_EMAIL`
8. `CONTACT_EMAIL`

Opcjonalnie:

- `ALLOWED_HOSTS` - jesli dodasz wlasna domene
- `CSRF_TRUSTED_ORIGINS` - jesli dodasz wlasna domene, np. `https://twojadomena.pl`

## Static i media

- `static/` jest zrodlem assetow i podczas deployu trafia do `staticfiles/` przez `collectstatic`.
- `media/` pozostaje w repo i jest serwowane przez aplikacje Django.
- To rozwiazanie jest dobre dla gotowych, publicznych plikow dodanych do repo.
- Jesli w przyszlosci chcesz dodawac zdjecia z panelu admina juz po deployu, potrzebny bedzie zewnetrzny storage, np. S3 lub Cloudinary.
