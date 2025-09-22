import streamlit as st # it is used to change our code in web apps
import PyPDF2 # to read a pdf file
from docx import Document  #to read word files
from sklearn.feature_extraction.text import CountVectorizer  #convert text to numbers
from sklearn.metrics.pairwise import cosine_similarity  # calculate similarity if any
import re  #to clean texts


USER_CREDENTIALS ={
    "admin" : "1234",
    "test"  : "abcd"
}


def login():
    st.title("login page")
    username=st.text_input("enter your user name")
    password=st.text_input("password ",type="password")

    if st.button("login"):

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]==password:
            st.session_state("logged in") = True
            st.success("logged in succesfully")

        else:
            st.error("login failed")
        
        if "logged in" not in st.session_state:
            st.session_state["logged in"] = False

        if st.session_state["logged in"]:
            resume_analayzer()
        
        else:   

            login()


def read_resume(file):
    text=""

    if file.type == "application/pdf":     # pdf document
        reader=PyPDF2.PdfReader(file)  #opens pdf files

        for page in reader.pages:
            text += page.extract_text()  # extract text from pages and add to text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # word document
        doc = Document(file)  #opens word files

        for para in doc.paragraphs:
            text += para.text+" "    # adds each paragraph by adding pdf and add pdf

    elif file.type=="text/plain":
        text = file.getvalue().decode("uf-8")
        
    return text


def clean_text(text):

    text=text.lower() #converts to lower
    text = re.sub(r"[^a-z\s]","",text)  #remove numbers and punctuation and keep only numbers from a-z and spaces
    words=text.split()  #add words by splitting words
    return "".join(words)  # returns splitted words into a string with a single space

def resume_analayzer():

    st.title("resume analyzer")
    resume_file=st.file_uploader("upload resume (PDF,DOCX,TXT)",type=["pdf","docx","txt"])  # upload only pdf,word,text files
    jd_text=st.text_area("paste job description here") # makw a multi line input to upload jib description
    
    if st.button("analyse"):
        
        if resume_file and jd_text.strip() !="":

            resume_text = read_resume(resume_file)
            resume_text = clean_text(resume_text)  #calling resume_text function for cleaning
            jd_clean = clean_text(jd_text)   #clean input job description


            vectorizer = CountVectorizer()   # counts text into numbers to count how many times a word occurs
            vectors = vectorizer.fit_transform([resume_text,jd_clean]) # Learn the vocabulary of unique words and transform it to numbers

            score = cosine_similarity(vectors[0],vectors[1])[0][0]


    



