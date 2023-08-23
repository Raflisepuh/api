# Menggunakan Node.js versi LTS sebagai dasar
FROM node:14

# Membuat direktori aplikasi di dalam gambar
WORKDIR /app

# Menyalin package.json dan package-lock.json ke dalam direktori kerja
COPY package*.json ./

# Menginstal dependensi
RUN npm install

# Menyalin seluruh sumber kode aplikasi ke dalam gambar
COPY . .

# Mengekspos port yang akan digunakan oleh aplikasi
EXPOSE 3000

# Menjalankan aplikasi saat kontainer dimulai
CMD ["node", "app.js"]
