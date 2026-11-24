FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 HOME=/tmp MPLCONFIGDIR=/tmp/matplotlib
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py narrativa.md global_power_plant_database.csv ./
USER 10001:10001
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.headless=true", "--server.port=8501"]
