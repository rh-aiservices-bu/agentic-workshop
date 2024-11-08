# calendar-api

A simple calendar API powered by FastAPI.

## Architecture

```md
- database
	- build.py
	- database_handler.py
- server
	- method.py
	- server.py
- client
	- client.py
```

## Usage

2. Install Python packages: `fastapi` and `uvicorn`
3. Run `python build.py` to create a SQLite database (only run for the first time)
4. Run `uvicorn server:app --reload --host 127.0.0.1 --port 8000 --workers 4 --limit-concurrency 100 --timeout-keep-alive 5`
5. Run test code in `client.py`, or try it out on `http://127.0.0.1:8000/docs`
