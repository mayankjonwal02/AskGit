from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from workflow.bot import run_chatbot
import uvicorn
from fastapi.responses import HTMLResponse


app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/bot")
async def bot_endpoint(request: QueryRequest):
    try:
        response = run_chatbot(request.query)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>GitLab Futuristic AI Bot</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                background: linear-gradient(135deg, #0f2027, #2c5364, #232526, #414345);
                min-height: 100vh;
            }
            .neon {
                text-shadow: 0 0 8px #00fff7, 0 0 16px #00fff7, 0 0 32px #00fff7;
            }
            .glow-border {
                box-shadow: 0 0 16px #00fff7, 0 0 32px #00fff7;
            }
            .fade-in {
                animation: fadeIn 1s ease-in;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px);}
                to { opacity: 1; transform: translateY(0);}
            }
            .typing {
                border-right: .15em solid #00fff7;
                white-space: pre-wrap;
                word-break: break-word;
                overflow-wrap: break-word;
                overflow-x: hidden;
                animation: typing 2s steps(40, end), blink-caret .75s step-end infinite;
                max-width: 100%;
            }
            @keyframes typing {
                from { width: 0 }
                to { width: 100% }
            }
            @keyframes blink-caret {
                from, to { border-color: transparent }
                50% { border-color: #00fff7; }
            }
        </style>
    </head>
    <body class="flex flex-col items-center justify-center min-h-screen">
        <div class="w-full max-w-xl p-8 rounded-3xl bg-black/60 shadow-2xl glow-border">
            <h1 class="text-4xl md:text-5xl font-extrabold text-center neon mb-8 tracking-wide fade-in">🤖 GitLab AI Assistant</h1>
            <form id="chat-form" class="flex flex-col gap-4">
                <input id="query" name="query" type="text" placeholder="Ask me anything about GitLab..." required
                    class="w-full px-4 py-3 rounded-xl bg-gray-900 text-white focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all duration-300 text-lg shadow-inner neon"/>
                <button type="submit"
                    class="py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-blue-600 text-white font-bold text-lg shadow-lg hover:scale-105 hover:from-cyan-300 hover:to-blue-500 transition-all duration-300 neon">
                    🚀 Ask
                </button>
            </form>
            <div id="loading" class="hidden flex flex-col items-center mt-8">
                <svg class="animate-spin h-10 w-10 text-cyan-400 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="#00fff7" stroke-width="4"></circle>
                  <path class="opacity-75" fill="#00fff7" d="M4 12a8 8 0 018-8v8z"></path>
                </svg>
                <span class="text-cyan-300 text-lg neon">Thinking...</span>
            </div>
            <div id="answer-container" class="mt-8 fade-in max-w-full overflow-x-auto break-words"></div>
        </div>
        <footer class="mt-8 text-cyan-200 text-sm opacity-60">Powered by FastAPI &amp; Gemini AI</footer>
        <script>
            const form = document.getElementById('chat-form');
            const queryInput = document.getElementById('query');
            const answerContainer = document.getElementById('answer-container');
            const loading = document.getElementById('loading');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                answerContainer.innerHTML = '';
                loading.classList.remove('hidden');
                const query = queryInput.value;
                try {
                    const res = await fetch('/bot', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query })
                    });
                    const data = await res.json();
                    loading.classList.add('hidden');
                    if (data.answer && data.answer.result) {
                        typeText(answerContainer, data.answer.result);
                    } else if (data.answer) {
                        typeText(answerContainer, data.answer);
                    } else if (data.error) {
                        answerContainer.innerHTML = `<div class="text-red-400 neon fade-in">❌ ${data.error}</div>`;
                    } else {
                        answerContainer.innerHTML = `<div class="text-red-400 neon fade-in">❌ Unexpected error.</div>`;
                    }
                } catch (err) {
                    loading.classList.add('hidden');
                    answerContainer.innerHTML = `<div class="text-red-400 neon fade-in">❌ ${err}</div>`;
                }
            });

            function typeText(container, text) {
                container.innerHTML = '';
                let i = 0;
                const span = document.createElement('span');
                span.className = 'text-cyan-200 text-xl neon typing max-w-full break-words';
                container.appendChild(span);
                function type() {
                    if (i < text.length) {
                        span.textContent += text.charAt(i);
                        i++;
                        container.scrollLeft = container.scrollWidth; // auto-scroll if overflow
                        setTimeout(type, 18);
                    } else {
                        span.classList.remove('typing');
                    }
                }
                type();
            }
        </script>
    </body>
    </html>
    """


