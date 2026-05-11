FROM python:3.12-slim

WORKDIR /app

# Install Node for Tailwind build (pymysql is pure Python, no C deps needed)
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json .
RUN npm install

COPY . .

# Build Tailwind CSS
RUN npm run build:css

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
