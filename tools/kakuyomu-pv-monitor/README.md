# カクヨムPVモニター（試作・実サイト未検証）

対象：『最強じゃなくなった俺がこのゲームをクリアする！』
https://kakuyomu.jp/works/11054822663706183433

## 方式
公開ページをChromiumで開き、見えている「詳細」タブのPVテキストだけを読み取り、data/pv_history.csvに記録します。非公開API・認証情報・アクセス制限回避は使用しません。数値が曖昧なら、誤記録を防ぐため失敗します。初期値708PVは本人申告として記録済みです。

**重要：この環境から実サイト上でブラウザを操作していないため、自動取得が成功するかは未検証です。GitHub Actionsは手動実行のみで、定期実行はまだ有効化していません。Notionへの自動反映も未接続です。**

## 実行方法
GitHubリポジトリの「Actions」→「Kakuyomu PV monitor (experimental)」→「Run workflow」。成功した場合はCSVがGitHubにコミットされます。

WindowsまたはMacで直接実行する場合、Python 3.12以上をインストールし、リポジトリのルートで以下を実行します。

```bash
python -m pip install -r tools/kakuyomu-pv-monitor/requirements.txt
python -m playwright install chromium
python tools/kakuyomu-pv-monitor/monitor.py
```

サイトへアクセスせず確認済みPVを記録したい場合は、`python tools/kakuyomu-pv-monitor/monitor.py --manual-pv 708` を使用してください。

## 次の段階
最初の手動実行でカクヨムの画面表示と取得値が一致するか検証し、問題がない場合に限りユーザー了承の下で定期実行を設定します。Notion連携には別途安全な認証設定が必要です。GitHub公開ファイルに秘密情報を含めないでください。

利用規約：https://kakuyomu.jp/legal/tos
