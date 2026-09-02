# Elevate Services Phase 1

Django + DRF backend for Customer App + Admin App.

## Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## APIs
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/token/refresh/
GET  /api/v1/auth/me/
POST /api/v1/auth/social/google/  {id_token}
POST /api/v1/auth/social/apple/   {identity_token,email?}
POST /api/v1/auth/social/facebook/ {access_token}
GET/POST/PATCH/DELETE /api/v1/services/
GET/POST/PATCH/DELETE /api/v1/packages/
GET/POST/PATCH /api/v1/orders/

Admin status flow: PENDING -> ACCEPTED -> IN_PROGRESS -> COMPLETED.
