# Flask と Azure で作る ToDo アプリ開発チュートリアル 
## 一覧表示編

このチュートリアルでは、Python の Web フレームワークである Flask を使用して、シンプルな ToDo アプリケーションを開発します。今回の演習では、まず基本となる「Todo の一覧表示」機能のみを実装します。 Todo の登録、更新、削除、追記といったその他の機能については、次回以降の演習で段階的に実装していきます。
開発したアプリケーションは、ローカル環境での動作確認後、Microsoft Azure の App Service にデプロイします。データベースには、ローカル開発中は XAMPP に付属の MySQL (データベース名: my-rdb-clouddev) を使用し、Azure 上では Azure Database for MySQL を使用します。操作は基本的に CLI (コマンドラインインターフェース) で行います。Azure の設定は Azure Portal で直接行います。

### 学習目標:
- Flask を用いた基本的な Web アプリケーションの開発方法を理解する。
- SQLAlchemy を用いたデータベース操作の基本 (読み取り) を理解する。
- ローカル環境での MySQL (XAMPP) のセットアップと CLI での利用方法を理解する。
- Azure App Service および Azure Database for MySQL の基本的な利用方法を理解する。
- VSCode を用いた開発と Azure へのデプロイ方法を理解する。
- Python の仮想環境 (venv) の利用方法を理解する。
- requirements.txt を用いたパッケージ管理方法を理解する。

### 対象読者:
Python の基本的な文法を理解している方。
Web アプリケーション開発に興味がある方。
クラウドプラットフォーム (Azure) の利用に興味がある方。
XAMPP の利用経験がある、または利用したい方。

### 今回開発する ToDo アプリの主な機能:
- Todo の一覧表示: 登録された Todo を一覧で表示する。
### 次回以降で実装する機能 (予定):
- Todo の登録 (タイトル、期限、完了か否か、内容のメモ)
- Todo の更新 (既存 Todo の編集、完了状態の切り替え)
- Todo の削除
- Todo への追記 (追記内容、追記日時)


## ローカル開発環境の準備
まずは、ローカルの Windows PC で開発を始めるための準備を行います。

### Python のインストール状況の確認
このチュートリアルでは、Python が既にインストールされていることを前提とします。
コマンドプロンプトまたは PowerShell を開き、以下のコマンドで Python と pip (Python のパッケージ管理ツール) のバージョンが表示されることを確認してください。
```
python --version
pip --version
```
もし Python がインストールされていない場合や、バージョンが古い場合は、公式サイトから最新版の Python をダウンロードしてインストールしてください。
Python 公式サイト: https://www.python.org/downloads/windows/
インストール時には、「Add Python to PATH」のチェックボックスをオンにすることを推奨します。

### VSCode のインストールと拡張機能
Visual Studio Code (VSCode) は高機能なコードエディタで、多くの開発者に利用されています。
VSCode 公式サイト: https://code.visualstudio.com/download
VSCode をインストールしたら、以下の便利な拡張機能をインストールしておきましょう。VSCode の左側のアクティビティバーから拡張機能ビューを開き、検索してインストールします。
- Python (Microsoft): Python の開発サポート (デバッグ、リンティング、IntelliSense など)。
- Azure App Service (Microsoft): Azure App Service へのデプロイを容易にします。
- Azure Account (Microsoft): VSCode から Azure アカウントにサインインするために必要です。
- Pylance (Microsoft): より強力な Python 言語サーバー (任意ですが推奨)。

### MySQL の準備と設定 (XAMPP と CLI)
このチュートリアルでは、XAMPP に同梱されている MySQL を使用します。XAMPP が既にインストールされていることを前提とします。
1. XAMPP コントロールパネルの起動:
    XAMPP のインストールディレクトリにある xampp-control.exe を実行して、XAMPP コントロールパネルを開きます。
    [XAMPP コントロールパネルの画像]
2. MySQL の起動:
    XAMPP コントロールパネルで、MySQL モジュールの「Start」ボタンをクリックして MySQL サーバーを起動します。起動に成功すると、モジュール名の背景が緑色になり、ポート番号 (通常は 3306) が表示されます。
    [XAMPP コントロールパネルでMySQLが起動している画像]
3. MySQL コマンドラインクライアントへのパス設定 (推奨):
    MySQL コマンドラインクライアント (mysql.exe) をどのディレクトリからでも簡単に実行できるように、環境変数の Path に mysql.exe が存在するディレクトリ (例: C:\xampp\mysql\bin) を追加しておくことを推奨します。
    設定方法は Windows のバージョンによって異なりますが、通常は「システムのプロパティ」>「詳細設定」>「環境変数」からシステム環境変数の Path を編集します。
    パスを設定しない場合は、コマンドプロンプトで C:\xampp\mysql\bin ディレクトリに移動してから mysql コマンドを実行する必要があります。
4. MySQL への接続確認 (CLI):
    コマンドプロンプトまたは PowerShell を開きます。
    XAMPP の MySQL のデフォルトの root ユーザーにはパスワードが設定されていないことが多いです。以下のコマンドで接続を試みます。
```
mysql -u root
```

パスワードを要求された場合は、XAMPP インストール時または別途設定した root ユーザーのパスワードを入力します。
接続に成功すると、mysql> というプロンプトが表示されます。
```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is X
Server version: X.X.X-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
(XAMPP に含まれるのは MariaDB であることが多いですが、MySQL と互換性があります。)
接続を終了するには exit または quit と入力して Enter キーを押します。
5. データベースの作成 (CLI):
    Flask アプリケーションで使用するデータベースを CLI で作成します。データベース名は my-rdb-clouddev とします。
    再度 mysql -u root (必要であれば -p オプションでパスワード入力) で MySQL に接続し、以下の SQL コマンドを実行します。
```
CREATE DATABASE `my-rdb-clouddev` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

実行後、以下のコマンドでデータベースが作成されたことを確認できます。

```
SHOW DATABASES;
```
一覧に my-rdb-clouddev が表示されていれば成功です。
確認後、exit で MySQL モニターを終了します。
注意: XAMPP の MySQL の root ユーザーには、セキュリティのためパスワードを設定することを強く推奨します。パスワードの設定は mysqladmin コマンドや SQL ステートメント (ALTER USER 'root'@'localhost' IDENTIFIED BY '新しいパスワード'; FLUSH PRIVILEGES;) で行えます。このチュートリアルでは、簡単のためパスワードなし、または各自が設定したパスワードを前提に進めます。.env ファイルには正しいユーザー名とパスワードを設定してください。

### プロジェクトフォルダの作成と仮想環境の構築
ToDo アプリケーション用のプロジェクトフォルダを作成し、その中に Python の仮想環境を構築します。仮想環境を使用することで、プロジェクトごとに独立した Python パッケージの依存関係を管理できます。
任意の場所にプロジェクト用のフォルダを作成します (例: C:\dev\flask_todo_app)。
```
mkdir C:\dev\flask_todo_app
cd C:\dev\flask_todo_app
```

VSCode でこのフォルダを開きます (File > Open Folder...)。
VSCode のターミナルを開きます (View > Terminal または Ctrl + @)。
ターミナルで以下のコマンドを実行し、仮想環境を作成します (.venv という名前のフォルダが作成されます)。
```
python -m venv .venv
```

作成した仮想環境をアクティベートします。
PowerShell の場合:
```
.\.venv\Scripts\Activate.ps1
```

コマンドプロンプトの場合:
```
.\.venv\Scripts\activate.bat
```

アクティベートされると、ターミナルのプロンプトの先頭に (.venv) と表示されます。VSCode は通常、仮想環境を自動的に検出し、Python インタープリタとして選択するかどうかを尋ねてきます。「Yes」を選択してください。手動で選択する場合は、VSCode のステータスバーの左下にある Python のバージョン表示部分をクリックし、.venv\Scripts\python.exe を選択します。

### requirements.txt の作成と Python パッケージのインストール
プロジェクトで使用する Python パッケージとそのバージョンを requirements.txt ファイルに記述し、一括でインストールします。
requirements.txt の作成:
プロジェクトのルートディレクトリ (例: C:\dev\flask_todo_app) に、requirements.txt という名前のファイルを新規作成し、以下の内容を記述します。
```
flask==2.3.3
flask-sqlalchemy==3.0.5
python-dotenv==1.0.0
pymysql==1.1.0
gunicorn==21.2.0
```

解説:
- flask: Web フレームワーク本体。
- flask-sqlalchemy: Flask で SQLAlchemy を利用するための拡張機能。
- python-dotenv: .env ファイルから環境変数を読み込むためのライブラリ。
- pymysql: Python から MySQL (MariaDB) に接続するためのドライバ。
- gunicorn: 本番環境で Flask アプリケーションを実行するための WSGI サーバー (Azure App Service で使用)。

### パッケージの一括インストール:
仮想環境がアクティベートされた状態で、VSCode のターミナルで以下のコマンドを実行し、requirements.txt に記載されたパッケージをすべてインストールします。
```
pip install -r requirements.txt
```
これにより、指定されたバージョンのパッケージがインストールされます。
インストール後、pip freeze コマンドでインストールされたパッケージとそのバージョンが requirements.txt の内容と一致することを確認できます (依存関係で他のパッケージもインストールされる場合があります)。
```
pip freeze
```

## Flask アプリケーションの開発 (一覧表示)
環境が整ったので、Flask アプリケーションのコーディングを開始します。今回は Todo の一覧表示機能のみを実装します。
### プロジェクトの構造
プロジェクトフォルダ (flask_todo_app) 内に以下のファイルとフォルダを作成していきます。detail.html は今回は作成しません。
flask_todo_app/
├── .venv/                     # Python 仮想環境 (自動生成)
├── app.py                     # Flask アプリケーションのメインファイル
├── models.py                  # SQLAlchemy のモデル定義
├── templates/                 # HTML テンプレートを格納するフォルダ
│   ├── base.html              # ベーステンプレート
│   └── index.html             # Todo 一覧ページ
├── static/                    # CSS、JavaScript、画像などの静的ファイルを格納 (今回は未使用)
├── .env                       # 環境変数ファイル (データベース接続情報など)
└── requirements.txt           # Python パッケージのリスト


### データベースモデルの定義 (models.py)
models.py ファイルを作成し、ToDo アイテムと追記ログのデータベース構造を SQLAlchemy のモデルとして定義します。追記ログ (TodoLog) のモデルも定義しておきますが、実際の利用は次回以降の演習となります。

解説:
TodoLog モデルは定義されていますが、今回の演習では使用しません。リレーションシップも定義されていますが、実際にログを登録・表示する機能は次回以降に実装します。

### Flask アプリケーションの設定と初期化 (app.py)
プロジェクトのルートに app.py ファイルを作成し、Flask アプリケーションの基本的な設定と、先ほど定義したデータベースモデルの初期化を行います。
まず、ローカルの MySQL への接続情報を記述するための .env ファイルをプロジェクトルートに作成します。
XAMPP の MySQL のデフォルトの root ユーザーはパスワードが空の場合があります。その場合は DB_PASSWORD="" のように設定します。もしご自身でパスワードを設定した場合は、そのパスワードを記述してください。データベース名は my-rdb-clouddev に変更します。

注意: .env ファイルは機密情報を含むため、Git などのバージョン管理システムには含めないように .gitignore ファイルに .env を追加することを推奨します。
次に app.py を作成します。

解説:
load_dotenv(): .env ファイルを読み込み、そこに定義された変数を環境変数として利用できるようにします。
app = Flask(__name__): Flask アプリケーションのインスタンスを作成します。
app.config['SQLALCHEMY_DATABASE_URI']: SQLAlchemy がデータベースに接続するための情報 (接続文字列) を設定します。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False: SQLAlchemy のイベントシステムを無効にし、オーバーヘッドを削減します。
app.config['SECRET_KEY']: Flask がセッション情報や flash メッセージを安全に扱うために必要なキーです (次回以降の演習で使用)。
db.init_app(app): models.py で作成した db インスタンスを Flask アプリケーションに関連付けます。
if __name__ == '__main__': app.run(debug=True): このスクリプトが直接実行された場合に、Flask の開発用サーバーを起動します。

### HTML テンプレートの作成
ユーザーインターフェースとなる HTML ファイルを作成します。Flask はデフォルトで templates という名前のフォルダ内にある HTML ファイルを検索します。
#### ベーステンプレート (templates/base.html)
全てのページで共通するヘッダーやフッター、基本的な HTML 構造を定義します。他のテンプレートはこのベーステンプレートを継承します。
templates/base.html を作成:

解説:
基本的なHTML構造とBootstrap 5の読み込み。
{% block title %} と {% block content %} は、各ページで内容を差し替えるためのプレースホルダー。
flashメッセージ表示部分は次回以降の演習で使用するためコメントアウト。

#### Todo 一覧ページ (templates/index.html)
Todo の一覧表示のみを行うシンプルなページにします。登録フォームや操作ボタンはコメントアウトします。
templates/index.html を作成:

解説:
base.html を継承。
todos_incomplete と todos_complete リストをループしてTodoアイテムを表示。
登録フォームと操作ボタンは次回以降のためコメントアウト。
### ルーティングとビュー関数の実装 (app.py に追記)
app.py に、Todo の一覧表示を行うビュー関数を実装します。

解説:
index(): データベースから未完了と完了済みのTodoを取得し、index.html に渡してレンダリング。
その他の機能 (登録、詳細表示など) のルーティングはコメントアウト。
init-db コマンド: データベーステーブルを作成。初期データ投入の例もコメントで記載。

## ローカルでの動作確認
作成した Flask アプリケーションをローカル環境で実行し、動作を確認します。
### データベースの作成とテーブルの初期化、テストデータの投入 (CLI)
#### データベースの作成 (未実施の場合):
 my-rdb-clouddev という名前のデータベースを CLI で作成しました。まだの場合は手順 1.3.5. を参照して作成してください。
#### テーブルの初期化:
VSCode のターミナル (仮想環境がアクティベートされている状態) で、以下のコマンドを実行してデータベース内にテーブルを作成します。
```
flask init-db
```

成功すると「データベースが初期化されました。」と表示されます。
MySQL コマンドラインクライアントで USE \my-rdb-clouddev`;の後にSHOW TABLES; を実行し、todoテーブルとtodo_log` テーブルが作成されていることを確認できます。
#### テストデータの投入 (CLI - 重要):
今回は Todo の登録機能がないため、一覧表示を確認するにはデータベースに手動でデータを投入する必要があります。
MySQL コマンドラインクライアント (mysql -u root -p) で my-rdb-clouddev データベースに接続し、以下の SQL INSERT 文を実行します。
```
USE `my-rdb-clouddev`;

INSERT INTO todo (title, due_date, memo, completed, created_at, updated_at) VALUES
('牛乳を買う (CLI)', '2025-05-25', '低脂肪乳を2本 CLIから投入', 0, NOW(), NOW()),
('プレゼン資料作成 (CLI)', '2025-05-28', '最終レビューまで終わらせる CLIから投入', 0, NOW(), NOW()),
('部屋の掃除 (CLI)', NULL, '週末にまとめてやる CLIから投入', 1, '2025-05-18 10:00:00', '2025-05-18 15:30:00');

SELECT * FROM todo; -- 挿入されたデータを確認
```

### Flask 開発サーバーの起動
VSCode のターミナルで、以下のコマンドを実行して Flask の開発サーバーを起動します。
```
python app.py
```

サーバーが起動すると、http://127.0.0.1:5000 でアプリケーションが実行されている旨のメッセージが表示されます。
### ブラウザでの動作確認 (一覧表示)
Web ブラウザを開き、アドレスバーに http://127.0.0.1:5000 と入力してアクセスします。
投入したテストデータが、未完了と完了済みに分かれて正しく表示されることを確認してください。


## Azure 環境の準備
ローカルでの開発とテストが完了したら、次は Azure にデプロイするための準備を行います。

### Azure アカウントの作成
Azure を利用するには、Microsoft アカウントと Azure サブスクリプションが必要です。
まだ持っていない場合は、Azure の公式サイトから作成してください。
Azure 公式サイト: https://azure.microsoft.com/

### Azure Database for MySQL の作成
Azure Portal (https://portal.azure.com/) にサインインし、以下の手順で Azure Database for MySQL (フレキシブルサーバー) を作成します。
「＋ リソースの作成」 > 「Azure Database for MySQL」を検索・選択。
「フレキシブル サーバー」を選択して「作成」。
基本設定:
リソース グループ: 新規作成 (例: rg-todo-app)。
サーバー名: グローバルに一意な名前 (例: mysql-todo-app-yourname)。
リージョン: (例: Japan East)。
MySQL バージョン: (例: 8.0)。
ワークロードの種類: 「開発/テスト」。コンピューティングとストレージは最小構成で開始可能。
管理者ユーザー名とパスワード: 設定し、必ず控えておく。
ネットワーク設定:
接続方法: 「パブリック アクセス (許可された IP アドレス)」。
ファイアウォール規則: 「現在のクライアント IP アドレスを追加」し、「Azure サービスからのパブリック アクセスを許可する」をオンにする。
「確認および作成」 > 「作成」。
デプロイ完了後、作成した Azure Database for MySQL サーバーに接続し (ローカルの mysql コマンドラインクライアントや MySQL Workbench を使用)、アプリケーション用のデータベース (例: todo_app_azure) を CLI で作成します。
```
CREATE DATABASE todo_app_azure CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

接続には、Azure Portal で確認できるサーバー名、管理者ユーザー名、設定したパスワードが必要です。ファイアウォールでローカルPCのIPが許可されていることを確認してください。

### Azure App Service の作成
Azure Portal で Web App を作成します。
「＋ リソースの作成」 > 「Web App」を検索・選択。
基本設定:
リソース グループ: 上記で作成したものを選択。
名前: グローバルに一意なアプリ名 (例: flask-todo-app-yourname)。
公開: 「コード」。
ランタイム スタック: 「Python 3.x」 (ローカル環境に合わせる)。
オペレーティング システム: 「Linux」。
リージョン: Azure Database for MySQL と同じリージョン。
App Service プラン: 新規作成 (例: asp-todo-app)。SKU は「Free (F1)」または「Basic (B1)」で開始可能。
「確認および作成」 > 「作成」。

## Azure へのデプロイ
### データベース接続情報の変更
app.py は環境変数から接続情報を読み取るため、コードの変更は不要です。Azure App Service のアプリケーション設定で環境変数を設定します。
### requirements.txt の確認
プロジェクトのルートディレクトリに requirements.txt が存在し、1.5. で作成した内容 (特に gunicorn が含まれていること) を確認します。このファイルがデプロイ時に使用されます。
### App Service の構成 (Azure Portal)
Azure App Service の環境変数とスタートアップコマンドを Azure Portal で直接設定します。
#### アプリケーション設定 (環境変数)
Azure Portal で作成した App Service に移動し、「構成」 > 「アプリケーション設定」タブを開きます。
「＋ 新しいアプリケーション設定」をクリックし、以下の設定を追加・保存します。
名前: DB_USER
値: Azure Database for MySQL の管理者ユーザー名 (例: azure_admin@mysql-todo-app-yourname)
名前: DB_PASSWORD
値: Azure Database for MySQL の管理者パスワード
名前: DB_HOST
値: Azure Database for MySQL のサーバー名 (例: mysql-todo-app-yourname.mysql.database.azure.com)
名前: DB_NAME
値: Azure 上のデータベース名 (例: todo_app_azure)
名前: SECRET_KEY

設定を追加したら、必ずページ上部の「保存」をクリックします。変更を適用するために App Service が再起動されることがあります。

#### スタートアップコマンド
App Service の「構成」ページで、「全般設定」タブを選択します。
「スタック設定」セクションの「スタートアップ コマンド」フィールドに、以下の Gunicorn コマンドを入力・保存します。
````
gunicorn --bind=0.0.0.0 --timeout 600 app:app --preload
````

解説:
app:app: app.py ファイル内の Flask アプリケーションインスタンス app を指します。
--bind=0.0.0.0: App Service がリクエストを受け付けるために必要です。
--timeout 600: タイムアウト設定 (秒)。
--preload: メモリ使用量を削減するのに役立ちます。
#### データベーステーブルの初期化 (Azure 上)
デプロイ後、App Service の「SSH」機能を使ってコンテナに接続し、flask init-db コマンドを実行して Azure Database for MySQL にテーブルを作成します。
App Service の「SSH」 > 「移動 →」。
ターミナルで cd /home/site/wwwroot。
source /antenv/bin/activate (仮想環境をアクティベート)。
flask init-db を実行。

### VSCode を使用したデプロイ
VSCode の Azure 拡張機能を使用します。
Azure にサインイン。
Azure ビューで App Service 名を右クリック > 「Deploy to Web App...」。
デプロイするフォルダ (プロジェクトフォルダ) を選択し、確認後「Deploy」。
5.5. Azure上データベースへのテストデータ投入 (CLI または MySQL Workbench)
Azure Database for MySQL に接続し (ローカルの mysql コマンドラインクライアントや MySQL Workbench を使用。ファイアウォール設定確認)、テストデータを投入します。
```
USE todo_app_azure; -- Azure 上のデータベース名

INSERT INTO todo (title, due_date, memo, completed, created_at, updated_at) VALUES
('Azure Task 1 (CLI)', '2025-05-26', 'Deployed to App Service (CLI)', 0, NOW(), NOW()),
('Azure Task 2 (CLI)', '2025-05-27', 'Test DB Connection (CLI)', 0, NOW(), NOW());

SELECT * FROM todo;
```

## Azure 上での動作確認
### デプロイされたアプリケーションへのアクセス
App Service の「概要」ページに表示されている URL (例: https://flask-todo-app-yourname.azurewebsites.net) にブラウザでアクセスします。
### 動作テスト (一覧表示)
Azure Database for MySQL に投入したテストデータが正しく一覧表示されることを確認します。
### ログの確認 (トラブルシューティング)
問題発生時は、App Service の「ログ ストリーム」や「App Service ログ」でエラーを確認します。

## まとめと次のステップ
このチュートリアル (一覧表示編) では、Flask と XAMPP の MySQL を用いたローカル開発から、Azure App Service および Azure Database for MySQL へのデプロイまでの一連の流れ (一覧表示機能のみ) を学びました。Azure の設定は Azure Portal で直接行いました。
次回以降のステップ:
Todo の登録、詳細表示、更新、削除、追記機能の実装など。
このチュートリアルが、Flask と Azure を用いた Web アプリケーション開発の第一歩となれば幸いです。
