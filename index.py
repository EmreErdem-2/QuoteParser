
from llama_parse import LlamaParse  # pip install llama-parse
import mdutils

parser = LlamaParse(
    api_key=apiKey,  # you will need an API key, get it from https://cloud.llamaindex.ai/
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True
)
parsed_documents = parser.load_data("./LeninMarxOnMigration.pdf")
mdFile = mdutils(file_name='TestMarkdown')
mdFile.create_md_file()
mdFile.write(documents)
# Save the parsed results
with open('parsed_output.md', 'w', encoding="utf-8") as f:
    for doc in parsed_documents:
        f.write(doc.text + '\n')
