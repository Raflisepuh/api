# Gunakan base image Python
FROM python:3.9

# Set working directory di dalam kontainer
WORKDIR /app

RUN pip install fastapi uvicorn

# Copy dependencies file ke dalam kontainer
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi ke dalam kontainer
COPY . .

# Expose port yang akan digunakan oleh aplikasi
EXPOSE 5000

# Jalankan aplikasi saat kontainer berjalan
CMD ["python", "app.py"]
