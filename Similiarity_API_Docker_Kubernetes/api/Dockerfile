FROM python:3
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD ["python","sim.py"]