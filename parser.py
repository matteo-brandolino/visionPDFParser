from abc import ABC
from typing import Iterator

from cat.mad_hatter.decorators import hook
from cat.looking_glass.cheshire_cat import CheshireCat

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseBlobParser
from langchain.document_loaders.blob_loaders.schema import Blob

from openai import OpenAI

from .utils.helper import clear_images, read_images, split_pdf

class VisionPDFParser(BaseBlobParser, ABC):
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        clear_images()
        with blob.as_bytes_io() as file:
            result = split_pdf(file)
            if (result):
                images = read_images()
                content = ""
                ccat = CheshireCat()
                settings = ccat.mad_hatter.get_plugin().load_settings()
                client = OpenAI(
                    api_key=settings['open_ai_api_key']
                )
                for img in images:
                    messages = [
                        {"role": "system",
                            "content": settings['system_prompt']},
                        {"role": "user", "content": [
                            {"type": "text", "text": settings['user_prompt']},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/png;base64,{img}"}}
                        ]}
                    ]
                    response = client.chat.completions.create(
                        model="gpt-4.1",
                        messages=messages,
                        temperature=0,
                        max_tokens=1000,
                    )
                    content += response.choices[0].message.content + "\n"
                clear_images()
                yield Document(page_content=content, metadata={})
            clear_images()

@hook
def rabbithole_instantiates_parsers(file_handlers: dict, cat) -> dict:
    new_handlers = {
        "application/pdf": VisionPDFParser(),

    }
    file_handlers = file_handlers | new_handlers
    return file_handlers
