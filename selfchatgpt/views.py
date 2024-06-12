from django.shortcuts import render
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
import json
import os
from django.shortcuts import render
from .models import ChatHistory  # ChatHistory 모델을 임포트합니다

# Chroma 데이터베이스 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)

# 이전 대화 이력을 파일에 저장하고 불러오는 함수
def save_chat_history(chat_history):
    with open('chat_history.json', 'w') as file:
        json.dump(chat_history, file)

def load_chat_history():
    if os.path.exists('chat_history.json'):
        with open('chat_history.json', 'r') as file:
            return json.load(file)
    else:
        return []

# index 뷰 수정
def index(request):
    chat_history = load_chat_history()
    return render(request, 'selfgpt/index.html', {'chat_history': chat_history})

# chat 뷰 수정
def chat(request):
    # post로 받은 question을 가져옴
    user_question = request.POST.get('question')

    # chatgpt API 및 lang chain을 사용을 위한 선언
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    qa = RetrievalQA.from_llm(llm=chat, retriever=retriever, return_source_documents=True)

    # 시스템 응답 생성
    system_response = qa(user_question)["result"]

    # 이전 대화 이력을 업데이트
    chat_history = load_chat_history()
    chat_history.append({'user_question': user_question, 'system_response': system_response})
    save_chat_history(chat_history)

    # result.html에서 사용할 context
    context = {
        'user_question': user_question,
        'system_response': system_response,
        'chat_history': chat_history
    }

    # 응답을 보여주기 위한 html 선택 (위에서 처리한 context를 함께 전달)
    return render(request, 'selfgpt/result.html', context)
