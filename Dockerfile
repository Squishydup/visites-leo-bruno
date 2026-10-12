# Dockerfile volontairement naïf : il sera amélioré dans un TP suivant
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
