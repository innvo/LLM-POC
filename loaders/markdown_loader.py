from langchain.document_loaders import UnstructuredMarkdownLoader
markdown_path = "./README.md"
loader = UnstructuredMarkdownLoader(markdown_path)
data = loader.load()

print(data)