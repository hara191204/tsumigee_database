# tsumigee_database

自分が所持しているゲームソフトをデータベースで管理する Web アプリ。

## 技術スタック

| カテゴリ | 技術 |
| --- | --- |
| サーバー | Raspberry Pi 5 |
| コンテナ | Docker / Docker Compose |
| バックエンド | Django 6.0.6 (Python 3.12) |
| データベース | MySQL 8.4 |
| Web サーバー | Gunicorn |
| リンター / フォーマッター | Ruff |
| git hook 管理 | pre-commit |
| コミットルール | Conventional Commits + Commitlint |
| 開発フロー | GitHub Flow |

## ディレクトリ構成

```text
tsumigee_database/
├── app/                         # Django プロジェクト
│   ├── manage.py
│   └── tsumigee_project/
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│       └── asgi.py
├── .vscode/
│   └── settings.json            # VSCode 設定（venv 自動有効化）
├── Dockerfile                   # Django コンテナ定義
├── docker-compose.yml           # サービス構成定義
├── requirements.txt             # Python 依存パッケージ
├── .env.example                 # 環境変数テンプレート
├── .pre-commit-config.yaml      # pre-commit フック設定
├── commitlint.config.js         # コミットメッセージルール
└── package.json                 # Node.js 依存パッケージ（commitlint 用）
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

#### 6. Docker イメージをビルドして起動

```bash
docker compose build
docker compose up
```

ブラウザで `http://<RaspberryPiのIPアドレス>:8000` にアクセスして確認。

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

コミット時に pre-commit が ruff（コード品質）と commitlint（メッセージ形式）を自動で検証する。

## 開発フロー

[GitHub Flow](https://docs.github.com/ja/get-started/using-github/github-flow) に従う。

1. `main` から feature ブランチを作成

   ```bash
   git checkout -b feat/xxx
   ```

2. 変更をコミット（Conventional Commits 形式）
3. GitHub にプッシュして Pull Request を作成
4. レビュー後に `main` へマージ
