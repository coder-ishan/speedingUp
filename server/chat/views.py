import os
import openai
from PyPDF2 import PdfReader
from django.http import JsonResponse
from rest_framework.views import APIView
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class PDFUploadView(APIView):
    def post(self, request):
        documents = request.FILES.getlist('documents')
        query = request.data.get('query')

        # Extract text from PDFs
        extracted_text = ""
        for document in documents:
            pdf_reader = PdfReader(document)
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

        # Split the text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        text_chunks = text_splitter.split_text(extracted_text)

        # Create vector embeddings
        embeddings = OpenAIEmbeddings()
        vector_storage = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

        # Create conversation chain
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_storage.as_retriever(),
            memory=memory
        )

        # Process the query
        response = conversation({'question': query})
        chat_history = response['chat_history']

        return JsonResponse({'chat_history': chat_history}, safe=False)
