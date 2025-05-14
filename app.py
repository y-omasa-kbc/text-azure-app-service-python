import os
from flask import Flask, render_template, request, redirect, url_for, flash # request, redirect, url_for, flash は次回以降で使用
from dotenv import load_dotenv
from models import db, Todo, TodoLog # models.py からインポート
from datetime import datetime

# .env ファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# SQLAlchemy の設定
# 環境変数からデータベース接続情報を取得
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# pymysql を使用する場合の接続文字列
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
# データベースの変更を追跡しない (パフォーマンス向上のため)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# flash メッセージ用のシークレットキー (次回以降で使用)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key') # .env に SECRET_KEY を設定するか、直接文字列を指定

# データベースインスタンスを Flask アプリケーションに紐付け
db.init_app(app)


# datetime オブジェクトをテンプレートで使えるようにコンテキストプロセッサを定義
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    """Todo の一覧を表示し、未完了と完了済みに分けて表示する"""
    try:
        # Use CASE expression to handle NULL values in MySQL (which doesn't support NULLS LAST)
        from sqlalchemy import case, desc
        todos_incomplete = Todo.query.filter_by(completed=False).order_by(
            case((Todo.due_date == None, 1), else_=0),  # NULL values last
            Todo.due_date.asc(),
            Todo.created_at.desc()
        ).all()
        todos_complete = Todo.query.filter_by(completed=True).order_by(Todo.updated_at.desc()).all()
    except Exception as e:
        app.logger.error(f"Error fetching todos: {e}")
        todos_incomplete = []
        todos_complete = []
    return render_template('index.html', todos_incomplete=todos_incomplete, todos_complete=todos_complete)

# --- ここから下は次回以降の演習で実装する機能のルーティングです (コメントアウト) ---
# @app.route('/add', methods=['POST'])
# def add_todo(): ...
# @app.route('/todo/<int:todo_id>')
# def todo_detail(todo_id): ...
# (その他のビュー関数もコメントアウト)


# データベースの初期化コマンド (Flask CLI)
@app.cli.command('init-db')
def init_db_command():
    """データベーステーブルを作成または再作成します。"""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            print('データベースが初期化されました。')
            # 初期データ投入の例 (コメントアウト)
            # from datetime import date
            # initial_todo1 = Todo(title="最初のTodoタスク", memo="これは最初のタスクのメモです。")
            # db.session.add(initial_todo1)
            # db.session.commit()
            # print('初期データが投入されました。')
        except Exception as e:
            print(f'データベース初期化中にエラーが発生しました: {e}')

if __name__ == '__main__':
    # 開発時はデバッグモードを有効にする
    app.run(debug=True)
