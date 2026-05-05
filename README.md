# CI/CD Deployment Project to cPanel

Project ini dibuat untuk memenuhi tugas Continuous Deployment.

## Deskripsi

Website statis sederhana ini dideploy otomatis ke cPanel menggunakan GitHub Actions.
Setiap perubahan yang di-push ke branch `main` akan menjalankan workflow deployment.

## Teknologi

- HTML, CSS
- GitHub Actions
- FTP Deployment
- cPanel Hosting

## Struktur Project

```text
.
├── public/
│   └── index.html
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .gitignore
└── README.md
```

## Continuous Deployment Flow

1. Developer melakukan push ke branch `main`.
2. GitHub Actions menjalankan workflow `Deploy to cPanel via FTP`.
3. Repository di-checkout.
4. Folder `public/` diupload ke folder `/public_html/` pada cPanel melalui FTP.
5. Website dapat diakses melalui domain hosting.

## GitHub Secrets yang Dibutuhkan

Tambahkan secrets berikut di GitHub:

| Secret Name | Keterangan |
|---|---|
| `FTP_SERVER` | Host FTP/cPanel, contoh: `melioracognitio.com` |
| `FTP_USERNAME` | Username FTP/cPanel |
| `FTP_PASSWORD` | Password FTP/cPanel |

Path GitHub:

```text
Repository Settings > Secrets and variables > Actions > New repository secret
```

## Cara Menjalankan Deployment

1. Upload project ini ke repository GitHub.
2. Pastikan branch utama bernama `main`.
3. Tambahkan GitHub Secrets.
4. Push perubahan ke branch `main`.
5. Buka tab `Actions` untuk melihat proses deployment.

## Output yang Dikumpulkan

Yang dikumpulkan adalah salah satu dari berikut:

- Link repository GitHub
- Link website yang sudah terdeploy

Contoh:

```text
https://github.com/username/cpanel-cicd-project
https://melioracognitio.com/
```
