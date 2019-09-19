FROM python:slim
WORKDIR /app
COPY . .
RUN easy_install spacy
RUN pip install flask \
    flask_restful \
    boto3 \
    pymongo
RUN python -m spacy download en_core_web_sm
CMD ["python","sim.py"]