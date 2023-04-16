import os
import openai
import re

from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import Engine, Completion, api_key
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

openai.api_key = os.getenv("OPENAI_API_KEY")


class Conversation(BaseModel):
    messages: list = []


class Message(BaseModel):
    message: str


conversation = Conversation()

# Home page


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint to generate response

router = APIRouter()


@app.post("/response")
async def generate_response(data: Message):

    try:
        global conversation
        conversation.messages.append({"user": data.message})

        patterns = [
            r".*python\b",
            r".*golang\b",
            r".*javascript\b",
            r".*java\b",
        ]

        if not any(re.search(keyword, data.message, re.IGNORECASE) for keyword in patterns):
            response_text = "Please ask me a programming-related question."
            conversation.messages.append({"bot": response_text})
            return {"response": response_text}

        else:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{Message}\n\nResponse:",
                temperature=0.5,
                max_tokens=1024,
                n=1,
                stop=None,
                frequency_penalty=0,
                presence_penalty=0
            )

        conversation.messages.append({"bot": response.choices[0].text.strip()})
    except openai.error.RateLimitError as e:
        return {"response": "I'm sorry, I'm having trouble connecting to the server. Please try again later."}
    return {"response": response.choices[0].text.strip()}


# API endpoint to get conversation
router = APIRouter()


@app.get("/conversation")
async def get_conversation():
    global conversation
    return conversation

# API endpoint to clear conversation

router = APIRouter()


@app.delete("/conversation")
async def clear_conversation():
    global conversation
    conversation = Conversation()
    return {"message": "Conversation cleared."}
