# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Pythonの出力バッファリングを無効化（ログがリアルタイムで見える）
# .pycファイル生成を抑制（コンテナ内では不要）
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

# mysqlclient(MySQLdb)のビルドに必要なシステムパッケージ
# default-libmysqlclient-dev: mysqlclientのコンパイルに必須
# build-essential: gccなどのビルドツール
# pkg-config: ビルド時のライブラリパス解決に必要
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 依存関係だけ先にコピーしてインストール（レイヤーキャッシュを効かせる）
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# 実行用ユーザーを作成（rootで実行しない）
RUN useradd --create-home --shell /bin/bash appuser

# アプリ本体のコピー
COPY --chown=appuser:appuser ./app /code
COPY --chown=appuser:appuser entrypoint.sh /entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "tsumigee_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
