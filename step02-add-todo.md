# Flask と Azure で作る ToDo アプリ開発チュートリアル 
## step02 ToDo追加機能作成
今回は、アプリケーションにToDoを追加する機能を作成します。表示画面のToDo一覧表示の上に、登録するToDoの情報を入力するフォームを配置します。送信されたToDoの情報はSQLAlchemyを通してデータベースに保存されます。　　
Flaskアプリの中でSQLAlchemyを使用する方法については、以下のドキュメントを参照してください。
[FlaskとSQLAlchemyを使用したMariaDBへのアクセス](https://github.com/y-omasa-kbc/doc-manuals-tutorials/blob/main/python/framework/flask-sqlalchemy-mariadb.md)


### 変更点

#### app.py
```
diff --git a/app.py b/app.py
index 6210834..3c052b5 100644
--- a/app.py
+++ b/app.py
@@ -51,9 +51,44 @@ def index():
         todos_complete = []
     return render_template('index.html', todos_incomplete=todos_incomplete, todos_complete=todos_complete)
 
-# --- ここから下は次回以降の演習で実装する機能のルーティングです (コメントアウト) ---
-# @app.route('/add', methods=['POST'])
-# def add_todo(): ...
+# --- 実装済みの機能のルーティング ---
+@app.route('/add', methods=['POST'])
+def add_todo():
+    """新しいTodoを追加する"""
+    try:
+        title = request.form.get('title')
+        due_date_str = request.form.get('due_date')
+        memo = request.form.get('memo')
+        
+        # タイトルは必須
+        if not title:
+            flash('タイトルは必須です', 'danger')
+            return redirect(url_for('index'))
+        
+        # 新しいTodoオブジェクトを作成
+        new_todo = Todo(title=title, memo=memo)
+        
+        # 期限日が入力されていれば設定
+        if due_date_str:
+            try:
+                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
+                new_todo.due_date = due_date
+            except ValueError:
+                flash('期限日の形式が正しくありません', 'warning')
+        
+        # データベースに保存
+        db.session.add(new_todo)
+        db.session.commit()
+        
+        flash('Todoが追加されました', 'success')
+    except Exception as e:
+        db.session.rollback()
+        app.logger.error(f"Error adding todo: {e}")
+        flash('Todoの追加中にエラーが発生しました', 'danger')
+    
+    return redirect(url_for('index'))
+
+# --- 以下は次回以降の演習で実装する機能のルーティングです (コメントアウト) ---
 # @app.route('/todo/<int:todo_id>')
 # def todo_detail(todo_id): ...
 # (その他のビュー関数もコメントアウト)
```
####  HTMLテンプレート base.html
```
diff --git a/templates/base.html b/templates/base.html
index edc7a06..8bdec04 100644
--- a/templates/base.html
+++ b/templates/base.html
@@ -17,12 +17,12 @@
 <body>
     <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
         <div class="container-fluid">
-            <a class="navbar-brand" href="{{ url_for('index') }}">Flask ToDo アプリ (一覧表示編)</a>
+            <a class="navbar-brand" href="{{ url_for('index') }}">Flask ToDo アプリ (一覧・登録編)</a>
         </div>
     </nav>

     <div class="container">
-        {# flash メッセージ表示エリア (次回以降の演習で使用)
+        <!-- フラッシュメッセージ表示エリア -->
         {% with messages = get_flashed_messages(with_categories=true) %}
             {% if messages %}
                 <div class="flash-messages">
@@ -35,7 +35,6 @@
                 </div>
             {% endif %}
         {% endwith %}
-        #}

         {% block content %}
         {% endblock %}
```

####  HTMLテンプレート index.html
```
diff --git a/templates/index.html b/templates/index.html
index 294dbfb..d281a18 100644
--- a/templates/index.html
+++ b/templates/index.html
@@ -5,11 +5,27 @@
 {% block content %}
 <h1 class="mb-4">Todo リスト</h1>

-{# Todo 登録フォームは次回以降の演習で実装します (コメントアウト)
+<!-- ToDo登録フォーム -->
 <div class="card mb-4">
-    ... (登録フォームのHTML) ...
+    <div class="card-header">新しいTodoを追加</div>
+    <div class="card-body">
+        <form action="{{ url_for('add_todo') }}" method="POST">
+            <div class="mb-3">
+                <label for="title" class="form-label">タイトル</label>
+                <input type="text" class="form-control" id="title" name="title" required>
+            </div>
+            <div class="mb-3">
+                <label for="due_date" class="form-label">期限日（任意）</label>
+                <input type="date" class="form-control" id="due_date" name="due_date">
+            </div>
+            <div class="mb-3">
+                <label for="memo" class="form-label">メモ（任意）</label>
+                <textarea class="form-control" id="memo" name="memo" rows="3"></textarea>
+            </div>
+            <button type="submit" class="btn btn-primary">追加</button>
+        </form>
+    </div>
 </div>
-#}
```