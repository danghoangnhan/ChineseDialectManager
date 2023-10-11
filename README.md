
# ChineseDialectManager

The ChineseDialectManager is a web application that serves as a Chinese dialect management system. It allows users to manage and organize information related to various Chinese dialects.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Deployment Guide](#deployment-guide)
- [Contributing](#contributing)
- [License](#license)


## Features


- **Dictionaries  Management**: Users can create and edit dictionary information using the Django Admin interface.
- **IPA Converter**: The system supports an IPA converter that allows users to input pronunciation in the International Phonetic Alphabet (IPA) format.
- **CSV Import-Export**: The system supports importing and exporting dictionary data using CSV files. Users can import the dictionary's vocabulary and IPA conversion rules for easy data management.
## Requirements

Before the installation , ensure you have the following installed:

- ![Docker Version](https://img.shields.io/badge/Docker-20.10.21-blue.svg) 
- ![Docker Compose Version](https://img.shields.io/badge/Docker%20Compose-1.25.0-blue.svg)

## Deployment Guide

To deploy the ChineseDialectManager using Docker and Docker Compose, follow the steps below:

1. Clone the repository:

```bash
git clone https://github.com/danghoangnhan/ChineseDialectManager.git
cd IPADictionaryAPI
```

2. Create a prod.env file in the envs directory. Update the environment variables with your desired configuration:

```plaintext
# .env file

# Database configuration
MYSQL_ROOT_PASSWORD=your-mysql-root-password
MYSQL_DATABASE=your-mysql-db-name
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
```

3. Start the services (Django application and MySQL database):

```bash
docker-compose up -d
```

4. Once the services are up and running, open your web browser and go to `http://127.0.0.1:8002/admin/` to access the Django Admin interface.

4. Log in using the superuser account created during installation.

5. Use the Django Admin interface to manage Chinese dialect data, including adding, editing, and deleting dialect information.

6. Customize the application as needed for your specific use case.

 sudo docker exec -i 6b968d5ae8af mysqldump -uroot -pdictionary dictionary > backup.sql
