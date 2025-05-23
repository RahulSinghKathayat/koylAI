import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Koyl AI", layout="centered")
st.title("Koyl AI: Nutrition Advisor")

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("Start the Model"):
        st.session_state.started = True
        st.rerun()
    st.stop() 



load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


try:
    model = ChatGroq(
        model="Meta-Llama/Llama-4-Scout-17b-16e-Instruct",
        groq_api_key=groq_api_key
    )
except Exception as e:
    st.error(f" Failed to load ChatGroq model: {e}")
    st.stop()

embedding = HuggingFaceEmbeddings(model_name='avsolatorio/GIST-small-Embedding-v0')

@st.cache_resource
def load_vectorstore():
    try:
        vs = FAISS.load_local(
            "faiss_index",
            embeddings=embedding,
            allow_dangerous_deserialization=True
        )
        return vs
    except Exception as e:
        st.error(f" Failed to load FAISS index: {e}")
        return None

vectorstore = load_vectorstore()
if vectorstore is None:
    st.stop()

retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_template("""
You are a nutrition AI assistant that gives dietary recommendations based on peer-reviewed research. 

Given a patient's health condition(s) and allergy profile, provide specific and research-backed nutrition advice.
Use only medically accurate, peer-reviewed information. Cite nutritional reasoning if available.

Patient Condition(s): {condition}
Allergies: {allergies}

Context from medical literature:
{context}

What are the best dietary recommendations for this patient?
""")

document_chain = create_stuff_documents_chain(llm=model, prompt=prompt)


st.title("Provide your symptoms and allergies from dairy products")

condition = st.text_input("Enter patient condition(s):", placeholder="e.g., high blood pressure, diabetes")
allergies = st.text_input("Enter allergy profile:", placeholder="e.g., dairy, gluten")

if st.button("Get Dietary Recommendations"):
    if not condition or not allergies:
        st.warning(" Please fill in both condition and allergy fields.")
        st.stop()

    query = f"{condition} {allergies}"

    with st.spinner(" Retrieving relevant documents..."):
        retrieved_docs = retriever.invoke(query)

    with st.spinner(" Generating dietary recommendations..."):
        response = document_chain.invoke({
            "condition": condition,
            "allergies": allergies,
            "context": retrieved_docs
        })

    st.markdown("##  Dietary Recommendation")
    st.write(response)
