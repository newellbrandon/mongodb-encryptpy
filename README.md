# MongoDB with Python Demo

This repository contains demos for using MongoDB with Python. 

## Demos

### 1. Client-Side Field Level Encryption (`csfle/`)

This demo shows how to use MongoDB's Client-Side Field Level Encryption (CSFLE) with Python and PyMongo.

- [`csfle/make_data_key.py`](csfle/make_data_key.py): Script to generate a local master key and create a data encryption key (DEK) in MongoDB.
- [`csfle/insert_encrypted_document.py`](csfle/insert_encrypted_document.py): Script to insert and retrieve documents with encrypted fields using the generated DEK.

## Setup

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Run the CSFLE demo:**

    1. Generate the data key:
        ```sh
        python csfle/make_data_key.py
        ```
    2. Insert and retrieve an encrypted document:
        ```sh
        python csfle/insert_encrypted_document.py
        ```

## License

See [LICENSE](LICENSE) for details.