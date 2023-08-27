FROM python:3.10

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir $HOME/make-a-pod

RUN --mount=type=secret,id=ssh_private_key,mode=0444,required=true \
    mkdir $HOME/.ssh && \
    cp /run/secrets/ssh_private_key $HOME/.ssh/id_ed25519 && \
    chmod 400 $HOME/.ssh/id_ed25519

COPY --chmod=400 --chown=user deployment/ssh_known_hosts.txt $HOME/.ssh/known_hosts
RUN git clone git@github.com:DonatasTamosauskas/make-a-pod.git

WORKDIR $HOME/make-a-pod
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1
RUN poetry install --no-root

WORKDIR $HOME/make-a-pod
ENV PYTHONPATH=$HOME/make-a-pod

EXPOSE 7860

CMD ["poetry", "run", "python", "-m", "app.ui"]
