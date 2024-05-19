# Marvin virtual assistant

## Description

This project is an open-source first attempt at creating a fully working smart assistant

<!-- ## Features -->
<!---->
<!-- - Speed -->
<!-- - Feature 2: [Description of feature 2] -->
<!-- - Feature 3: [Description of feature 3] -->

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3
- You have a working PostgreSQL database instance with pg_vector extension running

## Installation

To install this project, follow these steps:

1. **Clone the repository**:

    ```sh
    git clone https://github.com/SDAPlatform/Marvin
    ```

2. **Navigate to the project directory**:

    ```sh
    cd Marvin
    ```

3. **Create a virtual environment using `venv`**:

    ```sh
    python3 -m venv venv
    ```

4. **Activate the virtual environment**:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

5. **Create a `.env` file with the following keys**:

    Create a file named `.env` in the project root directory and add the following content:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    TAVILY_API_KEY=your_tavily_api_key
    POSTGRES_HOST=your_postgres_host
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB_NAME=your_postgres_db_name
    ```

    Note that you may need to add other keys based on what tools you're going to use

6. **Install the dependencies using the `requirements.txt` file**:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use this project, follow these steps:

1. **Run the application**:

    ```sh
    python src/app.py
    ```

## Contributing

To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch: 

    ```sh
    git checkout -b your-feature-branch
    ```

3. Make your changes and commit them:

    ```sh
    git commit -m 'Add some feature'
    ```

4. Push to the original branch:

    ```sh
    git push origin your-feature-branch
    ```

5. Create a pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project is licensed under the [MIT License](LICENSE).
