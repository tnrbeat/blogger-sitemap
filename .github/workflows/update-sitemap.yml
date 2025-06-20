name: Update Blogger Sitemap

on:
  workflow_dispatch:  # 手動実行
  schedule:
    - cron: '0 3 * * *'  # JSTで毎日12:00（UTC 03:00）に実行

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: リポジトリをチェックアウト
      uses: actions/checkout@v3

    - name: Pythonをセットアップ
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: 依存パッケージをインストール
      run: pip install feedparser

    - name: Bloggerのフィードを読み込んでsitemap.xmlを作成
      run: |
        python generate_sitemap.py

    - name: sitemap.xmlをコミット＆プッシュ
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git pull origin main --rebase
        git add sitemap.xml
        git commit -m "Update sitemap.xml [auto]" || echo "No changes to commit"
        git push origin main
