import pandas as pd
import streamlit as st
from docx import Document
import os
import PyPDF2

st.title('RESUME CLASSIFICATION')


def docx(path):
  doc = Document(path)
  indx=0
  dd=[]
  for para in doc.paragraphs:
    indx+=1
    if(len(para.text)>0):
      dd.append(para.text)
    else:
      continue
  return dd


def pdf(path):
  pdfFileObject = open(path, 'rb')
  pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
  pagefull=[]
  for i in range(pdfReader.numPages):
    pageObjfull=pdfReader.getPage(i)
    pagefull.append(pageObjfull.extractText())
    pagefull=' '.join(pagefull)
    pagefull=pagefull.split()
  return pagefull
	


import pandas as pd
import os
path="C:/Users/sagar/anaconda3/Resumes"
ndocx=[]
ndoc=[]
npdf=[]
n=[]
newpathdocx=[]
newpathdoc=[]
newpathpdf=[]
for filename in os.listdir(path):

    if filename.endswith('.docx'):
        newpathdocx.append(os.path.join(path,filename))
        ndocx.append(filename)

    elif filename.endswith('.doc'):
        newpathdoc.append(os.path.join(path,filename))
        ndoc.append(filename)

    elif filename.endswith('.pdf'):
        newpathpdf.append(os.path.join(path,filename))
        npdf.append(filename)

      
n=ndocx+npdf

extdocx=[]
for i in newpathdocx:
  extdocx.append(docx(i))

extpdf=[]
for i in newpathpdf:
  extpdf.append(pdf(i))



final_extraction=extdocx+extpdf

skill=[]
for i in final_extraction:
  skill.append(" ".join(i))

ff={'NAME':n,'Skills':skill}

df=pd.DataFrame(data=ff)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_df=0.95,min_df=2,stop_words='english')

dtm =  tfidf.fit_transform(df['Skills'])

from sklearn.decomposition import NMF
nmf_model = NMF(n_components=15,random_state=42)
nmf_model.fit(dtm)
nmf_final_model = nmf_model.transform(dtm)
nmf_final_model.argmax(axis=1)
df['Role']=nmf_final_model.argmax(axis=1)


mytopic={0:'Workday',1:'Peoplesoft',2:'Frontend Developer',3:'DBM',4:'Peoplesoft',5:'Frontend Developer',6:'Student',7:'Workday',8:'Peoplesoft',9:'Analyst',10:'Frontend Developer',11:'Frontend Developer',12:'Frontend Developer',13:'Frontend Developer',14:'Analyst'}
df['RoleName']= df['Role'].map(mytopic)


df=df.drop('Skills',axis=1)

df=df.drop('Role',axis=1)

st.header('SELECT YOUR RESUME')
skills=st.selectbox('Resume',df['NAME'])

final_output=df[df['NAME'].values==skills]
st.subheader("DESIGNATION")
df1=st.write(final_output['RoleName'])

st.sidebar.header('USER_SELECT')
df2=st.sidebar.selectbox('DESIGNATION',('Workday','Peoplesoft','Frontend Developer','DBM','Peoplesoft','Student','Analyst'))



def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image:url(https://images.unsplash.com/photo-1553095066-5014bc7b7f2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8d2FsbCUyMGJhY2tncm91bmR8ZW58MHx8MHx8&w=1000&q=80);
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
       )

add_bg_from_url() 


