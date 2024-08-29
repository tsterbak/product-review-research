# product-review-research
An AI webapp build with promptmage to provide in-depth analysis for products by researching trustworthy online reviews.

## Getting Started

### Prerequisites

- Python 3.11 or higher

### Installation

1. Clone the repo
   ```sh
   git clone
   ```

2. Install poetry
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Source: https://python-poetry.org/docs/#installing-with-the-official-installer

3. Install dependencies
    ```sh
    poetry install
    ```

4. Run the app with promptmage
    ```sh
    poetry run promptmage run src/app.py
    ```

5. Open the app frontend in your browser
    ```sh
    index.html
    ```

6. Work with the promptmage gui
    ```sh
    http://localhost:8000/gui/
    ```

## Usage

1. Enter the product name in the search bar
2. Click on the search button
3. Wait for the analysis to complete
4. View the analysis results