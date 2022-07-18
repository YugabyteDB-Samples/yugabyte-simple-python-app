import psycopg2
import psycopg2.extras

config = {
    'host': '127.0.0.1',
    'port': '5433',
    'dbName': 'yugabyte',
    'dbUser': 'yugabyte',
    'dbPassword': 'yugabyte',
    'sslMode': '',
    'sslRootCert': ''
}


def main(conf):
    print(">>>> Connecting to YugabyteDB!")

    try:
        if conf['sslMode'] != '':
            yb = psycopg2.connect(host=conf['host'], port=conf['port'], database=conf['dbName'],
                                  user=conf['dbUser'], password=conf['dbPassword'],
                                  sslmode=conf['sslMode'], sslrootcert=conf['sslRootCert'],
                                  connect_timeout=10)
        else:
            yb = psycopg2.connect(host=conf['host'], port=conf['port'], database=conf['dbName'],
                                  user=conf['dbUser'], password=conf['dbPassword'],
                                  connect_timeout=10)
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
                  "Consider adding retry logic or using the pessimistic locking.")
        exit(1)

    print(">>>> Transferred {} between accounts.".format(amount))


if __name__ == "__main__":
    main(config)
