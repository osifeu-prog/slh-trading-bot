FROM python:3.11-slim

WORKDIR /app

# התקנת dependecies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקוד
COPY . .

# משתנה סביבה לאיפוס buffer
ENV PYTHONUNBUFFERED=1

# הרצת שני התהליכים: ה‑API (uvicorn) וה‑trader
CMD ["sh", "-c", "python run_trader.py & uvicorn main:app --host 0.0.0.0 --port 8080"]
