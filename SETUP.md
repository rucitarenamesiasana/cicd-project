# Panduan Setup Repository dan cPanel Deployment

## 1. Buat Repository GitHub

1. Buka GitHub.
2. Klik `New repository`.
3. Nama repository contoh: `cpanel-cicd-project`.
4. Pilih Public atau Private.
5. Klik `Create repository`.

## 2. Upload Project

Upload semua isi folder project ini ke repository GitHub.
Pastikan struktur folder tetap seperti ini:

```text
public/index.html
.github/workflows/deploy.yml
README.md
.gitignore
SETUP.md
```

## 3. Tambahkan GitHub Secrets

Masuk ke:

```text
Repository > Settings > Secrets and variables > Actions > New repository secret
```

Tambahkan:

```text
FTP_SERVER
FTP_USERNAME
FTP_PASSWORD
```

Catatan penting: jangan pernah menulis password langsung di file project.

## 4. Jalankan Workflow

Workflow berjalan otomatis saat ada push ke branch `main`.
Bisa juga dijalankan manual dari tab:

```text
Actions > Deploy to cPanel via FTP > Run workflow
```

## 5. Cek Website

Setelah workflow sukses, buka domain hosting.
Contoh:

```text
https://melioracognitio.com/
```

## 6. Yang Dikumpulkan

Kumpulkan salah satu:

```text
Link repository GitHub
```

atau

```text
Link website yang sudah terdeploy
```
