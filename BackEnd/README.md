# Qarabağ Tur Platforması — Backend (Python / FastAPI)

Bu, əvvəlki Node.js versiyasının **eyni verilənlər bazası strukturuna sahib** Python versiyasıdır.

## Texnologiyalar
- FastAPI (web framework)
- SQLAlchemy 2.0 (ORM)
- PostgreSQL
- Alembic (miqrasiyalar)
- JWT — `python-jose` (email/şifrə girişi)
- Authlib — Google və Facebook OAuth
- Passlib + bcrypt — şifrə hashləmə

## Quraşdırma

1. Virtual mühit yaradın və aktivləşdirin:
   ```
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Asılılıqları yükləyin:
   ```
   pip install -r requirements.txt
   ```

3. `.env.example` faylını `.env` adı ilə kopyalayın və dəyərləri doldurun:
   ```
   cp .env.example .env
   ```

4. Alembic ilə ilk miqrasiyanı yaradın və işə salın:
   ```
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```
   Bu, `app/db/models.py`-dakı bütün cədvəlləri (users, accounts, categories, places, restaurants, reviews, favorites, tour_plans, tour_plan_items) real PostgreSQL bazanızda yaradacaq.

5. Serveri işə salın:
   ```
   uvicorn app.main:app --reload --port 8000
   ```
   API `http://localhost:8000` ünvanında işə düşəcək.
   İnteraktiv Swagger sənədləri: `http://localhost:8000/docs`

## Hazır endpoint-lər

| Metod | Endpoint                     | Açıqlama                          |
|-------|-------------------------------|-----------------------------------|
| POST  | /api/auth/signup              | Email+şifrə ilə qeydiyyat         |
| POST  | /api/auth/login               | Email+şifrə ilə giriş             |
| GET   | /api/auth/me                  | Cari istifadəçi (token tələb edir)|
| GET   | /api/auth/google              | Google girişini başladır          |
| GET   | /api/auth/google/callback     | Google-dan geri dönüş             |
| GET   | /api/auth/facebook            | Facebook girişini başladır        |
| GET   | /api/auth/facebook/callback   | Facebook-dan geri dönüş           |

`/docs` səhifəsindən bütün endpoint-ləri birbaşa brauzerdə sınaya bilərsiniz (Postman-a ehtiyac olmadan).

## Verilənlər bazası strukturu

Eyni struktur, Node.js versiyası ilə tam üst-üstə düşür:

- **User** — istifadəçi + `interests`, `budget_level`, `travel_style` (fərdi tövsiyə üçün)
- **Account** — Google/Facebook hesablarının User-ə bağlanması
- **Category** — kateqoriyalar
- **Place** — görməli yerlər
- **Restaurant** — restoranlar
- **Review** — rəylər
- **Favorite** — seçilmişlər
- **TourPlan** / **TourPlanItem** — istifadəçinin tur planı

## Növbəti addımlar
- `/api/places`, `/api/restaurants` üçün CRUD router-ləri
- `/api/tour-plans` — istifadəçinin öz tur planını yaratması
- Tövsiyə alqoritmi: `interests` + `budget_level` + `travel_style` əsasında filtr
- `require_admin` dependency-si ilə admin-only endpoint-lər
