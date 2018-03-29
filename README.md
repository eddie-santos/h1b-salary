# H1B Salary Data

First, install Postgresql via the command line:

```bash
brew cask install postgres
```

Note that you must have brew installed, and the cask provides an app on top of the binaries. Open the postgres app, and make sure it's running. You'll see an elephant in the top toolbar. You can access Postgres via the command line by entering `psql postgres`, which takes you inside of the `postgres` database. Note that you can create other databases by typing `createdb {database_name}` on the command line, and enter them analogously.

You can find the H1B salary data under the Disclosure Data tab [here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm). I recommend adding the downloaded data into a folder called `data` in this directory. I reformatted the H1B/LCA file names to be `h1bdata_20XX.xlsx` where the `XX` encode the exact year. Note that the data formatting varies a bit year to year, and the files are rather large. The `parse_data.py` file can be run by `python3 parse_data.py`, and takes into account the differences in schema. You'll have to modify the `file_dir` to the absolute path to the data folder you just created.

A note on the database url: the `db_url` is really just the web address the database sits at, which in our case is local, though it doesn't have to be. A general url has the structure `{protocol}://{user}:{password}@{host}:{port}/{endpoint}`. You're generally used to the HTTP protocol, but in this case we're using the `postgresql+psycopg2` protocol. We haven't established a user or password (okay since it's local and not important), and obviously you don't see this for most websites, but you can log in to some special parts with this approach. Host is mostly a domain name or ip address (in our case `localhost`, which is the domain name for the ip address `127.0.0.1`), and Postgres typically sits at port 5432. Note that most public websites sit at port 80, and modern browsers assume if you didn't put a port you're referring to port 80. The endpoint is typically a routing system that is defined by functions that help you access a resource. In our case, the endpoint is simply the database name, telling the Postgres protocol to use that database.