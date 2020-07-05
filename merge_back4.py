from PyPDF2 import PdfFileMerger

pdfs = [['./out/4x4_collate'+str(x+1)+'.pdf','./out/4x4_merged'+str(x+1)+'.pdf'] for x in range(29)]



back='./out/back_print_4x4.pdf'

for pdf in pdfs:
    merger = PdfFileMerger()
    merger.append(pdf[0])
    merger.append(back)
    merger.write(pdf[1])
    merger.close()
merger = PdfFileMerger()
for pdf in pdfs:

    merger.append(pdf[1])
merger.write('./out/set4.pdf')
merger.close()
