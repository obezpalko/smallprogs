import pdfreader


def main():
    fd = open('/home/alexbe/Downloads/חולים_ביישובים_מעל_5,000_תושבים_pdf_pdf.pdf', "rb")
    doc = pdfreader.PDFDocument(fd)
    all_pages = [p for p in doc.pages()]
    print(doc)
    print(len(all_pages))
    viewer = pdfreader.SimplePDFViewer(fd)
    viewer.navigate(1)
    viewer.render()
    print(viewer.canvas.strings)


if __name__ == '__main__':
    main()
