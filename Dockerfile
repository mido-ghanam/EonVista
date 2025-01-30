# استخدم صورة Python كأساس
FROM python:3.9

# ضبط مجلد العمل
WORKDIR /app

# نسخ الملفات إلى المجلد العامل
COPY . .

# تثبيت المتطلبات
RUN pip install -r requirements.txt

# فتح البورت الذي سيعمل عليه التطبيق
EXPOSE 8000

# تشغيل تطبيق Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
