from flask import Flask, render_template, request, jsonify

from sqlalchemy import create_engine, String, DateTime, Integer, select, text

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker

from datetime import datetime

import sqlite3

con = sqlite3.connect(r'banco.db')
class base(DeclarativeBase): pass
engine = create_engine(r'sqlite:///banco.db')

APP = Flask(__name__)

class Livro(base):
    __tablename__ = 'livros'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    author: Mapped[str] = mapped_column(String(60))
    ISSN: Mapped[str] = mapped_column(String(60))
    publishing_date: Mapped[datetime] = mapped_column(DateTime)
    paginas: Mapped[int] = mapped_column(Integer)

base.metadata.create_all(engine)
session = sessionmaker(engine)

@APP.get('/')
def group_members():
    return render_template('index.html', list_pessoas=['Cesar Cunha Ziobro'])

@APP.get('/register_book')
def register_book():
    return render_template('create_books.html')

@APP.post('/books')
def add_books():
    data = request.get_json()
    data['publishing_date'] = datetime.strptime(data['publishing_date'], '%d/%m/%y')
    new_book = Livro(**data)
    with session() as sesh:
        sesh.add(new_book)
        sesh.commit()
    return {'status': 'created'}, 200
        
@APP.get('/books')
def get_books():
    with session() as sesh:
        livros = sesh.scalars(select(Livro)).all()
    livros_dict = [
        {
            "id": livro.id,
            "title": livro.title,
            "author": livro.author,
            "ISSN": livro.ISSN,
            "publishing_date": livro.publishing_date.strftime('%d/%m/%y') if livro.publishing_date else None,
            "paginas": livro.paginas
        }
        for livro in livros
    ]
    
    return render_template('livros.html', books=livros_dict)


if __name__ == '__main__':
    APP.run(debug=True)