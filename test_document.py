from pytex import Document, Section, CodeSnippet



if __name__ == '__main__':

    fnm = 'test_document'
    code = CodeSnippet(['x = {"key" : "value"}','print("hello world")'],language='Python')
    text = [Section('A Section',['line 1','line 2']),code]
    doc = Document(fnm)
    doc.add(text)
    doc.set_title('Test document','pytex (Zane Jakobs)',True)
    output = doc.compile().stdout
    print(f"stdout from compile:\n {output}")
    
