# Clinic Appointments

Фрагмент медицинской информационной системы: выбор врача, просмотр слотов на дату и бронирование приема пациентом.

## Стек

- Backend: Django 5, Django REST Framework, PostgreSQL
- Frontend: Next.js, TypeScript, TanStack Query
- Инфраструктура: Docker Compose

## Запуск

```bash
docker compose up --build
```

После старта:

- Frontend: http://localhost:3000
- API: http://localhost:8000/api
- PostgreSQL: localhost:5432

Если стандартные порты заняты, их можно переопределить:

```powershell
$env:BACKEND_HOST_PORT="8001"; $env:FRONTEND_HOST_PORT="3001"; $env:POSTGRES_HOST_PORT="5434"; docker compose up --build
```

```bash
BACKEND_HOST_PORT=8001 FRONTEND_HOST_PORT=3001 POSTGRES_HOST_PORT=5434 docker compose up --build
```

Команда запуска backend выполняет миграции и заполняет демо-данные. Доступны две клиники:

- `Clinic-Id: 1` — Central Clinic
- `Clinic-Id: 2` — North Clinic

## API

Все запросы к `/api/*` требуют заголовок `Clinic-Id`.

```bash
curl -H "Clinic-Id: 1" http://localhost:8000/api/doctors/
```

```bash
curl -H "Clinic-Id: 1" "http://localhost:8000/api/doctors/1/slots/?date=YYYY-MM-DD"
```

Для демо-данных подходит любая дата от текущего дня до шести дней вперед.

```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -H "Clinic-Id: 1" \
  -d '{"slot_id":1,"patient_name":"Ivan Petrov","patient_phone":"+77001234567"}'
```

## Тесты

```bash
docker compose run --rm backend python manage.py test
```

Тесты покрывают бронирование свободного слота, повторное бронирование, недоступность слота другой клиники и конкурентное бронирование одного слота.

## Конкурентное бронирование

Бронирование выполняется в `transaction.atomic()`. Слот выбирается через `select_for_update()`, поэтому PostgreSQL ставит row-level lock на строку слота до завершения транзакции. Если два запроса одновременно бронируют один слот, первый запрос меняет статус на `booked` и создает запись, а второй продолжает выполнение только после коммита первого и видит уже занятый слот.

Дополнительно запись связана со слотом через `OneToOneField`, поэтому на уровне базы данных один слот не может получить две записи даже при ошибке в прикладной логике.

## Изоляция клиник

Middleware извлекает `Clinic-Id` из каждого API-запроса и кладет найденную клинику в `request.clinic`. Все выборки врачей, слотов и создание записей фильтруются по этой клинике.

Слот хранит `clinic_id` отдельно от врача. Это намеренная денормализация для простых и быстрых фильтров изоляции: API не возвращает и не бронирует слот, если его `clinic_id` не совпадает с клиникой из заголовка.

## Структура

```text
backend/
  config/
  scheduling/
frontend/
  app/
docker-compose.yml
```

Незавершенных частей нет.
