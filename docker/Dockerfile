FROM python:3.8

WORKDIR /build

COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["streamlit", "hello"]
