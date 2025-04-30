# Azure App Service用のFlask Hello Worldアプリケーション

ブラウザでアクセスすると「Hello World from Azure App Service」と表示するシンプルなFlaskアプリケーションです。

## ローカル開発

### 前提条件
- Python 3.10以上
- 仮想環境（venv）は既に`\venv`ディレクトリに設定済み

### ローカルでのアプリケーション実行方法

1. 仮想環境を有効化する：

   Windowsの場合：
   ```
   venv\Scripts\activate
   ```

   macOS/Linuxの場合：
   ```
   source venv/bin/activate
   ```

2. 依存関係をインストールする：
   ```
   pip install -r requirements.txt
   ```

3. アプリケーションを実行する：
   ```
   python app.py
   ```

4. ブラウザを開き、`http://localhost:5000`にアクセスする

## Azure App Serviceへのデプロイ

### 前提条件
- アクティブなサブスクリプションを持つAzureアカウントがあること
- Visual Studio Code
- VSCodeの拡張機能「Azure App Service」がインストールされていること

1. VSCodeでAzure拡張機能にログインする
   - VSCodeの左側のアクティビティバーからAzureアイコンをクリックします
   - 「Sign in to Azure...」をクリックしてAzureアカウントにログインします

2. Webアプリを作成する
   - Azureエクスプローラーで「+」アイコンをクリックするか、右クリックメニューから「Create Web App...」を選択します
   - サブスクリプションを選択します
   - Webアプリの一意の名前を入力します
   - 「Python 3.10」ランタイムスタックを選択します
   - 価格プランを選択します（開発/テスト用にはF1無料プランまたはB1ベーシックプランがおすすめです）
   - リソースグループを選択または新規作成します
   - 作成が完了するまで待ちます（数分かかることがあります）

3. アプリケーションをデプロイする
   - VSCodeのエクスプローラービューでプロジェクトを右クリックし、「Deploy to Web App...」を選択します
   - 先ほど作成したWebアプリを選択します
   - デプロイの確認メッセージが表示されたら「Deploy」をクリックします
   - デプロイが完了するまで待ちます

4. デプロイしたアプリケーションにアクセスする
   - デプロイが完了すると、VSCodeの右下に通知が表示されます
   - 通知の「Browse Website」ボタンをクリックして、ブラウザでアプリケーションを開きます
   - または、VSCodeのAzureエクスプローラーでWebアプリを右クリックし、「Browse Website」を選択してアクセスすることもできます

注: プロジェクトに含まれる`startup.txt`ファイルが自動的に起動コマンドとして使用されるため、Azure Portalで起動コマンドを手動で設定する必要はありません。

## プロジェクト構造

- `app.py`: メインアプリケーションファイル
- `requirements.txt`: Python依存関係
- `web.config`: Azure App Service用のIIS設定
- `startup.txt`: Azure App Service用の起動コマンド
- `.gitignore`: Gitの無視ファイル
