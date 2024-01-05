import json
from collections import defaultdict

import tiktoken


def retrieve_text_blocks(blocks: list) -> list:
    """
    Retrieve text blocks from ocr output.
    """
    return [block for block in blocks if "Text" in block]


def get_text_from_blocks(blocks: list, max_block_length=100) -> str:
    """
    Retrieve text from ocr text blocks.
    """
    return "\n".join(
        [block["Text"] for block in blocks if len(block["Text"]) < max_block_length]
    )


def get_text_from_ocr_output(file_path: str) -> str:
    """
    Retrieve text from ocr output.
    """
    with open(file_path, "r", encoding="utf-8") as file_content:
        ocr_prediction = json.load(file_content)

    textract_prediction_blocks = ocr_prediction["Blocks"]
    text_blocks = retrieve_text_blocks(textract_prediction_blocks)
    text_blocks_by_page = get_text_from_blocks(text_blocks)
    return text_blocks_by_page


def group_blocks_by_page(
    text_blocks: list,
) -> dict[int, list]:
    """
    Group textract prediction blocks by page number.
    """
    predictions_by_page = defaultdict(list)
    for text_block in text_blocks:
        page_number = text_block["Page"]
        predictions_by_page[page_number].append(text_block)
    return predictions_by_page


def get_textract_predictions_by_page(
    textract_predictions: dict[str, list]
) -> dict[int, list]:
    """
    Retrieve the textract predictions for a given attachment, grouped by page.
    """
    textract_prediction_blocks = textract_predictions["Blocks"]
    text_blocks = retrieve_text_blocks(textract_prediction_blocks)
    return group_blocks_by_page(text_blocks)


MAX_TOKEN_LIMIT_FOR_CLASSIFICATION = 4000


def is_terms_and_conditions_page(page_text: str) -> bool:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(page_text)
    return len(tokens) > MAX_TOKEN_LIMIT_FOR_CLASSIFICATION


def ocr_prediction_without_terms_and_conditions(
    ocr_prediction_by_page: dict[int, list]
) -> str:
    """
    Retrieve the ocr prediction without terms and conditions.
    """
    filtered_ocr_prediction = ""
    for page in ocr_prediction_by_page:
        page_text = get_text_from_blocks(ocr_prediction_by_page[page])
        if not is_terms_and_conditions_page(page_text):
            filtered_ocr_prediction += page_text
    return filtered_ocr_prediction


def get_filtred_text_from_ocr_output(file_path: str) -> str:
    """
    Retrieve text from ocr output.
    """
    with open(file_path, "r", encoding="utf-8") as file_content:
        ocr_prediction = json.load(file_content)

    textract_predictions_by_page = get_textract_predictions_by_page(ocr_prediction)
    filtered_ocr_prediction = ocr_prediction_without_terms_and_conditions(
        textract_predictions_by_page
    )
    return filtered_ocr_prediction
