from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import io
import os
import re

def pdf_to_text(file):
    fp = open(file, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    print(type(retstr))
    codec = 'utf-8'
    laparams = LAParams()
    #device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    data = ""
    page_no = 0
    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        if pageNumber == page_no:
            interpreter.process_page(page)
            data = retstr.getvalue()
            break

        page_no += 1


    # In[3]:


    get_index = data.split("\n").index('Abstract- ')


    # In[4]:


    final_data = "".join(data.split("\n")[get_index:])


    # In[5]:


    dataSplit = re.split("(?<!\d)[.](?!\d)", final_data)


    # In[6]:


    modified = []
    for x in map(str.lstrip, dataSplit):
        modified.append(x)


    # In[7]:


    start = ''
    for word in modified:
        if word.startswith('Abstract'):
            start = modified.index(word)
            break


    # In[8]:


    end = ''
    for word in modified:
        if word.startswith('Keywords'):
            end = modified.index(word)
            break


    # In[9]:


    x = '\n'.join(dataSplit[start:end])


    # In[10]:


    f = open("input-file.txt", "w",encoding='utf-8')
    f.write(x)
    f.close()
