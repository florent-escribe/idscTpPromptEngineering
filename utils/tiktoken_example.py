import tiktoken


encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens = encoding.encode("Some text to encode")
print(len(tokens))
