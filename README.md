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

## Zmienne środowiskowe

Przykładowe wartości są w pliku `.env.example`.

Najważniejsze zmienne:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_EMAIL`

## Gmail / Google SMTP

Projekt jest ustawiony pod Gmail SMTP:

- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`

Do `EMAIL_HOST_PASSWORD` wstaw 16-znakowe App Password z konta Google, nie zwykłe hasło.

Checklist:

1. Włącz 2-Step Verification na koncie Google.
2. Wygeneruj App Password dla aplikacji pocztowej.
3. Ustaw `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` i `CONTACT_EMAIL`.

## Render

Repo zawiera plik `render.yaml`, więc możesz zrobić deploy jako Blueprint albo ręcznie jako Web Service.

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
2. `DATABASE_URL` - najlepiej z Render Postgres
3. `EMAIL_HOST_USER`
4. `EMAIL_HOST_PASSWORD`
5. `DEFAULT_FROM_EMAIL`
6. `CONTACT_EMAIL`

Opcjonalnie:

- `ALLOWED_HOSTS` - jeśli dodasz własną domenę
- `CSRF_TRUSTED_ORIGINS` - jeśli dodasz własną domenę, np. `https://twojadomena.pl`

## Static i media

- `static/` jest źródłem assetów i podczas deployu trafia do `staticfiles/` przez `collectstatic`.
- `media/` pozostaje w repo i jest serwowane przez aplikację Django.
- To rozwiązanie jest dobre dla gotowych, publicznych plików dodanych do repo.
- Jeśli w przyszłości chcesz dodawać zdjęcia z panelu admina już po deployu, potrzebny będzie zewnętrzny storage, np. S3 lub Cloudinary.
