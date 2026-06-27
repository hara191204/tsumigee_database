# tsumigee_database

自分が所持しているゲームソフトをデータベースで管理する Web アプリ。

## 機能

- ゲームの登録・編集・削除
- クリア状況（クリア / 積み / 収集のみ）・評価・クリア日の管理
- クリア状況変更時のクリア日自動入力（JS + サーバー側バリデーション）
- メーカー・ハードのマスタ管理
- フィルター（メーカー、ハード、クリア状況、評価、パッケージ所有、美少女ゲーム）と並び替え
- 積み率・クリア数のドーナツグラフ表示
- 全モデルへの変更履歴の記録
- ログイン認証（全ページ LoginRequired）

## 技術スタック

| カテゴリ | 技術 |
| --- | --- |
| サーバー | Raspberry Pi 5 |
| コンテナ | Docker / Docker Compose |
| バックエンド | Django 6.0.6 (Python 3.12) |
| データベース | MySQL 8.4 |
| Web サーバー | Nginx (リバースプロキシ / 静的ファイル配信) + Gunicorn (WSGI) |
| フロントエンド | Bootstrap 5.3.3 / FontAwesome 6.7.2 / Chart.js 4.4.7 |
| リンター / フォーマッター | Ruff / djLint |
| git hook 管理 | pre-commit |
| コミットルール | Conventional Commits + Commitlint |
| 開発フロー | GitHub Flow |

## ディレクトリ構成

```text
tsumigee_database/
├── app/                              # Django プロジェクト
│   ├── manage.py
│   ├── templates/                    # HTML テンプレート
│   │   ├── base.html
│   │   ├── registration/
│   │   │   └── login.html
│   │   └── tsumigee_database/
│   ├── tsumigee_database/            # メインアプリ
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── tsumigee_project/             # Django 設定
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── nginx/
│   └── nginx.conf                    # Nginx 設定（本番用）
├── Dockerfile
├── entrypoint.sh                     # 起動前に collectstatic を実行
├── docker-compose.yml                # 開発用
├── docker-compose.prod.yml           # 本番用（Nginx + Gunicorn）
├── requirements.txt
├── .env.example                      # 環境変数テンプレート
├── .pre-commit-config.yaml           # pre-commit フック設定
├── commitlint.config.js              # コミットメッセージルール
└── package.json                      # Node.js 依存パッケージ（commitlint 用）
```

## 開発環境のセットアップ

### 前提条件

- Docker / Docker Compose がインストール済みであること
- Node.js がインストール済みであること
- Python 3 がインストール済みであること
- `docker` グループにユーザーが追加済みであること

### 手順

#### 1. リポジトリをクローン

```bash
git clone https://github.com/hara191204/tsumigee_database.git
cd tsumigee_database
```

#### 2. 環境変数ファイルを作成

```bash
cp .env.example .env
```

`.env` を開き各変数に値を設定する。`DJANGO_SECRET_KEY` は以下で生成できる：

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

#### 3. venv を作成して pre-commit をインストール

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pre-commit
```

#### 4. git hooks を登録

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

#### 5. commitlint をインストール

```bash
npm install
```

#### 6. Docker イメージをビルドして起動（開発）

```bash
docker compose up
```

ブラウザで `http://localhost:8000` にアクセスして確認。

#### 7. スーパーユーザーを作成

```bash
docker compose exec web python manage.py createsuperuser
```

## 本番環境での起動

### 1. `.env` を本番用に更新

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,<サーバーのLAN IPアドレス>
```

### 2. 起動

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

ブラウザで `http://<サーバーのIPアドレス>` にアクセス（ポート 80）。

### 3. 自動起動の設定

```bash
sudo systemctl enable docker
```

Docker が自動起動し、`restart: unless-stopped` により各コンテナが自動で立ち上がる。

## よく使うコマンド

```bash
# コンテナ起動（開発）
docker compose up

# マイグレーション作成・適用
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Django シェル
docker compose exec web python manage.py shell

# システムチェック
docker compose exec web python manage.py check
```

## コミットルール

[Conventional Commits](https://www.conventionalcommits.org/) に従う。コミットメッセージは英語で記述する。

```text
<type>: <subject>
```

| type | 用途 |
| --- | --- |
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `chore` | ビルド・ツール設定など |
| `docs` | ドキュメント変更 |
| `refactor` | リファクタリング |
| `test` | テスト追加・修正 |
| `style` | コードスタイル修正（動作に影響なし） |
| `perf` | パフォーマンス改善 |

コミット時に pre-commit が ruff・djlint（コード品質）と commitlint（メッセージ形式）を自動で検証する。

## 開発フロー

[GitHub Flow](https://docs.github.com/ja/get-started/using-github/github-flow) に従う。

1. `main` から feature ブランチを作成

   ```bash
   git checkout -b feat/xxx
   ```

2. 変更をコミット（Conventional Commits 形式）
3. GitHub にプッシュして Pull Request を作成
4. レビュー後に `main` へマージ
