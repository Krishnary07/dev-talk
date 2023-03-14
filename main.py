import os
import openai 
import re

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import Engine, Completion,api_key
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI()
templates = Jinja2Templates(directory="templates")

# CORS

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

openai.api_key = "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"



class Conversation(BaseModel):
    messages: list = []

conversation = Conversation()

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint to generate response
@app.post("/response")
async def generate_response(message: str):
    global conversation
    conversation.messages.append({"user": message})

    patterns=[
        r".*python\b",
        r".*golang\b",
        r".*javascript\b",
        r".*java\b",
        r".*c\b",
        r".*c++\b",
        r".*c#\b",
        r".*php\b",
        r".*ruby\b",
        r".*swift\b",
        r".*kotlin\b",
        r".*rust\b",
        r".*scala\b",
        r".*haskell\b",
        r".*perl\b",
        r".*lua\b",
        r".*erlang\b",
        r".*elixir\b",
        r".*clojure\b",
        r".*coffeescript\b",
        r".*typescript\b",
        r".*dart\b",
        r".*f#\b",
        r".*r\b",
        r".*visual basic\b",
        r".*pascal\b",
        r".*fortran\b",
        r".*assembly\b",
        r".*prolog\b",
        r".*lisp\b",
        r".*scheme\b",
        r".*ocaml\b",
        r".*haxe\b",
        r".*nim\b",
        r".*crystal\b",
        r".*d\b",
        r".*dlang\b",
        r".*nimrod\b",
        r".*cython\b",
        r".*cython\b",
        r".*database\b",
        r".*sql\b", 
        r".*mysql\b",
        r".*postgresql\b",
        r".*sqlite\b",
        r".*mongodb\b",
        r".*redis\b",
        r".*nosql\b",
        r".*c++\b",
        r".*code\b",
        r".*program\b",
        r".*coding\b",
        r".*programming\b",
        r".*language\b",
        r".*syntax\b",
        r".*algorithm\b",
        r".*function\b",
        r".*method\b",
        r".*object\b",
        r".*class\b",
        r".*variable\b",
        r".*loop\b",
        r".*array\b",
        r".*list\b",
        r".*dictionary\b",
        r".*tuple\b",
        r".*set\b",
        r".*string\b",
        r".*integer\b",
        r".*float\b",
        r".*boolean\b",
        r".*if\b",
        r".*else\b",
        r".*elif\b",
        r".*while\b",
        r".*for\b",
        r".*try\b",
        r".*except\b",
        r".*raise\b",
        r".*import\b",
        r".*from\b",
        r".*as\b",
        r".*def\b",
        r".*return\b",
        r".*print\b",
        r".*input\b",
        r".*open\b",
        r".*write\b",
        r".*read\b",
        r".*close\b",
        r".*append\b",
        r".*split\b",
        r".*join\b",
        r".*sort\b",
        r".*reverse\b",
        r".*map\b",
        r".*filter\b",
        r".*reduce\b",
        r".*lambda\b",
        r".*decorator\b",
        r".*classmethod\b",
        r".*staticmethod\b",
        r".*property\b",
        r".*super\b",
        r".*self\b",
        r".*__init__\b",
        r".*__str__\b",
        r".*__repr__\b",
        r".*__len__\b",
        r".*__getitem__\b",
        r".*__setitem__\b",
        r".*__delitem__\b",
        r".*__contains__\b",
        r".*__call__\b",
        r".*__add__\b",
        r".*__sub__\b",
        r".*__mul__\b",
        r".*__div__\b",
        r".*__eq__\b",
        r".*__ne__\b",
        r".*__lt__\b",
        r".*__gt__\b",
        r".*__le__\b",
        r".*__ge__\b",
        r".*__enter__\b",
        r".*__exit__\b",
        r".*__iter__\b",
        r".*__next__\b",
        r".*__bool__\b",
        r".*__int__\b",
        r".*__float__\b",
        r".*__hash__\b",
        r".*__name__\b",
        r".*__doc__\b",
        r".*__module__\b",
        r".*__class__\b",
        r".*__slots__\b",
        r".*__dict__\b",
        r".*__weakref__\b",
        r".*__dir__\b",
        r".*__file__\b",
        r".*__package__\b",
        r".*__loader__\b",
        r".*__spec__\b",
        r".*__annotations__\b",
        r".*__builtins__\b",
        r".*__cached__\b",
        r".*__debug__\b",
        r".*__import__\b",
        r".*__loader__\b",
        r".*__main__\b",
        r".*__name__\b",
        r".*__package__\b",
        r".*__path__\b",
        r".*__spec__\b",
        r".*__all__\b",
        r".*__author__\b",
        r".*__builtins__\b",
        r".*__cached__\b",
        r".*__credits__\b",
        r".*__date__\b",
    ]

    if not any(re.search(keyword, message, re.IGNORECASE) for keyword in patterns):
        response_text = "Please ask me a programming-related question."
        conversation.messages.append({"bot": response_text})
        return {"response": response_text}
    
    else:
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}\n\nResponse:",
        temperature=0.5,
        max_tokens=1024,
        n = 1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )


    conversation.messages.append({"bot": response.choices[0].text.strip()})
    return {"response": response.choices[0].text.strip()}
    





# API endpoint to get conversation
@app.get("/conversation")
async def get_conversation():
    global conversation
    return conversation

# API endpoint to clear conversation
@app.delete("/conversation")
async def clear_conversation():
    global conversation
    conversation = Conversation()
    return {"message": "Conversation cleared."}







