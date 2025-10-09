# academiaKit — Backend API (Django + DRF)

API backend para gestión académica. Construido con **Django** y **Django REST Framework**, autenticación **JWT (SimpleJWT)** y documentación **Swagger** con **drf-spectacular**.

---

## ✨ Características
- **User model personalizado** (basado en `AbstractUser`) con roles (`student/teacher/admin`).
- **CRUD de usuarios** mediante `ModelViewSet` y permisos “Admin o Yo mismo”.
- **Autenticación JWT** (obtener/refresh/verify tokens) con `djangorestframework-simplejwt`.
- **Documentación Swagger** pública en `/api/docs/` (OpenAPI con drf-spectacular).
- **Arquitectura 100% API** (sin templates), ideal para frontends React/Vue/Next o apps móviles.

> En la fase final se conectará a **MySQL** (por ahora el proyecto usa SQLite para desarrollo).

---

## 🧱 Stack
- Python 3.11+
- Django 5+
- Django REST Framework (DRF)
- SimpleJWT
- drf-spectacular (Swagger UI)

---

## 📁 Estructura (simplificada)
```
academiaKit/
├─ academiaKit/              # settings/urls/wsgi/asgi
├─ accounts/                 # app de usuarios
│  ├─ models.py
│  ├─ serializers.py         # UserSerializer (CRUD seguro)
│  ├─ views.py               # UserViewSet + /me
│  └─ admin.py               # registro en admin
├─ orgs/ academics/ ...      # apps de negocio (por construir)
├─ db.sqlite3                # base de datos dev
├─ manage.py
└─ requirements.txt
