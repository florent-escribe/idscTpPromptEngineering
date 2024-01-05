from openai import OpenAI
import tiktoken

from utils.constants import AMOUNT_MATCHING_PROMPT, COMPANY_NAME_MATCHING_PROMPT


def get_answer_from_simple_prompt(user_prompt: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )
    return completion.choices[0].message.content


MODEL_MAX_CONTEXT_LENGTH = 4000


def truncate_to_token_limitations(text: str, token_limit: int) -> str:
    """
    Truncate text to token limitations of the LLM model.
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)

    current_part = []
    current_count = 0

    for token in tokens:
        current_part.append(token)
        current_count += 1

        if current_count >= token_limit:
            break

    decoded_truncated_tokens = [
        encoding.decode_single_token_bytes(token).decode("utf-8", errors="replace")
        for token in current_part
    ]
    truncated_text = "".join(decoded_truncated_tokens)
    return truncated_text


MODEL_MAX_CONTEXT_LENGTH = 4000


def get_answer_from_elaborate_prompt(system_prompt: str, user_prompt: str) -> str:
    client = OpenAI()
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded_system_prompt = encoding.encode(system_prompt)
    system_prompt_token_count = len(encoded_system_prompt)
    truncated_user_prompt = truncate_to_token_limitations(
        user_prompt, MODEL_MAX_CONTEXT_LENGTH - system_prompt_token_count
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": truncated_user_prompt,
            },
        ],
    )
    return completion.choices[0].message.content


def match_company_name(invoice_result, po_result):
    prompt = COMPANY_NAME_MATCHING_PROMPT
    prompt += f"1: {invoice_result}\n"
    prompt += f"2: {po_result}\n"
    response = get_answer_from_simple_prompt(prompt)
    return response


def match_amount(invoice_result, po_result):
    prompt = AMOUNT_MATCHING_PROMPT
    prompt += f"invoice amount : {invoice_result}\n"
    prompt += f"purchase order amount : {po_result}\n"
    response = get_answer_from_simple_prompt(prompt)
    return response
