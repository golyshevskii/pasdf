<img src="../images/setup.png" alt="setup" width="30" height="30"/> Setup
====

To begin, you should clone the repository's contents into your working folder by using the provided command in the terminal:

```
git clone https://github.com/golyshevskii/pasdf.git
```

---

❗ While working locally, it's important to set up a virtual environment along with the required libraries and their dependencies. It's recommended to install everything needed for smooth development

1. _Use the following command to create a virtual development environment in the root of your working folder_:

```
python3 -m venv venv
```

2. _To install the necessary libraries and their dependencies, execute the command below in the root of the repository folder_:

```
make poetry-install
```

---

Once the necessary changes are made, ensure that **Docker** is active, and then execute the command to initialize **Airflow** containers

```
echo -e "AIRFLOW_UID=$(id -u)" > .env
make setup
```

---

Once the initialization is finished, access the [Airflow](http://localhost:8080/home) interface. Then, use the provided credentials to log in:

```
username: airflow
password: airflow
```

---

❗ Additionally, for local development and testing purposes, you need to set the environment variables. You can do it by executing this file:

```
source 
```

> _Replace the variable `your_absolute_path` with the absolute path to the project folder_
