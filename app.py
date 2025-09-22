import streamlit as st # it is used to change our code in web apps
import PyPDF2 # to read a pdf file
from docx import Document  #to read word files
from sklearn.feature_extraction.text import CountVectorizer  #convert text to numbers
from sklearn.metrics.pairwise import cosine_similarity  # calculate similarity if any
import re  #to clean texts
import base64



def set_bg_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call at the top
set_bg_local("bg.jpg")



st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #34495e;'>Upload your resume and job description to check match score and missing skills.</p>", unsafe_allow_html=True)

st.markdown("""
<style>
div.stButton > button {
    background-color: #3498db;
    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 0.5em 1.5em;
    font-weight: bold;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #2980b9;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)




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
            st.session_state["logged_in"] = True
            st.success("logged_in succesfully")

        else:
            st.error("login failed")
        
      

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
    return " ".join(words)  # returns splitted words into a string with a single space

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

            resume_words=set(resume_text.split())

            jd_words=set(jd_clean.split())   #to split into words

            missing_keywords=jd_words-resume_words  # find missing words
            
            st.write(f"score: {round(score*100,2)}%")

            st.write("Missing Keywords:", ", ".join(missing_keywords))

        else:

            st.warning("please upload a resume and enter a job description")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Analyzer"])
    
if st.session_state["logged_in"]:
    resume_analayzer()
else:   
    login()





