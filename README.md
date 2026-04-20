# AI Travel Planner Chatbot

Backend: Flask + OpenAI fine-tuned model. Data prep from CSVs. Frontend: Angular (drop-in files included).

## Prerequisites
- Python 3.9+
- Node 18+ and Angular CLI (for frontend)

## Setup

1. Create virtualenv and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY and (optionally) FINE_TUNED_MODEL
```

3. Add CSVs to `data/` with columns (free-form allowed):
- query, Budget, City, Trip_type, interest, Duration

4. Merge CSVs and build JSONL:
```bash
python prepare_merge_csvs.py
python prepare_jsonl.py
```

5. Fine-tune (legacy OpenAI CLI, works with openai<1.0):
```bash
# prepare
openai tools fine_tunes.prepare_data -f travel_dataset.jsonl
# create job
openai api fine_tunes.create -t "travel_dataset_prepared.jsonl" -m gpt-3.5-turbo
```
Note the returned model id and put it into `.env` as `FINE_TUNED_MODEL`.

6. Run backend:
```bash
python app.py
# Flask will run at http://127.0.0.1:5000
```

7. Use Angular frontend (drop-in):
- Copy `angular/src/app/chat.service.ts` and the `angular/src/app/chatbot/` folder into your Angular app under `src/app/`
- In your `app.module.ts` import `HttpClientModule` and `FormsModule`, and declare `ChatbotComponent`
- Add `<app-chatbot></app-chatbot>` somewhere in your template
- Start Angular app:
```bash
npm install
ng serve
# Angular at http://localhost:4200
```

CORS is enabled on Flask so the Angular app can call `http://127.0.0.1:5000/chat`.

## Notes
- Requirements pin `openai<1.0.0` to keep legacy API used in `app.py`.
- Update `FINE_TUNED_MODEL` via `.env` without changing code.