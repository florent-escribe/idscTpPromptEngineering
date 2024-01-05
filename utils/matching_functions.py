from typing import cast

import pandas as pd
from utils.openai_functions import match_amount, match_company_name
from utils.typing import InvoiceFields


def document_extracted_values_df_to_dict(document_df: pd.DataFrame) -> dict[str, str]:
    output_dict = {
        "TOTAL": document_df["total_amount"].values[0],
        "PO_NUMBER": document_df["po_number"].values[0],
        "VENDOR_NAME": document_df["vendor_name"].values[0],
        "RECEIVER_NAME": document_df["receiver_name"].values[0],
    }
    return output_dict


def get_non_matching_fields(
    provider_invoice, purchase_order
) -> dict[str, dict[str, str]]:
    """Matching invoice fields and purchase orders using OpenAI API"""
    vendor_match = match_company_name(
        provider_invoice["VENDOR_NAME"], purchase_order["VENDOR_NAME"]
    )
    receiver_match = match_company_name(
        provider_invoice["RECEIVER_NAME"], purchase_order["RECEIVER_NAME"]
    )
    # match amounts
    amount_match = match_amount(provider_invoice["TOTAL"], purchase_order["TOTAL"])

    # match PO number (exact match)
    po_number_match = (
        "same"
        if provider_invoice["PO_NUMBER"] == purchase_order["PO_NUMBER"]
        else "different"
    )
    # map to boolean
    vendor_match_bool = vendor_match == "same"
    receiver_match_bool = receiver_match == "same"
    amount_match_bool = amount_match == "valid"
    po_number_match_bool = po_number_match == "same"

    non_matching_fields = {}

    if not po_number_match_bool:
        non_matching_fields["PO_NUMBER"] = {
            "provider_invoice": provider_invoice["PO_NUMBER"],
            "purchase_order": purchase_order["PO_NUMBER"],
        }

    if not vendor_match_bool:
        non_matching_fields["VENDOR_NAME"] = {
            "provider_invoice": provider_invoice["VENDOR_NAME"],
            "purchase_order": purchase_order["VENDOR_NAME"],
        }
    if not receiver_match_bool:
        non_matching_fields["RECEIVER_NAME"] = {
            "provider_invoice": provider_invoice["RECEIVER_NAME"],
            "purchase_order": purchase_order["RECEIVER_NAME"],
        }
    if not amount_match_bool:
        non_matching_fields["AMOUNT"] = {
            "provider_invoice": provider_invoice["TOTAL"],
            "purchase_order": purchase_order["TOTAL"],
        }

    return non_matching_fields


def match_po_and_invoice(order_df):
    """
    Detect defects in the dataframe of a single order.
    :param order_df: dataframe containing the order. It should contain 2 lines, one for the invoice and one for the PO.

    :return: dataframe containing the defects, with the following columns:
        - order_path: path to the order
        - PO_NUMBER_DEFECT: True if the PO_NUMBER is not the same in the invoice and the PO
        - AMOUNT_DEFECT: True if the AMOUNT is higher in the invoice than in the PO
        - VENDOR_NAME_DEFECT: True if the VENDOR_NAME is not the same in the invoice and the PO
        - RECEIVER_NAME_DEFECT: True if the RECEIVER_NAME is not the same in the invoice and the PO
    """
    if order_df.shape[0] <= 1:
        return None
    provider_invoice_df = order_df[order_df["file_name"] == "Invoice"]
    purchase_order_df = order_df[order_df["file_name"] == "PO"]

    provider_invoice_as_dict = document_extracted_values_df_to_dict(provider_invoice_df)
    purchase_order_as_dict = document_extracted_values_df_to_dict(purchase_order_df)

    provider_invoice = cast(InvoiceFields, provider_invoice_as_dict)
    purchase_order = cast(InvoiceFields, purchase_order_as_dict)

    non_matching_fields: list[str]
    non_matching_fields = get_non_matching_fields(
        provider_invoice, purchase_order
    ).keys()

    return pd.DataFrame(
        [
            [
                "PO_NUMBER" in non_matching_fields,
                "AMOUNT" in non_matching_fields,
                "RECEIVER_NAME" in non_matching_fields,
                "VENDOR_NAME" in non_matching_fields,
            ]
        ],
        columns=[
            "po_number_defect",
            "amount_defect",
            "receiver_name_defect",
            "vendor_name_defect",
        ],
    )
