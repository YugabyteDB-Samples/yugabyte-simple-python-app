# Simple Python Application for YugabyteDB

This application connects to your YugabyteDB instance via the 
[Python psycopg2 driver](https://docs.yugabyte.com/latest/reference/drivers/ysql-client-drivers/#psycopg2) and performs basic SQL 
operations. The instructions below are provided for [Yugabyte Cloud](https://cloud.yugabyte.com/) deployments. 
If you use a different type of deployment, then update the `sample-app.go` file with proper connection parameters.

## Prerequisite
* Python 3.6 or later
* psycopg2

## Start Yugabyte Cloud Cluster

* [Start YugabyteDB Cloud](https://docs.yugabyte.com/latest/yugabyte-cloud/cloud-quickstart/qs-add/) instance. You can use
the free tier at no cost.
* Add an IP address of your machine/laptop to the [IP allow list](https://docs.yugabyte.com/latest/yugabyte-cloud/cloud-secure-clusters/add-connections/#manage-ip-allow-lists)

## Clone Application Repository

Clone the repository and change dirs into it:

```bash
git clone https://github.com/yugabyte/yugabyte-simple-python-app.git && cd yugabyte-simple-python-app
```

## Install required packages

```bash
pip install -r requirements.txt
```

## Provide Yugabyte Cloud Connection Parameters

Note, Yugabyte Cloud requires SSL connections

Open the `sample-app.py` file and edit the following configuration parameters:
* `username` - The username for connecting to the database
* `password` - The password for connecting to the database
* `server` - The server hostname to connect to
* `cert_file` - If using SSL, Full path to the root CA certificate if using SSL, otherwise leave as None

## Execute the script 
Note, you can easily find all the settings on the Yugabyte Cloud dashboard:

![image](resources/cloud_app_settings.png)

```bash
python3 sample-app.py
```

Upon successful execution, you will see output similar to the following:

```bash
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

## Explore App Logic

Congrats! You've successfully executed a simple Go app that works with Yugabyte Cloud.

Now, explore the source code of `sample-app.go`:
1. `main` function - establishes a connection with your cloud instance via Go PostgreSQL driver.
3. `createDatabase` function - creates a table and populates it with sample data.
4. `selectAccounts` function - queries the data with SQL `SELECT` statements.
5. `transferMoneyBetweenAccounts` function - updates records consistently with distributed transactions.

## Questions or Issues?

Having issues running this application or want to learn more from Yugabyte experts?

Send a note to [our Slack channel](https://join.slack.com/t/yugabyte-db/shared_invite/zt-xbd652e9-3tN0N7UG0eLpsace4t1d2A),
or raise a question on StackOverflow and tag the question with `yugabytedb`!