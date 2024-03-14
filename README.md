# ollama-rag

Local LLM that can access specific and specialized knowledge it otherwise doesn't have access to. Data is derived from urls or pdf files that you provide, and stored as a RAG in a Postgres vector db. It can output to the command line, or to a web ui via streamlit or gradio. The embeddings are permanently stored in the db so the knowledge is persistent and permanently available.

=========

This is an ongoing work in progress and proof of concenpt, it might be broken. You might have to troubleshoot it, google answers etc, to get it to run. It is meant for experimentation and will change over time as I add more to it.

=========

The basic implementation:

4. Install python
   `sudo apt-get install python3`
   Check version / verify installation:
   `python3 --version`
1. Install Ollama
   `curl -fsSL https://ollama.com/install.sh | sh`
   A. add a coding model (I used mistral-openorca)
   `ollama pull mistral-openorca`
   B. add 'nomic-text-embed' (greatly increaes the token context window)
   `ollama pull nomic-embed-text`
   C. run list command to ensure models are available
   `ollama list`
1. Install Docker Engine or Docker Desktop:
   `https://docs.docker.com/engine/install/`

1. clone this repo
   A. install all from requirements.txt
   `pip install -r requirements.txt`
   B. compose the docker file
   I used a generic postgres/postgres name/pw. Can be changed in the compose yml file
   C. run the python apps:
   app1.py - command line only, you need to add your updates manually to the code to change the urls and search questions
   app2.py - gradio ui version

=========

Next Steps:

Implement the vectordb from postgres so it does something

Implement the pypdf library so that pdf's can be used for updating the llm knowledge base

Implement the streamlit ui version

Dockerize the entire app to simplify installs for people

Implement additional function calling to enhance the usefulness

Add option to choose any models available in your ollama install instead of manually assigning one in the code
