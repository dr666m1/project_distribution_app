FROM python:3.8-slim

WORKDIR /build

ENV UID="5000"
ENV GID="5000"
ENV USER="app"

COPY . .

RUN addgroup --gid $GID app && \
    adduser --quiet app --uid $UID --gid $GID --home /home/$USER

USER $UID

RUN pip install --no-cache-dir --user -r ./requirements.txt

WORKDIR /home/$USER
ENV PATH=$PATH:/home/$USER/.local/bin

ENTRYPOINT ["streamlit", "hello"]
