# Flask と Azure で作る ToDo アプリ開発チュートリアル 
## step03 ToDo削除機能追加
今回は、アプリケーションにToDoを削除する機能を作成します。表示画面で標示されたToDo一覧の各項目に、削除リンクを配置します。このリンクをクリックすると、対応するToDoのIDがサーバーにPOST送信され、それを受けた関数がSQLAlchemy経由で対応するレコードを削除します。　　
Flaskアプリの中でSQLAlchemyを使用する方法については、以下のドキュメントを参照してください。
[FlaskとSQLAlchemyを使用したMariaDBへのアクセス](https://github.com/y-omasa-kbc/doc-manuals-tutorials/blob/main/python/framework/flask-sqlalchemy-mariadb.md)


### 変更点

#### app.py
```
diff --git a/app.py b/app.py
index 3c052b5..f6a4f2c 100644
--- a/app.py
+++ b/app.py
@@ -1,7 +1,7 @@
 import os
-from flask import Flask, render_template, request, redirect, url_for, flash # request, redirect, url_for, flash は次回以降で使用
+from flask import Flask, render_template, request, redirect, url_for, flash
 from dotenv import load_dotenv
-from models import db, Todo, TodoLog # models.py からインポート
+from models import db, Todo, TodoLog
 from datetime import datetime
 
 # .env ファイルから環境変数を読み込む
@@ -88,6 +88,21 @@ def add_todo():
     
     return redirect(url_for('index'))
 
+@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
+def delete_todo(todo_id):
+    """指定されたIDのTodoを削除する"""
+    try:
+        todo_to_delete = Todo.query.get_or_404(todo_id)
+        db.session.delete(todo_to_delete)
+        db.session.commit()
+        flash('Todoが削除されました', 'success')
+    except Exception as e:
+        db.session.rollback()
+        app.logger.error(f"Error deleting todo {todo_id}: {e}")
+        flash('Todoの削除中にエラーが発生しました', 'danger')
+    
+    return redirect(url_for('index'))
+
 # --- 以下は次回以降の演習で実装する機能のルーティングです (コメントアウト) ---
 # @app.route('/todo/<int:todo_id>')
 # def todo_detail(todo_id): ...

```

####  HTMLテンプレート index.html
```
diff --git a/templates/index.html b/templates/index.html
index d281a18..7accc53 100644
--- a/templates/index.html
+++ b/templates/index.html
@@ -41,11 +41,11 @@
                     <small class="d-block text-muted">メモ: {{ todo.memo }}</small>
                 {% endif %}
             </div>
-            {# 操作ボタン類は次回以降の演習で実装します (コメントアウト)
             <div>
-                ... (操作ボタンのHTML) ...
+                <form action="{{ url_for('delete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
+                    <button type="submit" class="btn btn-link text-danger p-0" onclick="return confirm('本当に削除しますか？');">削除</button>
+                </form>
             </div>
-            #}
         </li>
         {% endfor %}
     </ul>
@@ -64,11 +64,11 @@
                     <small class="d-block text-muted">期限: {{ todo.due_date.strftime('%Y-%m-%d') }}</small>
                 {% endif %}
             </div>
-            {# 操作ボタン類は次回以降の演習で実装します (コメントアウト)
             <div>
-                ... (操作ボタンのHTML) ...
+                <form action="{{ url_for('delete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
+                    <button type="submit" class="btn btn-link text-danger p-0" onclick="return confirm('本当に削除しますか？');">削除</button>
+                </form>
             </div>
-            #}
         </li>
         {% endfor %}
     </ul>
```