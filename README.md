# Simple Python Application for YugabyteDB

This application connects to your YugabyteDB instance via the 
[Python psycopg2 driver](https://docs.yugabyte.com/latest/reference/drivers/ysql-client-drivers/#psycopg2) and performs basic SQL 
operations. The instructions below are provided for [YugabyteDB Aeon](https://cloud.yugabyte.com/) deployments. 
If you use a different type of deployment, then update the `sample-app.py` file with proper connection parameters.

## Prerequisites

* macOS with Apple M1 chip: Python 3.9.7 or later
* Other Operating Systems: Python 3.6 or later

## Start YugabyteDB Aeon Cluster

* [Start YugabyteDB Aeon](https://docs.yugabyte.com/latest/yugabyte-cloud/cloud-quickstart/qs-add/) instance. You can use
the free tier at no cost.
* Add an IP address of your machine/laptop to the [IP allow list](https://docs.yugabyte.com/latest/yugabyte-cloud/cloud-secure-clusters/add-connections/#manage-ip-allow-lists)

## Clone Application Repository

Clone the repository and change dirs into it:

```bash
git clone https://github.com/YugabyteDB-Samples/yugabyte-simple-python-app.git && cd yugabyte-simple-python-app
```

## Provide Cluster Connection Parameters

Open the `sample-app.py` file and edit the following configuration parameters:
* `host` - the hostname of your instance.
* `port` - the port number of the instance (the default is `5433`).
* `dbUser` - the username for your instance.
* `dbPassword` - the database password.
* `sslMode` - the SSL mode. Set to `verify-full` for YugabyteDB Aeon deployments.
* `sslRootCert` - a full path to your CA root cert (for example, `/Users/dmagda/certificates/root.crt`) 

Note, you can easily find all the settings on the YugabyteDB Aeon dashboard:

![image](resources/cloud-app-settings.png)

## Run the Application

1. Install [psycopg2](https://pypi.org/project/psycopg2/) (PostgreSQL database adapter):
    ```bash
    pip3 install psycopg2-binary
    ```
2. Run the application:
    ```bash
    python3 sample-app.py
    ```

Upon successful execution, you will see output similar to the following:

```bash
>>>> Connecting to YugabyteDB!
>>>> Successfully connected to YugabyteDB!
>>>> Successfully created table DemoAccount.
>>>> Selecting accounts:
name = Jessica, age = 28, country = USA, balance = 10000
name = John, age = 28, country = Canada, balance = 9000
>>>> Transferred 800 between accounts.
>>>> Selecting accounts:
name = Jessica, age = 28, country = USA, balance = 9200
name = John, age = 28, country = Canada, balance = 9800
```

## Explore Application Logic

Congrats! You've successfully executed a simple Python app that works with YugabyteDB.

Now, explore the source code of `sample-app.py`:
1. `main` function - establishes a connection with your cloud instance via psycopg2 driver.
2. `create_database` function - creates a table and populates it with sample data.
3. `select_accounts` function - queries the data with SQL `SELECT` statements.
4. `transfer_money_between_accounts` function - updates records consistently with distributed transactions.

## Questions or Issues?

Having issues running this application or want to learn more from Yugabyte experts?

Join [our Slack channel](https://communityinviter.com/apps/yugabyte-db/register),
or raise a question on StackOverflow and tag the question with `yugabytedb`!
