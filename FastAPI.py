from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

# Initialize the FastAPI app
app = FastAPI()

# Mount the static directory for serving CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up template rendering using Jinja2
templates = Jinja2Templates(directory="templates")

# MongoDB Atlas connection string
client = MongoClient("mongodb+srv://ekaanshkhosla007:12345@cluster0.ql8yi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select the database and collection
db = client["calculator_db"]  # Use your preferred database name
collection = db["calculations"]  # Use your preferred collection name

# Define a root route to display an HTML form
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route to add two numbers and save them in MongoDB Atlas
@app.get("/add", response_class=HTMLResponse)
def add_numbers(request: Request, a: float, b: float):
    result = a + b
    
    # Create the data to be saved in MongoDB
    data = {
        "a": a,
        "b": b,
        "result": result
    }
    
    # Insert the data into MongoDB collection
    collection.insert_one(data)
    
    # Return the result along with the HTML page
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
