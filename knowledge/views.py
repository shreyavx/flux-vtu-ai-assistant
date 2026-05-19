from django.shortcuts import render, redirect

from .forms import DocumentForm

from .utils import extract_text_from_pdf

from .models import DocumentChunk

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .llm import (ask_llm, is_rag_question)

from .utils import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from .vectordb import (
    create_embedding,
    store_embedding
)

@csrf_exempt
def upload_document(request):

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save()

            pdf_name = document.file.name

            pdf_path = document.file.path

            text = extract_text_from_pdf(pdf_path)

            chunks = split_text_into_chunks(text)

            for chunk in chunks:

                embedding = create_embedding(chunk)

                embedding_id = store_embedding(
                    chunk,
                    embedding,
                    pdf_name
                )

                chunk_obj = DocumentChunk.objects.create(
                    document=document,
                    chunk_text=chunk,
                    embedding_id=embedding_id
                )

            print("EMBEDDINGS STORED")

            print(text)

            return JsonResponse({
                "message": "PDF uploaded successfully!"
            })

    else:

        form = DocumentForm()

    return render(
        request,
        'knowledge/upload.html',
        {'form': form}
    )

from django.http import JsonResponse

from .vectordb import (
    create_embedding,
    search_similar_chunks
)

def ask_question(request):

    print("ASK FUNCTION HIT")

    if request.method == "POST":

        print(request.POST)

        question = request.POST.get("question")


        if is_rag_question(question):

            search_results = search_similar_chunks(question)

            context = search_results["context"]

            sources = search_results["sources"]


            prompt = f"""
            You are a concise VTU AI assistant.

            Use ONLY relevant academic information
            from the context.

            Ignore unrelated formatting text,
            headers, instructions,
            symbols, or corrupted PDF content.

            Keep answers concise and clean.

            Context:
            {context}

            Question:
            {question}
            """

            print(prompt)
            print("REACHED LLM")

            answer = ask_llm(prompt)


        else:

            sources = []

            prompt = f"""
            You are a concise AI assistant.

            Keep responses brief.

            User:
            {question}
            """

            answer = ask_llm(prompt)

        return JsonResponse({
                "answer": answer,
                "sources": sources
            })

    return JsonResponse({
        "error": "Invalid request"
    })


def chat_page(request):

    return render(
        request,
        "knowledge/chat.html"
    )