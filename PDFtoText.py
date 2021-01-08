from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import PyPDF2
import io
import re


def pdf_to_text(file):
    # fp = open(file, 'rb')
    fp = file.read()
    fileReader = PyPDF2.PdfFileReader(fp)
    print(fileReader.numPages)
    # rsrcmgr = PDFResourceManager()
    # retstr = io.StringIO()
    # laparams = LAParams()
    # device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    #
    # data = ""
    # page_no = 0
    # for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    #     if pageNumber == page_no:
    #         interpreter.process_page(page)
    #         data = retstr.getvalue()
    #         break
    #
    #     page_no += 1
    #
    # get_index = data.split("\n").index('Abstract- ')
    # final_data = "".join(data.split("\n")[get_index:])
    # data_split = re.split("(?<!\d)[.](?!\d)", final_data)
    #
    # modified = []
    # for x in map(str.lstrip, data_split):
    #     modified.append(x)
    #
    # start = ''
    # for word in modified:
    #     if word.startswith('Abstract'):
    #         start = modified.index(word)
    #         break
    #
    # end = ''
    # for word in modified:
    #     if word.startswith('Keywords'):
    #         end = modified.index(word)
    #         break
    #
    # fp.close()
    # return data_split[start:end]
