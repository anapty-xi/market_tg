FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot/

CMD ["python3", "run_bot.py"]