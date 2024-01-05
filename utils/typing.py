from typing import TypedDict


class InvoiceFields(TypedDict):
    RECEIVER_NAME: str
    VENDOR_NAME: str
    PO_NUMBER: str
    TOTAL: str
