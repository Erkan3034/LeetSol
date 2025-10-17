# LeetCode-GitHub-AutoSync-CLI

Tam otomatik bir CLI ve GitHub Actions iş akışı: En son kabul edilen LeetCode çözümlerinizi periyodik olarak depoya işler (commit). Proje ücretsiz araçlarla çalışır.

## Özellikler
- LeetCode GraphQL API (çerez tabanlı) ile son kabul edilen gönderileri çeker
- GitHub REST API v3 (PAT) ile `solutions/{Difficulty}/{problem-slug}.{ext}` yolunda dosya oluşturur/günceller
- Haftalık otomatik senkronizasyon (Pazar 02:00 UTC) + manuel tetikleme
- `--dry-run` ile sadece planı gösterme

## Kurulum
1. Python 3.10+ kurulu olmalı.
2. Bağımlılıklar:
```bash
pip install -r requirements.txt
```

## Gerekli Secrets / Environment
- `LC_SESSION`: LeetCode `LEETCODE_SESSION` çerezi
- `LC_CSRF`: LeetCode `csrftoken` çerezi
- `GITHUB_PAT`: GitHub Personal Access Token (repo içeriği yazma yetkili)
- `GH_OWNER`: GitHub kullanıcı/organizasyon adı
- `GH_REPO`: Depo adı

Bunları repo Secrets kısmına ekleyin. İş akışı (`.github/workflows/sync.yml`) değerleri `env` ile `sync.py`'ye aktarır.

## Yerel Çalıştırma
```bash
# PowerShell örneği
$env:LC_SESSION="<...>"
$env:LC_CSRF="<...>"
$env:GITHUB_PAT="<...>"
$env:GH_OWNER="<owner>"
$env:GH_REPO="<repo>"
python sync.py sync --limit 20 --dry-run
```
`--dry-run` olmadan çalıştırdığınızda GitHub'a yazacaktır.

## Dosya Yapısı
- `sync.py`: CLI giriş noktası; akışı yönetir
- `leetcode_api.py`: LeetCode GraphQL istemcisi
- `github_api.py`: GitHub içerik API istemcisi
- `.github/workflows/sync.yml`: Haftalık iş akışı
- `solutions/`: Senkronize edilen çözümler

## Zamanlama
- Cron: Pazar 02:00 UTC (`0 2 * * 0`)
- Manuel tetikleme: `workflow_dispatch`

## Notlar
- LeetCode oran sınırları ve oturum süresi dolması yaşanabilir; yeniden deneyin
- Dil-uzantı eşleme temel seviyededir; gerekirse `sync.py` içinde genişletin
