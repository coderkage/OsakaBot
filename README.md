# OsakaBot

![OsakaBot](https://github.com/coderkage/OsakaBot/blob/main/img/Screenshot%202025-03-10%20025014.png)

OsakaBot is a fun chatbot inspired by the ["sata andagi" meme](https://youtu.be/QEarTWhsL44?si=EwMIVKLeo_kaIAvb) from [Azumanga Daioh](https://www.imdb.com/title/tt0339955/), featuring Osaka's unique personality and quotes. This bot uses Retrieval-Augmented Generation (RAG) to generate responses based on Osaka’s dialogue.

## Features
- **RAG-based Chatbot**: Uses Retrieval-Augmented Generation to provide Osaka-style responses.
- **Quote Database**: Retrieves and generates responses from a collection of Osaka's quotes.
- **Lightweight & Fast**: Optimized for local deployment with minimal dependencies.

## Usage

Access the streamlit app : [Osakabot](https://osakabot.streamlit.app/) for usage.

![OsakaBot](https://github.com/coderkage/OsakaBot/blob/main/img/Screenshot%202025-03-08%20020942.png)
![OsakaBot](https://github.com/coderkage/OsakaBot/blob/main/img/Screenshot%202025-03-08%20022059.png)

## Configuration
- Modify the `osaka_quotes.json` file and create FAISS vector database using `quotes_faiss.py` to add more Osaka quotes.
- Customize the retrieval pipeline in `app.py` to tweak response generation.

## Future Enhancements
- Improve quote retrieval accuracy.
- Add voice synthesis for Osaka-style speech.
- Deploy as a Telegram/Discord bot.

## Contributions
- Pull requests are welcome! Please follow the existing code style and add relevant documentation.
