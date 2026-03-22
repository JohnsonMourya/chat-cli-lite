# Contributing to Gemini CLI Lite

We welcome contributions to the Gemini CLI Lite project! To ensure a smooth and efficient collaboration, please follow these guidelines.

## Getting Started

1.  **Fork the repository:** Start by forking the [Gemini CLI Lite repository](https://github.com/your-username/gemini-cli-lite) to your GitHub account.
2.  **Clone your fork:** Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/your-username/gemini-cli-lite.git
    cd gemini-cli-lite
    ```
3.  **Create a virtual environment:** It's highly recommended to use a virtual environment for dependency management.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
4.  **Install dependencies:** Install the project dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Making Changes

*   **Create a new branch:** For each new feature or bug fix, create a new branch from `main`:
    ```bash
    git checkout -b feature/your-feature-name  # For features
    git checkout -b bugfix/your-bug-fix-name  # For bug fixes
    ```
*   **Write clear, concise code:** Adhere to the existing coding style and conventions.
*   **Write tests:** If you add new features or fix bugs, please write appropriate unit and/or integration tests.
*   **Update documentation:** If your changes affect the functionality or usage, update the `README.md` or other relevant documentation.

## Submitting Changes

1.  **Commit your changes:** Write clear and descriptive commit messages. A good commit message explains *what* was changed and *why*.
    ```bash
    git add .
    git commit -m "feat: Add new feature" # Example
    ```
2.  **Push your branch:** Push your local branch to your forked repository on GitHub:
    ```bash
    git push origin feature/your-feature-name
    ```
3.  **Create a Pull Request (PR):** Go to the original Gemini CLI Lite repository on GitHub and create a new Pull Request from your forked branch to the `main` branch. Please provide a detailed description of your changes in the PR.

## Code of Conduct

We strive to create a welcoming and inclusive community. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) (if available, otherwise implicit respectful behavior is expected).