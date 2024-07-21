import os

TOGETHER_API_KEY = '9e9eecb88b9ea4f2d83d1a8bcd37caf6656c2d599cab02baf09ef6d96685914e'
os.environ['TOGETHER_API_KEY'] = TOGETHER_API_KEY
os.environ['OPENAI_API_KEY'] = 'sk-None-YooJu1Nf3u9MKjvbct01T3BlbkFJQtdfVox3UiITzuMoJaLp'

ROOT_DIR = os.path.join(os.path.abspath(os.curdir), 'RAG_summary')
SPLITTER_CHUNK_SIZE = 1024