# Connectly — CodeAlpha Task 2

Django social media platform with authentication, profiles, multiple post types, comments, likes, follows, bookmarks, and Community Challenges as the unique feature.

## Stack
Python · Django 5.2.17 · SQLite · HTML · CSS · JavaScript · Pillow

## Windows setup
```powershell
cd C:\Users\HAI\OneDrive\Desktop\CodeAlpha_SocialMedia
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Features
- Login/Register/Logout + show/hide password
- Profiles
- Text/Image/Video/Link/Poll/Location/Event posts
- Comments
- Like/Unlike
- Follow/Unfollow
- Bookmarks
- Community Challenges: join, participants, challenge posts, completion

The Google button in the login design is a visual placeholder; real OAuth is intentionally outside the selected scope.
