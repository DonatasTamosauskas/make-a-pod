---
title: make-a-podcast
emoji: 🎙️
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# make-a-pod 🎙️
Welcome to this little project, make-a-pod! This pet project uses the magic of 
Text-to-Speech (TTS) 🗣️ to convert Internet articles into podcasts 🎧. Very useful 
if you, like me, sometimes prefer to listen rather than read!

## Table of Contents
- 🏗️ The Tool
- 🧰 What You'll Need
- 🎬 Getting Started
- ✍️ Contributions
- 📜 License

## 🏗️ The Tool
make-a-pod is made up of two parts:
- article uploading UI (built with Gradio) 🖥️ 
- and a TTS service 🗣️ that does the heavy lifting of converting article text to speech.

You can find the output, an actual podcast, on Spotify over at 
[make-a-pod](https://podcasters.spotify.com/pod/show/make-a-podcast).

## 🧰 What You'll Need
To dive in, you'll need a couple of tools:

Docker (for the Gradio UI & TTS services)
An SSH Key for your GitHub repo (as git is used in place of a DB) placed in 
`deployment/ssh_key.txt` 🔐

## 🎬 Getting Started
### Launching the Article Collection Gradio UI
With Docker 🐳 all set and your GitHub SSH key in place, go ahead and launch the 
Gradio UI using Docker Compose:
```shell
docker-compose up ui
```
You'll be able to access the UI at [http://localhost](http://localhost)

### Record Your Next Podcast 🎙️
The TTS service can now be called into action. All uploaded articles will be transformed 
into podcast-ready audio 🎧 on running:
```shell
docker-compose run podcaster
```

## ✍️ Contributions
Got some bright ideas 💡? Contributions are always welcome!

## 📜 License
make-a-pod is released under the MIT license. For the specifics, check out
LICENSE in the repository.

And that's it, folks! Happy Podcast Crafting! 🎙️🚀
