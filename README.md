Web site for movie reviews

Návod na inštaláciu:
1. Potrebujete mať nainštalovaný Python na svojom zariadení (verzia 3.x)
2. Nakopírujte si tento repozitár z GitHub-u
3. Je odporúčané používať virtual environment na izolovanie závislosti, ak ho nemáte nainštalovaný, tak do konzoly:
  python -m venv env
  env\Scripts\activate //pre Windows
  source env/bin/activate //pre Linux alebo macOS
4. Potrebujete nainštalovať potrebné závislosti:
  Django==5.1.3
  pillow==11.1.0
  requests==2.32.3
  pip install Django==5.1.3 pillow==11.1.0 requests==2.32.3
  (ak napíšete do konzoly "pip freeze", tak sa Vám zobrazia nainštalované balíčky)
5. Nastavte databázu:
  python manage.py migrate
6. Spustite aplikáciu lokálne:
  python manage.py runserver
7. Otvoríte webový prehliadač a prejdite na adresu http://127.0.0.1:8000/ kde sa Vám táto webová aplikácia zobrazí
