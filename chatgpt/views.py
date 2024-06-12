from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.urls import reverse
from django.utils import timezone

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory , ChatMessageHistory 
from langchain.schema import Document

import pandas as pd
import json



# Create your views here.

# Chroma 데이터베이스 초기화 - 사전에 database가 완성 되어 있다는 가정하에 진행 - aivleschool_qa.csv 내용이 저장된 상태임
embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002")
database = Chroma(persist_directory = "./database", embedding_function = embeddings)

def index(request):
    return render(request, 'gpt/index.html')

def chat(request):
    query = request.POST.get('question')

    # chatgpt API 및 lang chain을 사용을 위한 선언
    chat = ChatOpenAI(model="gpt-3.5-turbo")

    # 세션에서 대화 기록 가져오기
    conversation = request.session.get('conversation', [])

    # 대화 기록에 사용자의 질문 추가
    conversation.append({"role": "user", "content": query})

    # 현재 질문을 체인에 추가
    retriever = database.as_retriever(search_kwargs={"k": 3})
    qa = RetrievalQA.from_llm(llm=chat, retriever=retriever, return_source_documents=True)
    result = qa(query)

    # 대화 기록에 대답 추가
    conversation.append({"role": "ai", "content": result["result"]})

    # 세션에 대화 기록 저장
    request.session['conversation'] = conversation

    # result.html에서 사용할 context
    context = {
        'question': query,
        'result': result["result"]
    }

    return render(request, 'gpt/result.html', context)
