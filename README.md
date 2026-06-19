# Artificial-DB-simulation

<p align="center">
  <img src="https://img.shields.io/github/stars/Jacus000/Artificial-DB-simulation?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/Jacus000/Artificial-DB-simulation?style=social" alt="GitHub Forks">
  <img src="https://img.shields.io/badge/license-Not%20Specified-lightgrey" alt="License: Not Specified">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version">
</p>

Creating and exploring a database of a fictional entertainment park. This project aims to simulate a realistic database for an amusement park, complete with various types of data like personal information, event logs, and operational details. It's an excellent resource for testing applications, practicing SQL queries, or conducting data analysis on a generated dataset.

## Table of Contents

- [Project Title & Description](#project-title--description)
- [Key Features & Benefits](#key-features--benefits)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Installation & Setup Instructions](#installation--setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Python Environment](#2-set-up-python-environment)
  - [3. Database Setup](#3-database-setup)
  - [4. Initialize Database Schema](#4-initialize-database-schema)
  - [5. Generate Initial Data](#5-generate-initial-data)
- [Usage Examples](#usage-examples)
- [Configuration Options](#configuration-options)
- [Contributing Guidelines](#contributing-guidelines)
- [License Information](#license-information)
- [Acknowledgments](#acknowledgments)

---

## Key Features & Benefits

This project offers a robust framework for generating and exploring a simulated entertainment park database.

### Key Features:
*   **Comprehensive Data Generation**: Create diverse datasets including personal information (names, surnames, addresses, phone numbers, emails, PESEL - *Polish national identification number*), event data (e.g., accidents), and more.
*   **Realistic Simulation**: Generate data that mimics real-world scenarios within an amusement park environment.
*   **Modular Architecture**: Easily extendable Python modules for generating different types of data.
*   **Database Integration**: Seamlessly populates a relational database (e.g., PostgreSQL) with the generated data.
*   **Analysis Ready**: Provides an R Markdown template (`Raport_Analiza_Quant.Rmd`) for quantitative analysis of the simulated data.
*   **Database Management Scripts**: Includes scripts for cleaning, dropping, and initializing the database structure.

### Benefits:
*   **Safe Testing Environment**: Ideal for developing and testing applications that interact with a database without using sensitive or real-world data.
*   **Data Analysis Practice**: Provides a rich dataset for practicing SQL queries, data manipulation, and performing various analyses.
*   **Educational Tool**: Excellent for learning about database design, data generation techniques, and data simulation.
*   **Customizable**: Configure various parameters to tailor the generated data to specific needs.

## Project Structure

The repository is organized as follows:

```
├── .env                              # Environment variables (e.g., database credentials)
├── .gitignore                        # Files/directories to ignore in Git
├── README.md                         # Project documentation
├── Raport_Analiza_Quant.Rmd          # R Markdown for quantitative analysis
├── data/                             # Contains data-related files
│   ├── generate_data/                # Python scripts for data generation logic
│   │   └── personal_data_example.py  # Example script for generating personal data
│   └── raw_data/                     # Raw input data files (e.g., name lists, addresses)
│       ├── adresy.csv
│       ├── imiona_meskie.csv
│       ├── imiona_zenskie.csv
│       ├── nazwiska_meskie.csv
│       └── nazwiska_zenskie.csv
├── database/                         # Database-related files
│   └── seeds/                        # SQL seed files for initial data
│       └── dev/                      # Development specific seed files
│           ├── clean_db.sql          # Script to clean dynamic data
│           ├── drop_db.sql           # Script to drop database tables
│           └── static/               # Static data seed files
│               └── 00_fill_sectors.sql # Populates initial static tables (e.g., park sectors)
└── python/                           # Core Python application logic
    ├── db/                           # Database interaction modules
    │   └── fetch_from_db.py          # Module for fetching data from the database
    ├── generate/                     # Core data generation modules
    │   └── generate_accidents.py     # Example module for generating accident data
    └── generation_orchestrator.py    # Orchestrates the data generation process
    └── main.py                       # Main script to run the data generation
```
*(Note: A `scripts/` directory containing `init_db.sh` is implied for database initialization, as referenced in `main.py` comments. Please ensure this script is located and executable.)*

## Technologies Used

### Languages:
*   **Python**: Primary language for data generation and database interaction.
*   **SQL**: For database schema definition, initialization, and data manipulation.
*   **R** (Optional): For quantitative analysis using `Raport_Analiza_Quant.Rmd`.

### Frameworks & Libraries:
*   **pandas**: For efficient data manipulation and processing in Python.
*   **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper (ORM) for database abstraction.
*   **python-dotenv**: For managing environment variables securely.
*   **PostgreSQL**: Recommended relational database system for hosting the generated data.
*   **Bash Scripting**: For database setup and management tasks.

## Prerequisites & Dependencies

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Python 3.8+**: The primary language for the project.
*   **pip**: Python package installer (usually comes with Python).
*   **PostgreSQL**: A running PostgreSQL server instance.
*   **psql client**: Command-line interface for PostgreSQL.
*   **(Optional) R and RStudio**: If you plan to use the R Markdown report for quantitative analysis.

## Installation & Setup Instructions

Follow these steps to get your local copy up and running:

### 1. Clone the Repository

First, clone the `Artificial-DB-simulation` repository to your local machine:

```bash
git clone https://github.com/Jacus000/Artificial-DB-simulation.git
cd Artificial-DB-simulation
```

### 2. Set Up Python Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

Install the required Python packages. Create a `requirements.txt` file in the root of your project if it doesn't exist, and populate it with the following:

```
pandas
sqlalchemy
python-dotenv
psycopg2-binary # For PostgreSQL connectivity
```

Then install:

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Ensure you have a PostgreSQL server running and accessible.

#### Create a `.env` file:
Create a file named `.env` in the root directory of the project and populate it with your PostgreSQL connection details:

```dotenv
# .env example
USER=your_postgres_user
PASSWORD=your_postgres_password
HOST=localhost
PORT=5432
DB_NAME=entertainment_db
```
Replace `your_postgres_user`, `your_postgres_password`, and `entertainment_db` with your actual database credentials and desired database name. Ensure your PostgreSQL user has privileges to create databases or that the `entertainment_db` is already created.

### 4. Initialize Database Schema

The project uses a bash script to set up the database structure and populate initial static data.

**Locate the `init_db.sh` script and run it:**

```bash
# Assuming the 'init_db.sh' script is located in a 'scripts' directory
# at the root of your project. If not, adjust the path accordingly.
cd scripts # This directory is implied by the main.py comments.
           # Please verify its actual location or copy 'init_db.sh'
           # to a suitable location if not found.

./init_db.sh
```
You will be prompted to enter your PostgreSQL password during this process. This script typically handles:
*   Creating the `entertainment_db` if it doesn't exist.
*   Setting up all necessary tables (schema definition).
*   Populating static data from `database/seeds/dev/static/00_fill_sectors.sql` and potentially other seed files.

### 5. Generate Initial Data

Once the database structure is in place, you can generate the dynamic, simulated data:

```bash
python main.py
```

Upon successful execution, you should see a message: `Success: Database is populated.`

## Usage Examples

After following the setup instructions, your `entertainment_db` will be populated with simulated data.

### Querying the Database
You can now connect to your PostgreSQL database using `psql` or any other database client and explore the generated data:

```bash
psql -h localhost -p 5432 -U your_postgres_user -d entertainment_db
```
*(Remember to replace placeholders with your actual credentials.)*

You can run SQL queries directly, for example:
```sql
SELECT * FROM workers LIMIT 10;
SELECT * FROM accidents ORDER BY accident_date DESC LIMIT 5;
```

### Extending Data Generation
The `python/generate/` directory contains modules for generating various types of data. You can inspect these scripts (e.g., `generate_accidents.py`, `personal_data_example.py`) to understand how data is created and potentially add new generation logic to suit your specific simulation needs.

### Quantitative Analysis
The `Raport_Analiza_Quant.Rmd` file provides a starting point for analyzing the generated data using R. If you have R and RStudio installed, open this file to run the analysis and generate reports based on your simulated database.

## Configuration Options

The primary configuration for the project is handled via the `.env` file in the root directory.

*   **`.env` variables**:
    *   `USER`: PostgreSQL username for database connection.
    *   `PASSWORD`: PostgreSQL password for database connection.
    *   `HOST`: Database host (e.g., `localhost` or an IP address).
    *   `PORT`: Database port (default `5432` for PostgreSQL).
    *   `DB_NAME`: The name of the database to connect to (`entertainment_db` by default).

*   **Generation Parameters**:
    Some data generation modules (e.g., `python/generate/generate_accidents.py`) accept parameters like `probability_of_accidents`. These can be adjusted directly in the Python code within the respective generation modules. For more dynamic control, you could modify `main.py` to expose these as command-line arguments.

## Contributing Guidelines

We welcome contributions to the `Artificial-DB-simulation` project! If you'd like to contribute, please follow these steps:

1.  **Fork** the repository on GitHub.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/issue-description`.
3.  **Make your changes**, ensuring they adhere to the project's existing coding style and maintain functionality.
4.  **Write clear, concise commit messages** explaining your changes.
5.  **Push your branch** to your forked repository.
6.  **Open a Pull Request** to the `main` branch of the original repository, providing a detailed description of your changes and why they are beneficial.

## License Information

This project does not currently have a specified license. Users are advised to contact the owner (Jacus000) for licensing terms if they intend to use this project beyond personal exploration or private development.

## Acknowledgments

*   Special thanks to the open-source community for the invaluable tools and libraries used in this project, including Python, pandas, SQLAlchemy, and PostgreSQL.
*   Credit to various online resources for providing lists of names, surnames, and addresses that serve as raw data for the generation process in `data/raw_data/`.
