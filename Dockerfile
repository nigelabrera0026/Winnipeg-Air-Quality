# Official Python image
FROM python:3.11.10-alpine3.20



# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /wpgair

COPY requirements.txt /wpgair/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Set working directory to where manage.py is located
WORKDIR /wpgair/wpgair

EXPOSE 8000

# RUN python manage.py collectstatic --noinput


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]