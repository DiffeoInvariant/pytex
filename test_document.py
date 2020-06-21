from pytex import Document, Section, CodeSnippet



if __name__ == '__main__':

    fnm = 'test_document'
    code = CodeSnippet(['#!/usr/bin/python3','print("hello world")'],language='Python')
    text = [Section('A Section',['line 1','line 2']),code]
    doc = Document(fnm)
    doc.add(text)
    doc.write()
    
