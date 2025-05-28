# Flask と Azure で作る ToDo アプリ開発チュートリアル 
## step04 ToDoの未完/完了切替機能追加 
今回は、アプリケーションにToDoの未完/完了を切り替える機能を追加します。表示画面で標示されたToDo一覧のうち、未完了のものには「完了」リンクを表示します。完了済みのものには「未完了にする」リンクを標示します。それぞれのリンクをクリックすると、対応するToDoのIDがサーバーにPOST送信され、それを受けた関数がSQLAlchemy経由で対応するレコードを削除します。　　
  
Flaskアプリの中でSQLAlchemyを使用する方法については、以下のドキュメントを参照してください。
[FlaskとSQLAlchemyを使用したMariaDBへのアクセス](https://github.com/y-omasa-kbc/doc-manuals-tutorials/blob/main/python/framework/flask-sqlalchemy-mariadb.md)

### 変更点
#### app.py
```
diff --git a/app.py b/app.py
index f6a4f2c..209ee5f 100644
--- a/app.py
+++ b/app.py
@@ -103,6 +103,38 @@ def delete_todo(todo_id):
     
     return redirect(url_for('index'))
 
+@app.route('/complete_todo/<int:todo_id>', methods=['POST'])
+def complete_todo(todo_id):
+    """指定されたIDのTodoを完了済みにする"""
+    try:
+        todo_to_complete = Todo.query.get_or_404(todo_id)
+        todo_to_complete.completed = True
+        todo_to_complete.updated_at = datetime.utcnow() # 更新日時を記録
+        db.session.commit()
+        flash('Todoが完了しました', 'success')
+    except Exception as e:
+        db.session.rollback()
+        app.logger.error(f"Error completing todo {todo_id}: {e}")
+        flash('Todoの完了中にエラーが発生しました', 'danger')
+    
+    return redirect(url_for('index'))
+
+@app.route('/incomplete_todo/<int:todo_id>', methods=['POST'])
+def incomplete_todo(todo_id):
+    """指定されたIDのTodoを未完了にする"""
+    try:
+        todo_to_incomplete = Todo.query.get_or_404(todo_id)
+        todo_to_incomplete.completed = False
+        todo_to_incomplete.updated_at = datetime.utcnow() # 更新日時を記録
+        db.session.commit()
+        flash('Todoが未完了になりました', 'success')
+    except Exception as e:
+        db.session.rollback()
+        app.logger.error(f"Error incompleting todo {todo_id}: {e}")
+        flash('Todoの未完了化中にエラーが発生しました', 'danger')
+    
+    return redirect(url_for('index'))
+
 # --- 以下は次回以降の演習で実装する機能のルーティングです (コメントアウト) ---
 # @app.route('/todo/<int:todo_id>')
 # def todo_detail(todo_id): ...
```

#### HTMLテンプレート index.html
```
diff --git a/templates/index.html b/templates/index.html
index 7accc53..d7a7f57 100644
--- a/templates/index.html
+++ b/templates/index.html
@@ -42,6 +42,9 @@
                 {% endif %}
             </div>
             <div>
+                <form action="{{ url_for('complete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
+                    <button type="submit" class="btn btn-link text-success p-0 me-2">完了</button>
+                </form>
                 <form action="{{ url_for('delete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
                     <button type="submit" class="btn btn-link text-danger p-0" onclick="return confirm('本当に削除しますか？');">削除</button>
                 </form>
@@ -65,6 +68,9 @@
                 {% endif %}
             </div>
             <div>
+                <form action="{{ url_for('incomplete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
+                    <button type="submit" class="btn btn-link text-warning p-0 me-2">未完了にする</button>
+                </form>
                 <form action="{{ url_for('delete_todo', todo_id=todo.id) }}" method="POST" style="display:inline;">
                     <button type="submit" class="btn btn-link text-danger p-0" onclick="return confirm('本当に削除しますか？');">削除</button>
                 </form>
 ```