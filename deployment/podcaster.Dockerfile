FROM python:3.10

RUN apt-get update -yq && \
    apt-get install -yq --no-install-recommends \
    libsndfile1 espeak

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME
RUN --mount=type=secret,id=ssh_private_key,mode=0444,required=true \
    mkdir $HOME/.ssh && \
    cp /run/secrets/ssh_private_key $HOME/.ssh/id_ed25519 && \
    chmod 400 $HOME/.ssh/id_ed25519

COPY --chmod=400 --chown=user deployment/ssh_known_hosts.txt $HOME/.ssh/known_hosts

# For local development, use the COPY. Else, use git clone
RUN git clone git@github.com:DonatasTamosauskas/make-a-pod.git
#COPY --chown=user . ./make-a-pod

WORKDIR $HOME/make-a-pod
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1
RUN poetry install -E TTS --no-root && \
    poetry run pip install --upgrade numpy==1.23.5  # In conflict with coqui-tts 1.17.8 requirement, but required to work

WORKDIR $HOME/make-a-pod
ENV PYTHONPATH=$HOME/make-a-pod

CMD ["poetry", "run", "python", "-m", "app.audio_gen"]
