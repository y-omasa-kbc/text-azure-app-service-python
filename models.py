from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    memo = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # TodoLog とのリレーションシップ (次回以降の演習で使用)
    logs = db.relationship('TodoLog', backref='todo', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Todo {self.id}: {self.title}>'

class TodoLog(db.Model): # 今回は使用しませんが、定義は残しておきます
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    log_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TodoLog {self.id} for Todo {self.todo_id}>'
