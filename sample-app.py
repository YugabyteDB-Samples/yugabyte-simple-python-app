import psycopg2
import psycopg2.extras

config = {
    'username': '', # The username for connecting to the database
    'password': '', # The password for connecting to the database
    'server': '', # The server hostname to connect to
    'cert_file': None # Full path to the root CA certificate if using SSL
}


def main(conf):
    try:
        if conf['cert_file']:
            yb = psycopg2.connect(user=conf['username'], password=conf['password'],
                                  host=conf['server'],
                                  port='5433', database='yugabyte',
                                  sslmode="verify-full", sslrootcert=conf['cert_file'])
        else:
            yb = psycopg2.connect(user=conf['username'], password=conf['password'],
                                  host=conf['server'],
                                  port='5433', database='yugabyte')
    except Exception as e:
        print("Exception while connecting to YugabyteDB")
        print(e)
        exit(1)

    print(">>>> Successfully connected to YugabyteDB!")

    create_database(yb)
    select_accounts(yb)
    transfer_money_between_accounts(yb, 800)
    select_accounts(yb)
    yb.close()


def create_database(yb):
    try:
        with yb.cursor() as yb_cursor:
            yb_cursor.execute('DROP TABLE IF EXISTS DemoAccount')

            create_table_stmt = """
                CREATE TABLE DemoAccount (
                    id int PRIMARY KEY,
                    name varchar,
                    age int,
                    country varchar,
                    balance int
                )"""
            yb_cursor.execute(create_table_stmt)

            insert_stmt = """
                INSERT INTO DemoAccount VALUES
                        (1, 'Jessica', 28, 'USA', 10000),
                        (2, 'John', 28, 'Canada', 9000)"""
            yb_cursor.execute(insert_stmt)
        yb.commit()
    except Exception as e:
        print("Exception while creating tables")
        print(e)
        exit(1)

    print(">>>> Successfully created table DemoAccount.")


def select_accounts(yb):
    print(">>>> Selecting accounts:")

    with yb.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as yb_cursor:
        yb_cursor.execute("SELECT name, age, country, balance FROM DemoAccount")

        results = yb_cursor.fetchall()
        for row in results:
            print("name = {name}, age = {age}, country = {country}, balance = {balance}".format(**row))


def transfer_money_between_accounts(yb, amount):
    try:
        with yb.cursor() as yb_cursor:
            yb_cursor.execute("UPDATE DemoAccount SET balance = balance - %s WHERE name = 'Jessica'", [amount])
            yb_cursor.execute("UPDATE DemoAccount SET balance = balance + %s WHERE name = 'John'", [amount])
        yb.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print("Exception while transferring money")
        print(e)
        if e.pgcode == 40001:
            print("The operation is aborted due to a concurrent transaction that is modifying the same set of rows." +
                  "Consider adding retry logic for production-grade applications.")
        exit(1)

    print(">>>> Transferred {} between accounts.".format(amount))


if __name__ == "__main__":
    main(config)
