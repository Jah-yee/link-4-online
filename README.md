<p align="center">
    <img src="./public/readme_header.png" width="450" alt="Link 4 Online">
</p>

# Link 4 Online
『Connect 4』が遊べるオンラインゲームです。
WebSocket と Vue.js の学習で作りました。

[ English README is here ](./README_en.md)
## 技術スタック
### フロントエンド
- TypeScript
- pnpm
- Vite
- Vue.js
- VueRouter
### バックエンド
- Python
- FastAPI
- Pydantic
- uvicorn
- websockets

## 実行方法
### Docker
#### Dev
`docker-compose.dev.yml` を使って開発コンテナを起動する
```bash
docker compose -f docker-compose.dev.yml up
```
#### Build
`docker-compose.yml` を使ってビルドしたコンテナを起動する
```bash
docker compose up
```
### pnpm + pip
#### セットアップ
1. pnpm の依存パッケージをインストールします
    ```bash
    pnpm i # or pnpm install
    ```
2. python の依存パッケージをインストールします

    venvを利用する場合はインストールする前にvenvをアクティベートしてください
    ```bash
    pip install -r requirements.txt
    ```
#### Dev
1. python サーバーを起動する

    venvを利用する場合は実行する前にvenvをアクティベートしてください
    ```bash
    pnpm backend
    ```
2. 新しいタブをでViteの開発サーバーを起動する
    ```bash
    pnpm dev
    ```

    `http://localhost:5173`でサイトにアクセスすることができます
#### Build
1. フロントエンドのファイルをビルドします
    ```bash
    pnpm build
    ```
2. python サーバーを起動する

    venvを利用する場合は実行する前にvenvをアクティベートしてください
    ```bash
    pnpm backend
    ```
    `http://localhost:8000`でビルドしたサイトにアクセスできます

## License
Private / Personal project
