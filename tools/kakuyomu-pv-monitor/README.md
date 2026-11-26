# カクヨムPVモニター（取得・Notion連携検証済み）

対象：『最強じゃなくなった俺がこのゲームをクリアする！』  
https://kakuyomu.jp/works/11054822663706183433

## 仕組みとスケジュール

- **毎日09:00 JST**: GitHub Actions がカクヨムの公開作品ページをブラウザで開き、見えている「詳細」タブの累計PVを読み取って `data/pv_history.csv` に記録します（UTCのcron `0 0 * * *`）。GitHubのスケジュール実行は混雑により遅延や欠落が起こり得ます。
- **毎日10:00 JST**: ChatGPTのタスクがGitHubの当日実測（`source=public_detail_ui`）を読み、Notionの既存執筆目標「最強じゃなくなった俺がこのゲームをクリアする！ 累計10,000PV」の「現在値」を更新します。
- 新しい実測がない日やPV値が以前より小さい場合、Notionに古い値・疑わしい値を書きません。
- **安全性**: カクヨムのログイン情報・非公開APIは使用しません。Notionの接続認証はChatGPTのNotion連携によって行い、GitHubの公開コードにNotionのトークンは保存しません。

## 検証記録

- 2026-11-26 10:25 JST：GitHub Actionsから公開作品ページを取得し、累計708PVを抽出・CSVに保存しました。 [実行ログ](https://github.com/afterschool7733-oss/-/actions/runs/45735595778)
- 2026-11-26：Notion連携の手動テストでGitHubの実測708PVを既存執筆目標に反映し、読み直して一致を検証しました。比較用の本人申告は第1話66PV／第2話49PVです。
- 2026-11-27からの**定期実行そのものは未検証**です。取得または同期に失敗した場合、実測値を捏造せず障害として扱います。

## 実行方法

- 手動実行：リポジトリの「Actions」→「Kakuyomu PV monitor」→「Run workflow」。
- Windows/Macでの実行（Python 3.12以上）：

```bash
python -m pip install -r tools/kakuyomu-pv-monitor/requirements.txt
python -m playwright install chromium
python tools/kakuyomu-pv-monitor/monitor.py
```

- 確認済みの数値を手動記録する場合は `python tools/kakuyomu-pv-monitor/monitor.py --manual-pv 708` を使用します。記録源は区別され、自動同期は公開画面の実測のみを参照します。

## 参照先

- [履歴CSV](./data/pv_history.csv)
- [GitHub Actions](../../.github/workflows/kakuyomu-pv.yml)
- [Notion執筆目標](https://app.notion.com/p/42414092dbc9811e8286dddc01050d5c)
- [カクヨム利用規約](https://kakuyomu.jp/legal/tos)
