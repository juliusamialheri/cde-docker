# Python ETL Pipeline with Dockerized Database

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Python, dockerized with a PostgreSQL database. The ETL process runs in one container, and the database in another, connected via a Docker network.

## Prerequisites
- Docker installed on your local machine.
- Basic knowledge of running bash scripts and Docker commands.

## Project Structure
- `etl.py`: The Python script that performs the ETL operations.
- `Dockerfile`: Dockerfile for building the ETL container image.
- `run_etl.sh`: Bash script to automate starting containers, building the image, running the pipeline, and cleaning up.
- `README.md`: This file.

## Step-by-Step Instructions to Run the Pipeline Locally

1. **Save the Files**:
   - Create a new directory (e.g., `etl-docker`).
   - Save `etl.py`, `Dockerfile`, `run_etl.sh`, and `README.md` in this directory.

2. **Make the Bash Script Executable**:
   - Open a terminal and navigate to the project directory.
   - Run: `chmod +x run_etl.sh`

3. **Run the Pipeline**:
   - Execute the bash script: `./run_etl.sh`
   - This will:
     - Create a Docker network named `etl_network` (if it doesn't exist).
     - Start a PostgreSQL container named `db` with the database `mydb`, user `user`, and password `pass`.
     - Build the ETL image named `etl_image`.
     - Run the ETL container, which executes `etl.py` to perform the ETL process.
     - The script waits for the DB to be ready, extracts dummy data, transforms it (filters adults and uppercases names), and loads it into the `users` table in the database.
     - Finally, it cleans up by stopping and removing the DB container and network.

4. **Verify the Run**:
   - During execution, you'll see output from the ETL script, including the extracted data, transformed data, and confirmation of loading.
   - If you want to inspect the database after the run (before cleanup), comment out the cleanup section in `run_etl.sh` and manually connect to the DB:
     - Run: `docker exec -it db psql -U user -d mydb`
     - Query: `SELECT * FROM users;`
     - Exit with `\q`

5. **Notes**:
   - The ETL uses dummy generated data for extraction to keep it self-contained (no external dependencies like files or APIs).
   - The transformation uses Pandas for data manipulation.
   - The database connection uses the container name `db` as the host, thanks to Docker networking.
   - If the DB takes longer to start, adjust the wait loop in `etl.py`.
   - No additional dependencies need to be installed manually; the Dockerfile handles Python packages.
   - Cleanup is included to avoid leaving containers running, but you can modify as needed.

If you encounter issues (e.g., port conflicts or Docker permissions), ensure Docker is running and you have sufficient privileges.