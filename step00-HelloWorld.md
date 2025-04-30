# Azure App Service用のPython + Flaskアプリケーション

このドキュメントでは、Azure App Serviceにデプロイ可能な「Hello World from Azure App Service」と表示するシンプルなFlaskアプリケーションの各ファイルについて詳しく説明します。

## 1. app.py

`app.py`はFlaskアプリケーションのメインファイルです。このファイルにはWebアプリケーションのルーティングとビジネスロジックが含まれています。

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World from Azure App Service'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 詳細説明

- `from flask import Flask`: Flaskフレームワークをインポートします。
- `app = Flask(__name__)`: Flaskアプリケーションのインスタンスを作成します。`__name__`は現在のモジュール名を表します。
- `@app.route('/')`: ルートURL（'/'）へのHTTP GETリクエストを処理するルートを定義します。
- `def hello_world():`: ルートURLにアクセスした際に実行される関数を定義します。
- `return 'Hello World from Azure App Service'`: ブラウザに表示されるテキストを返します。
- `if __name__ == '__main__':`: このスクリプトが直接実行された場合にのみ以下のコードを実行します。
- `app.run(host='0.0.0.0', port=5000, debug=True)`: 開発サーバーを起動します。`host='0.0.0.0'`はすべてのネットワークインターフェースでリッスンすることを意味し、`port=5000`はポート5000を使用することを指定します。`debug=True`はデバッグモードを有効にします。

## 2. requirements.txt

`requirements.txt`はPythonの依存関係を管理するためのファイルです。このファイルには、アプリケーションが必要とするPythonパッケージとそのバージョンが記載されています。

```
flask==2.3.3
gunicorn==21.2.0
```

### 詳細説明

- `flask==2.3.3`: Flaskフレームワークのバージョン2.3.3をインストールします。Flaskは軽量なWebアプリケーションフレームワークで、ルーティング、リクエスト処理、レスポンス生成などの機能を提供します。
- `gunicorn==21.2.0`: Gunicorn（Green Unicorn）のバージョン21.2.0をインストールします。GunicornはPythonのWSGI HTTPサーバーで、本番環境でFlaskアプリケーションを実行するために使用されます。Azure App Serviceでは、このサーバーを使用してアプリケーションをホストします。

## 3. web.config

`web.config`はAzure App ServiceのIIS（Internet Information Services）ウェブサーバーの設定ファイルです。このファイルは、IISがPythonアプリケーションを実行するための設定を定義します。

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" scriptProcessor="D:\home\Python310\python.exe|D:\home\Python310\wfastcgi.py" resourceType="Unspecified" requireAccess="Script"/>
    </handlers>
    <rewrite>
      <rules>
        <rule name="Static Files" stopProcessing="true">
          <match url="^/static/.*" ignoreCase="true"/>
          <action type="Rewrite" url="^/static/.*" appendQueryString="true"/>
        </rule>
        <rule name="Configure Python" stopProcessing="true">
          <match url="(.*)" ignoreCase="false"/>
          <action type="Rewrite" url="app.py"/>
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
  <appSettings>
    <add key="WSGI_HANDLER" value="app.app"/>
    <add key="PYTHONPATH" value="D:\home\site\wwwroot"/>
    <add key="WSGI_LOG" value="D:\home\LogFiles\wfastcgi.log"/>
  </appSettings>
</configuration>
```

### 詳細説明

- `<handlers>`: IISがリクエストを処理するためのハンドラーを定義します。
  - `<add name="PythonHandler" ...>`: すべてのリクエスト（`path="*"`、`verb="*"`）をPythonハンドラーで処理するように設定します。`scriptProcessor`はPythonインタープリターとwfastcgi.pyスクリプトのパスを指定します。

- `<rewrite>`: URLの書き換えルールを定義します。
  - `<rule name="Static Files" ...>`: `/static/`で始まるURLは静的ファイルとして処理します。
  - `<rule name="Configure Python" ...>`: その他のすべてのURLは`app.py`にリダイレクトされます。

- `<appSettings>`: アプリケーション設定を定義します。
  - `WSGI_HANDLER`: WSGIアプリケーションのエントリーポイントを指定します（`app.py`の`app`オブジェクト）。
  - `PYTHONPATH`: Pythonモジュールを検索するパスを指定します。
  - `WSGI_LOG`: ログファイルのパスを指定します。

## 4. startup.txt

`startup.txt`はAzure App Serviceがアプリケーションを起動する際に実行するコマンドを指定するファイルです。

```
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

### 詳細説明

- `gunicorn`: Gunicorn WSGIサーバーを使用してアプリケーションを実行します。
- `--bind=0.0.0.0`: すべてのネットワークインターフェースでリッスンします。
- `--timeout 600`: リクエスト処理のタイムアウトを600秒（10分）に設定します。
- `app:app`: `app.py`ファイル内の`app`オブジェクトをWSGIアプリケーションとして使用することを指定します。

## 5. .gitignore

`.gitignore`はGitバージョン管理システムで無視すべきファイルやディレクトリを指定するファイルです。これにより、不要なファイルやディレクトリがリポジトリにコミットされるのを防ぎます。

```
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
*.log
```

### 詳細説明

- `# Virtual Environment`: 仮想環境関連のディレクトリを無視します。
  - `venv/`, `env/`, `ENV/`: 一般的な仮想環境ディレクトリ名です。

- `# Python`: Python関連の一時ファイルやビルドファイルを無視します。
  - `__pycache__/`: Pythonのコンパイル済みバイトコードを含むディレクトリです。
  - `*.py[cod]`: `.pyc`、`.pyo`、`.pyd`ファイル（コンパイル済みPythonファイル）を無視します。
  - その他のビルド関連ディレクトリやファイル。

- `# IDE`: 統合開発環境（IDE）の設定ファイルを無視します。
  - `.idea/`: JetBrains IDEs（PyCharmなど）の設定ディレクトリです。
  - `.vscode/`: Visual Studio Codeの設定ディレクトリです。
  - `*.swp`, `*.swo`: Vimエディタの一時ファイルです。

- `# Logs`: ログファイルを無視します。
  - `*.log`: すべてのログファイルを無視します。

## まとめ

これらのファイルを組み合わせることで、Azure App Serviceにデプロイ可能なPython + Flaskアプリケーションの基本構造が完成します。このアプリケーションはブラウザで「Hello World from Azure App Service」と表示するシンプルなものですが、より複雑なアプリケーションを構築するための基盤となります。
