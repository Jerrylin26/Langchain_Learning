import tiktoken
from langchain.text_splitter import TokenTextSplitter

doc_str = """The crowd roared as Jake stepped up to the plate, his heart pounding like a drum. The pitcher’s eyes were cold, calculating, as he wound up for the perfect throw. Sweat dripped down Jake’s forehead, but he focused on the ball, imagining the crack of the bat echoing across the empty summer field. The first pitch came fast, too fast—Jake barely managed a swing, sending a foul ball into the bleachers. The tension grew with every pitch. On the third, he adjusted, timing his swing perfectly. The bat connected with a sharp, satisfying crack, and the ball soared high, curving past the outfielders. Cheers erupted as he rounded the bases, adrenaline pumping. This was more than a game; it was the moment he had trained for, dreamed about, and now, living it. Every heartbeat matched the rhythm of the crowd, every step a testament to perseverance. Baseball, he realized, wasn’t just a sport—it was a story written in sweat and courage."""

text_splitter = TokenTextSplitter(
    encoding_name='gpt2',
    chunk_size=12,
    chunk_overlap=0
)

docs = text_splitter.create_documents([doc_str])

token_encoder = tiktoken.get_encoding('gpt2')

for doc in docs:
    print(doc)
    print(f"length: {len(token_encoder.encode(doc.page_content))}")
    print('----------------------')