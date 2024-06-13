from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

from .models import *

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)


def index(request):
    login_cookies = request.COOKIES.get('login', 'None')
    if login_cookies != 'None':
        talk_items = TalkItem.objects.filter(user=login_cookies)
        prev_questions = []
        prev_results = []
        for item in talk_items:
            prev_questions.append(item.question)
            prev_results.append(item.answer)
    else:
        if 'prev_questions' not in request.session:
            request.session['prev_questions'] = []
            request.session['prev_results'] = []

        prev_questions = request.session['prev_questions']
        prev_results = request.session['prev_results']

    if prev_questions:
        data = {
            'data': zip(prev_questions, prev_results),
            'login_cookies': login_cookies,
        }
    else:
        data = {'data': None}

    return render(request, 'selfchatgpt/index.html', data)

@csrf_exempt
def chat(request):
    login_cookies = request.COOKIES.get('login', 'None')
    query = request.POST.get('query')
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=1.0, max_tokens=200)
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="answer",
                                      return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory,
                                               return_source_documents=True, output_key="answer")
    result = qa.invoke(query)

    context = {
        'question': query,
        'result': result["answer"]
    }
    if login_cookies != 'None':
        try:
            TalkItem.objects.create(user=login_cookies, question=query, answer=result["answer"])

        except Exception as e:
            print(e)
    else:
        if 'prev_questions' in request.session:
            request.session['prev_questions'] += [query]
            request.session['prev_results'] += [result["answer"]]
        else:
            request.session['prev_questions'] = []
    return JsonResponse(context)


def sessionClear(request):
    request.session.clear()
    return redirect('selfchatgpt:index')
