import os
from some_library_for_indexing import GPTSimpleVectorIndex, PromptHelper, LLMPredictor, SimpleDirectoryReader, ChatOpenAI

def construct_index(directory_path):
    if os.path.exists('index.json'):
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        return index

    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=.3, model_name="gpt-3.5-turbo-16k-0613", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')
    return index
