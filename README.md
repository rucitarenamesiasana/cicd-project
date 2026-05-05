# Final Project Software Testing - Task Management API

![CI](https://github.com/rucitarenamesiasana/cicd-project/actions/workflows/ci.yml/badge.svg)

## Deskripsi Aplikasi

Project ini adalah aplikasi **Task Management API** sederhana yang dibuat untuk Final Project mata kuliah Software Testing. Aplikasi menyediakan fitur untuk membuat, melihat, mengubah status, menghapus, dan melihat statistik task.

Aplikasi dibuat agar mudah diuji dan memiliki automated testing yang berjalan otomatis menggunakan GitHub Actions sebagai Continuous Integration (CI).

## Fitur Utama

1. Membuat task baru dengan validasi input.
2. Melihat daftar task dan detail task.
3. Mengubah status task dan menghapus task.
4. Melihat statistik task berdasarkan status dan prioritas.

## Teknologi

- Python
- Flask
- Pytest
- Pytest Coverage
- GitHub Actions
- JSON file storage

## Struktur Repository

```text
.
├── .github/workflows/ci.yml
├── data/
├── public/
├── src/
│   ├── app.py
│   ├── storage.py
│   └── task_service.py
├── tests/
│   ├── test_app_integration.py
│   └── test_task_service_unit.py
├── README.md
├── LAPORAN.md
└── requirements.txt
```

## Cara Menjalankan Aplikasi

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:

```bash
python -m src.app
```

3. Buka endpoint:

```text
http://localhost:5000/health
http://localhost:5000/tasks
http://localhost:5000/stats
```

## Contoh Endpoint

### Create Task

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Belajar testing","description":"Mengerjakan final project","priority":"high"}'
```

### Update Status

```bash
curl -X PATCH http://localhost:5000/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

## Cara Menjalankan Test

```bash
pytest
```

## Cara Menjalankan Test Coverage

```bash
pytest --cov=src --cov-report=term-missing --cov-report=xml
```

Target minimal coverage pada tugas adalah **60%**. Project ini disiapkan agar coverage berada di atas target minimal.

## Strategi Pengujian

### Unit Testing

Unit test berfokus pada logika bisnis pada `TaskService`, seperti:

- validasi title
- validasi priority
- validasi status
- pembuatan task
- update status
- delete task
- statistik task

Jumlah unit test: **23 test case**.

### Integration Testing

Integration test berfokus pada endpoint API Flask, seperti:

- health check
- create task
- validasi input API
- get task
- update status
- delete task
- statistik task

Jumlah integration test: **7 test case**.

## Continuous Integration

Workflow GitHub Actions berada pada:

```text
.github/workflows/ci.yml
```

Workflow berjalan otomatis saat:

- push ke branch `main`
- pull request ke branch `main`

Pipeline melakukan:

1. Checkout repository
2. Setup Python
3. Install dependencies
4. Build / syntax check
5. Run test dengan coverage
6. Upload coverage report sebagai artifact

## Link Repository

```text
https://github.com/rucitarenamesiasana/cicd-project
```
