from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str

books = []
ids = 0
   
@app.get("/")
async def root():
    return {"message": "Pong!"}

@app.get("/books/index", response_class=HTMLResponse)
async def index():
    html: str

    html = "<h1>Book Store</h1>"
    html = "<p>Welcome to the book store!</p>"
    html += "<ol>"
    
    books_from_db = await get_books()
    
    for book in books_from_db:
        html += f"<li>Book: {book.title} - Author: {book.author} - <a href=\"/authors/{book.author}\">Author's page</a></li>"
        
    return HTMLResponse(content=html)

@app.get("/authors/{author}", response_class=HTMLResponse)
async def author(author: str):
    html: str

    html = f"<h1>Discover more about {author}!</h1>"
    html += f"<h2>Author: {author}</h2>"
    html += "<ol>"
    
    books_from_db = await get_books()
    
    for book in books_from_db:
        if book.author == author:
            html += f"<li>Book: {book.title}</li>"
        
    return HTMLResponse(content=html)

@app.post("/books", response_model=Book)
async def create_book(book: Book):
    books.append(book)
    return book

@app.get("/books/list")
async def get_books():
    return books

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    books.pop(book_id - 1)
    return {"message": "Book deleted!"}
