# Node-RED-DataCleansing Release Notes

## 6.0.1

* パイプライン実行環境のvmImageのバージョン変更(20.04→22.04)
* ドキュメント更新

## 2.0.0

* ログ出力標準化対応
* SetFormatInfoノードをグローバル設定ノード化
* data-cleansingノード改善
  * フォーマットIDとフォーマット情報の設定機能追加
  * 変換エラー処理のオプション追加
  * 新規変換関数の追加、修正

## 1.0.3

* Node-RED-Templateをマージ
  * 格納先Artifactsをビルドの種類(手動/Tag)によって変更
  * 他必要ファイル取り込み
* data-cleansingノードの潜在不具合対応
  * 入力メッセージの形式に配列を選択した際に、必ずエラーが発生する潜在不具合を修正
* data-cleansingノード修正
  * fs.rmdirSyncのrecursiveオプションが非推奨となり将来的に削除されるため、fs.rmSyncに変更
* アイコンを変更

## 1.0.2

* 1.0.1のリリースビルドパッケージ

## 1.0.1

* data-cleansingノード不具合対応
  * フォーマット情報サイズが一定量を超えると実行時エラーが発生する不具合を修正。

## 1.0.0

* 新規作成
  * get-format-number ノード
  * set-format-info ノード
  * data-cleansing ノード
