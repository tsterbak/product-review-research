# product-review-research
An AI webapp build with promptmage to provide in-depth analysis for products by researching trustworthy online reviews.

Developed with PromptMage: https://promptmage.io

![Product Review Research](https://github.com/tsterbak/product-review-research/blob/main/assets/product-review-research.png)

## Getting Started

### Prerequisites

- Docker and docker-compose installed on your machine

### Installation

1. Clone the repo
   ```sh
   git clone
   ```

2. Add .env file to the root of the project and to src/
    ```sh
    # src/.env
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```
    ```sh
    # .env
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

2. Build the docker images and start the containers
    ```sh
    docker-compose up --build
    ```

3. Open the app frontend in your browser
    ```sh
    http://localhost:8080/
    ```

4. Work with the promptmage gui
    ```sh
    http://localhost:8000/gui/
    ```

## Usage

1. Enter the product name in the search bar
2. Click on the search button
3. Wait for the analysis to complete
4. View the analysis results