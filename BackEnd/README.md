# Qarabağ Tur Platforması — Backend

Fərdi tur planları, məkanlar və restoranlar üçün backend API.

## Texnologiyalar
- Node.js + Express
- PostgreSQL + Prisma ORM
- JWT (email/şifrə girişi)
- Passport.js (Google və Facebook OAuth)

## Quraşdırma

1. Asılılıqları yükləyin:
   ```
   npm install
   ```

2. `.env.example` faylını `.env` adı ilə kopyalayın və dəyərləri doldurun:
   ```
   cp .env.example .env
   ```
   - `DATABASE_URL` — öz PostgreSQL bağlantınız
   - `JWT_SECRET`, `SESSION_SECRET` — istənilən güclü təsadüfi mətn
   - Google/Facebook üçün OAuth açarları (hələlik boş qala bilər, sonra doldurarsınız)

3. Bazanı yaradın və Prisma miqrasiyasını işə salın:
   ```
   npx prisma migrate dev --name init
   ```
   Bu əmr `prisma/schema.prisma`-dakı bütün cədvəlləri (users, accounts, places, restaurants, reviews, favorites, tour_plans, tour_plan_items) real PostgreSQL bazasında yaradacaq.

4. Serveri işə salın:
   ```
   npm run dev
   ```
   API `http://localhost:5000` ünvanında işə düşəcək.

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

OAuth girişindən sonra istifadəçi `CLIENT_URL/oauth-success?token=...` ünvanına yönləndirilir — frontend bu token-i tutub localStorage-a yazmalıdır.

## Verilənlər bazası strukturu (qısa xülasə)

- **User** — istifadəçi məlumatları + `interests`, `budgetLevel`, `travelStyle` (fərdi tur tövsiyəsi üçün)
- **Account** — Google/Facebook hesablarının User-ə bağlanması
- **Category** — məkan/restoran kateqoriyaları (Tarixi abidə, Təbiət, Muzey və s.)
- **Place** — görməli yerlər (Şuşa, Ağdam, Xankəndi və s. üzrə)
- **Restaurant** — restoranlar
- **Review** — istifadəçi rəyləri (Place və ya Restaurant üçün)
- **Favorite** — seçilmişlər
- **TourPlan** / **TourPlanItem** — istifadəçinin yaratdığı gün-gün tur planı

## Növbəti addımlar (sonra əlavə edə bilərsiniz)
- `/api/places`, `/api/restaurants` — CRUD endpoint-ləri
- `/api/tour-plans` — istifadəçinin özü üçün tur planı yaratması
- Tövsiyə alqoritmi: `interests` + `budgetLevel` + `travelStyle` əsasında məkan/restoran filtri
- Admin panel üçün `requireAdmin` middleware-i istifadə edərək məkan/restoran əlavə etmə
