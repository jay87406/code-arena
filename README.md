# Code Arena (Numpy/Python 線上多人練習)

這是一個可部署在 Linux 的多人練習遊戲：
- 前端網頁：玩家可直接在瀏覽器解題。
- 後端 API：評分、進度、排行榜。
- 分流機制：依 `IP + client_id + 日期` 分配題目，避免所有人同一題。

## 需求
- Python 3.11+

## 安裝
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 啟動
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

瀏覽器開啟 `http://<你的主機IP>:8000`

## Docker 部署
```bash
docker compose up --build -d
```

查看狀態/日誌：
```bash
docker compose ps
docker compose logs -f
```

停止服務：
```bash
docker compose down
```

## 主要 API
- `GET /api/me` 取得玩家狀態與當前題目
- `POST /api/nickname` 更新暱稱
- `POST /api/submit` 提交程式碼
- `GET /api/leaderboard` 取得排行榜

## 注意事項
- 目前使用記憶體儲存玩家資料，服務重啟會清空。
- 程式碼執行使用簡化限制，適合內部練習環境，不建議直接暴露公網高風險環境。
- 若你放在 Nginx/Cloudflare 後方，請正確傳遞 `X-Forwarded-For`，IP 分流才會準確。
