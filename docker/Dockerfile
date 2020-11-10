FROM python:3.8-slim

ENV UID="5000"
ENV GID="5000"
ENV USER="app"

RUN addgroup --gid $GID app && \
    adduser --quiet app --uid $UID --gid $GID --home /home/$USER

WORKDIR /home/$USER/app

COPY . .

ENV PATH=$PATH:/home/$USER/.local/bin

USER $UID

RUN pip install --no-cache-dir --user -r ./requirements.txt

ENTRYPOINT ["streamlit", "run", "entrypoint.py"]
