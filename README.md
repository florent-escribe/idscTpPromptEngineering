# idscTpPromptEngineering
A training exercise on prompt engineering for the IDSC class of Mines Paris\
Jan 2024

### Context :
You are trying to automate the invoice processing service of a company.\
In data/pdf_documents, there is a dataset of invoices and purchase orders.\
In data/ocr_results, there is the output of Amazon Textract, an OCR system, on those documents.\
Your goal is to determine for each pair of Invoice/PO whether :
- The PO number is the same
- The receiver name is the same
- The vendor name is the same
- The invoice total is lower than the PO number

### Instructions :
1. MODOP: Get your OpenAI API key
    - Go to [https://openai.com/product](https://openai.com/product)
    - Create an account or login with google
    - Fill in personal information
    - ~~Label data~~ Prove you are human
    - Go to [API keys](https://platform.openai.com/api-keys) on the left panel
    - Verify your phone number
    - A window automatically opens to create an API key
    - Give it a name
    - Save it to a local text file
    - Go to [Billing](https://platform.openai.com/account/billing/overview) on the left panel
        - Click *Add payment details*
        - Select *Individual account*
        - Fill in your payment details
        - Ask for the minimum 5$
        - Pay (6$ total with tax)
    - All set !

2. Create a .env file at the root of the project
3. Add 
```
OPENAI_API_KEY="[your api key]"
PYTHONPATH="[the path to your projet]"
```
4. In the terminal, run `source .env`. You can check that it has worked by looking at your environment variables.
5. Create a python virtual environment in the project
6. Install project requirements by running `pip install -r requirements.txt`
7. In notebooks/ open prompt_examples.ipynb and run your first GPT prompts through OpenAI's API.
8. In notebooks/ open extraction_example.ipynb, extract the PO#, receiver/vendor names and total for one document.
9. In notebooks/extraction_on_dataset.ipynb, you will find code that extracts those fields on the whole dataset.
9. In notebooks/ open matching_layout.ipynb, determine for each order if the PO fields match those of the invoice.
10. In notebooks/matching_on_dataset.ipynb, you will find code that matches POs and invoices.
11. Iterate on the prompts to get better results.

