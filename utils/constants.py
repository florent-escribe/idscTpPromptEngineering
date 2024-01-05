COMPANY_NAME_MATCHING_PROMPT = """
You are an intelligent entity matcher for company names.
I will give you two strings containing company names and you will tell me if you think it is the same company.
For example: - “Company LTD” is the same as  “Company Limited”, “CIAN.033.MSI” is the same as “CIAN-033-MSI”, etc.
There might be some characters omitted or incorrectly recognized during the OCR, so don't expect an exact match.
When I send you the two strings, you will reply with one word: "same" or "different".
Only send 1 word in response.
Here are the names:
"""

AMOUNT_MATCHING_PROMPT = """
You are an intelligent entity matcher for amounts.
I will give you two amounts coming from an invoice and a purchase order and you will tell me if the invoice amount is valid.
An invoice amount is valid if it is smaller than the purchase order amount, or equal to the purchase order amount.
Do not pay attention to the amounts format. For example: - “12.0” is the same as “12”, “12'000.00” is the same as “12000”, etc.
When I send you the two numbers, you will reply with one word: "valid" or "defect".
Only send 1 word in response.
Here are the amounts:
"""
