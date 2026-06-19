
# Artificial-DB-simulation

Creating and exploring a database of a fictional entertainment park. This project aims to simulate a realistic database for an amusement park, complete with various types of data like personal information, event logs, and operational details. It's an excellent resource for testing applications, practicing SQL queries, or conducting data analysis on a generated dataset.

## Table of Contents

* [Project Title & Description](https://www.google.com/search?q=%23project-title--description)
* [Key Features & Benefits](https://www.google.com/search?q=%23key-features--benefits)
* [Project Structure](https://www.google.com/search?q=%23project-structure)
* [Technologies Used](https://www.google.com/search?q=%23technologies-used)
* [Prerequisites & Dependencies](https://www.google.com/search?q=%23prerequisites--dependencies)
* [Installation & Setup Instructions](https://www.google.com/search?q=%23installation--setup-instructions)
* [1. Clone the Repository](https://www.google.com/search?q=%231-clone-the-repository)
* [2. Set Up Python Environment](https://www.google.com/search?q=%232-set-up-python-environment)
* [3. Database Setup](https://www.google.com/search?q=%233-database-setup)
* [4. Initialize Database Schema](https://www.google.com/search?q=%234-initialize-database-schema)
* [5. Generate Initial Data](https://www.google.com/search?q=%235-generate-initial-data)


* [Usage Examples](https://www.google.com/search?q=%23usage-examples)
* [Configuration Options](https://www.google.com/search?q=%23configuration-options)

---

## Key Features & Benefits

This project offers a robust framework for generating and exploring a simulated entertainment park database, focusing heavily on realistic, statistically sound data generation.

### Key Features:

* **Advanced Probabilistic Generation**: The core of the simulation relies on various realistic probability distributions to generate data that mirrors real-world statistical behavior, moving far beyond simple random assignment.
* **Deep Data Interdependency**: Generates strongly correlated datasets within a highly normalized relational structure. Events in the database affect one another—for instance, specific weather conditions, machinery breakdowns, and peak guest hours dynamically influence the probability of accidents and resource allocation.
* **Highly Configurable Parameters**: Allows for fine-tuning the simulation environment. You can easily adjust key variables such as the total number of guests, frequency of ride breakdowns, and the probability of accidents to scale the database or test specific edge cases.
* **Comprehensive Data Breadth**: Creates diverse records including personal information (names, surnames, addresses, phone numbers, emails, PESEL), financial logs, and operational event data.
* **Analysis Ready**: Provides an R Markdown template (`Raport_Analiza_Quant.Rmd`) for deep quantitative analysis and statistical validation of the simulated distributions.

### Benefits:

* **Safe Testing Environment**: Ideal for developing and testing applications that interact with a database without using sensitive or real-world data.
* **Data Analysis Practice**: Provides a rich dataset for practicing complex SQL aggregations, data manipulation, and performing various quantitative analyses.
* **Educational Tool**: Excellent for learning about database normalization, probabilistic data generation scripts, and simulation architecture.

## Project Structure

The repository is organized as follows:

```
├── .env                              # Environment variables (e.g., database credentials)
├── .gitignore                        # Files/directories to ignore in Git
├── README.md                         # Project documentation
├── Raport_Analiza_Quant.Rmd          # R Markdown for quantitative analysis
├── data/                             # Contains data-related files
│   ├── generate_data/                # Python scripts for probabilistic data generation logic
│   │   └── personal_data_example.py  
│   └── raw_data/                     # Raw input data files for realistic sampling
│       ├── adresy.csv
│       ├── imiona_meskie.csv
│       ├── imiona_zenskie.csv
│       ├── nazwiska_meskie.csv
│       └── nazwiska_zenskie.csv
├── database/                         # Database-related files
│   └── seeds/                        # SQL seed files for initial static data
│       └── dev/                      
│           ├── clean_db.sql          # Script to clean dynamic data
│           ├── drop_db.sql           # Script to drop database tables
│           └── static/               
│               └── 00_fill_sectors.sql 
├── scripts/                          # Bash scripts for setup
│   └── init_db.sh                    # Database initialization script
└── python/                           # Core Python application logic
    ├── db/                           # Database interaction modules
    │   └── fetch_from_db.py          
    ├── generate/                     # Core data generation modules
    │   └── generate_accidents.py     
    ├── generation_orchestrator.py    # Orchestrates the interconnected data generation process
    └── main.py                       # Main script to run the data simulation

```

## Technologies Used

### Languages:

* **Python**: Primary language for probabilistic data generation and pipeline orchestration.
* **SQL**: For relational database schema definition, initialization, and data manipulation.
* **R** (Optional): For quantitative analysis and distribution plotting using `Raport_Analiza_Quant.Rmd`.

### Frameworks & Libraries:

* **pandas**: For efficient data manipulation and processing in Python.
* **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper (ORM) for database abstraction.
* **python-dotenv**: For managing environment variables securely.
* **MariaDB**: The primary relational database system used to build and test the project.

## Prerequisites & Dependencies

Before you begin, ensure you have the following installed:

* **Git**: For cloning the repository.
* **Python 3.8+**: The primary language for the project.
* **pip**: Python package installer.
* **MariaDB**: A running MariaDB server instance.
* **mariadb-client**: Command-line interface for MariaDB.
* **(Optional) R and RStudio**: If you plan to use the R Markdown report for quantitative analysis.

## Installation & Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Jacus000/Artificial-DB-simulation.git
cd Artificial-DB-simulation

```

### 2. Set Up Python Environment

Use a virtual environment to manage dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

```

Create a `requirements.txt` file in the root of your project if it doesn't exist, and install the required packages:

```
pandas
sqlalchemy
python-dotenv
mysqlclient # For MariaDB/MySQL connectivity

```

```bash
pip install -r requirements.txt

```

### 3. Database Setup

Create a `.env` file in the root directory of the project and populate it with your MariaDB connection details:

```dotenv
USER=your_mariadb_user
PASSWORD=your_mariadb_password
HOST=localhost
PORT=3306
DB_NAME=entertainment_db

```

### 4. Initialize Database Schema

Use the bash script to set up the database structure and populate initial static data.

```bash
cd scripts
./init_db.sh

```

### 5. Generate Initial Data

Once the database structure is in place, you can generate the interconnected, simulated data:

```bash
cd ..
python main.py

```

Upon successful execution, you should see a message indicating the database has been populated.

## Usage Examples

Connect to your MariaDB database using the CLI or any client (e.g., DBeaver, DataGrip) and explore the generated data:

```bash
mariadb -h localhost -P 3306 -u your_mariadb_user -p entertainment_db

```

Execute SQL queries to see the relationships and generated statistics:

```sql
SELECT * FROM workers LIMIT 10;
SELECT * FROM accidents ORDER BY accident_date DESC LIMIT 5;

```

## Configuration Options

The simulation is built to be highly modular. You can adjust the scale and behavior of the generated data.

### Environment Configuration

The primary connection configuration is handled via the `.env` file.

**Database Compatibility:** While the database was built and tested primarily on **MariaDB**, the architecture is highly flexible. Because the project utilizes **SQLAlchemy** for ORM and database interactions, you can easily connect to other relational databases (such as PostgreSQL, SQLite, or SQL Server). To do this, simply change the connection string in your `.env` file and ensure you have the appropriate Python database driver installed (e.g., `psycopg2-binary` for PostgreSQL). Note that while the Python code is DB-agnostic, the raw SQL initialization scripts (`init_db.sh` and seed files) may require minor dialect adjustments if moving away from MariaDB.

### Simulation Parameters

The generation scripts allow you to fine-tune the distributions and scale of the simulated park. These parameters control the density and frequency of events, respecting the underlying statistical dependencies:

* **`number_of_guests`**: Adjusts the total footprint of park visitors, cascading into ticket sales, queue times, and crowd density metrics.
* **`probability_of_accidents`**: Modifies the baseline statistical chance of incidents occurring, which dynamically interacts with weather conditions and specific park sectors.
* **`breakdown_rate`**: Configures how often machinery and attractions suffer from technical failures, generating realistic maintenance logs and downtime periods.

These parameters can be configured directly within the core generation modules (e.g., `python/generate/`) or orchestrated via arguments in `main.py`.
