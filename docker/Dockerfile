FROM python:3.8-slim

WORKDIR /build

COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["streamlit", "hello"]
