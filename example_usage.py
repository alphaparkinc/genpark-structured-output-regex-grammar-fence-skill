"""
Demonstration of genpark-structured-output-regex-grammar-fence-skill
"""

from client import OutputGrammarFenceClient

def main():
    fencer = OutputGrammarFenceClient()

    noisy_llm_response = """
    Certainly! Here is the structured summary of the transaction you requested:

    ```json
    {
        "status": "APPROVED",
        "tx_id": "TX_9941_Z",
        "settled_amount": 120.50,
        "currency": "USD"
    }
    ```

    Please let me know if you need additional details!
    """

    data = fencer.extract_json(noisy_llm_response)
    print("=== EXTRACTED CLEAN JSON DATA ===")
    print(f"Transaction ID: {data['tx_id']}")
    print(f"Amount: {data['settled_amount']} {data['currency']}")
    print(f"Valid Schema: {fencer.enforce_schema_keys(data, ['tx_id', 'status'])}")

if __name__ == "__main__":
    main()
