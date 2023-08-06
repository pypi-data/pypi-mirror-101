# What is this?
Tinybird Analytics is a blazing fast analytics engine for your serverless applications.
Think of it as a set of next-generation lego pieces for building data workflows and applications which rely on real-time analytics.

# Developing tinybird.co?

### Installing the development environment

1. Compile or install clickhouse:
    a. Compiling clickhouse yourself: [Debian/Ubuntu](https://clickhouse.yandex/#quick-start) or [MacOS/Other](https://clickhouse.yandex/docs/en/getting_started/)

    b. Using Docker: [Install docker](https://docs.docker.com/install/) and run the clickhouse container

    ```
    docker run -d --name tt -p 9000:9000 -p 8123:8123 --ulimit nofile=262144:262144 yandex/clickhouse-server
    ```

    Remember that if at any time you stop the docker container you will lose any data you may have imported to your clickhouse instance.

    c. Using Docker with ClickHouse `tinybird` cluster

    ```
    docker build --tag tinybird/clickhouse --file docker/tinybird-clickhouse.Dockerfile .
    docker run -d --name tb-ch -p 9000:9000 -p 8123:8123 --ulimit nofile=262144:262144 tinybird/clickhouse
    ```

    d. Use a pre-built binary, check https://clickhouse.tech/docs/en/development/build/#you-don-t-have-to-build-clickhouse. (see FAQ: using native clickhouse clickhouse builds with osx)

2. Install Python >= 3.6

3. Install Redis (and init it)

```
# On MacOS:
brew install redis
```

4. Checkout this repo

5. Create your mvenv and install all dependencies:

    **A. Straightforward way:**

    ```
    python3 -mvenv .e
    . .e/bin/activate
    PYCURL_SSL_LIBRARY=openssl pip install --editable .
    ```
    (--editable option means you can change code inside tinybird folder). Note that you need, at least, clickhouse headers in order to install python dependencies

    **B. You might get an error like this on OSX 10.15.5:**

    ```
    ImportError: pycurl: libcurl link-time ssl backend (none/other) is different from compile-time ssl backend (openssl)
    ```

    If that's the case, try installing `pycurl` like this (use the required pycurl version):

    ```
    brew install openssl curl-openssl
    python3 -mvenv .e
    . .e/bin/activate
    export PYCURL_SSL_LIBRARY=openssl;export PYCURL_CURL_CONFIG=/usr/local/opt/curl-openssl/bin/curl-config;export LDFLAGS='-L/usr/local/opt/openssl/lib -L/usr/local/opt/c-ares/lib -L/usr/local/opt/nghttp2/lib -L/usr/local/opt/libmetalink/lib -L/usr/local/opt/rtmpdump/lib -L/usr/local/opt/libssh2/lib -L/usr/local/opt/openldap/lib -L/usr/local/opt/brotli/lib';export CPPFLAGS=-I/usr/local/opt/openssl/include;pip install pycurl==7.43.0.3 --compile --no-cache-dir
    pip install --editable .
    ```
   
    **C. In Big Sur**
    
    Install the Catalina version of clickhouse-toolset and install pycurl with the correct SSL library before installing the dependencies.
    I have done this guide for Python 3.7, but 3.6 should work as well. If you want to use the 3.6, install the corresponding clickhouse-toolset version.
    ```
    brew install openssl
    python3 -mvenv .e
    . .e/bin/activate

    # Needs the latest pip version to install clickhouse-toolset
    pip install --upgrade pip
    # Remember to select the correct path to the .whl
    pip install ../clickhouse-toolset/dist/clickhouse_toolset-0.9.dev0-cp37-cp37m-macosx_10_15_x86_64.whl
    export PYCURL_SSL_LIBRARY=openssl;export LDFLAGS='-L/usr/local/opt/openssl/lib -L/usr/local/opt/c-ares/lib -L/usr/local/opt/nghttp2/lib -L/usr/local/opt/libmetalink/lib -L/usr/local/opt/rtmpdump/lib -L/usr/local/opt/libssh2/lib -L/usr/local/opt/openldap/lib -L/usr/local/opt/brotli/lib';export CPPFLAGS=-I/usr/local/opt/openssl/include;pip install pycurl==7.43.0.6 --compile --no-cache-dir
    # To check if pycurl is correctly installed and configured, executing "python -c 'import pycurl'" must return nothing. 

    # And now the dependencies:
    pip install --editable .
    ```


6. Config flake8 to prevent lint errors on commit:

    ```
    git config --bool flake8.strict true
    ```

### Testing locally

1. Install testing dependencies

```
pip install -e ".[test]"
```

2. Install zookeeper 

Ubuntu:
_(yes, it's `zookeeperd`)_

```
sudo apt install zookeeperd
```

Mac:

```
brew install zookeeper
```

3. Add zookeeper configuration in your ClickHouse installation:

* Enter config.d directory:

```
cd /path-to-your-clickhouse-server/config.d
```

* Create the zookeeper.xml file with the following config:

```xml
<yandex>
    <zookeeper>
        <node>
            <host>localhost</host>
            <port>2181</port>
        </node>
    </zookeeper>
</yandex>
```

4. Run the tests with [pytest](https://docs.pytest.org/en/stable/usage.html):

* Export env variables tests to pass:

```
export REDIS_PORT_TEST=6780
export CLICKHOUSE_BIN_FOLDER_PATH=/path/to/clickhouse
```

* To run all tests

```
pytest tests
```

* There're several options, for example, testing a single file:

```
pytest tests/views/test_api_datasources.py -vv
```

* Running a single test:

```
pytest tests/views/test_api_datasources.py -k test_name
```



### Starting the development environment

```
CLICKHOUSE_BIN_FOLDER_PATH=/path/to/clickhouse tinybird_server --port 8001
```

**Important note:** on OSX add `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` as follows

```
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES CLICKHOUSE_BIN_FOLDER_PATH=/path/to/clickhouse/bin tinybird_server --port 8001
```

### Useful commands

If running CH with docker, you can do the following to connect to clickhouse client
```
docker exec -it tt /bin/bash
clickhouse client
```

# Developing in the UI

You need, at least, **node** version 12 in order to have the UI running in your local development. Then, in the root of the project:

```bash
npm install
npm run dev:build
```

If you want to make changes and check how they look:

```bash
npm run dev:watch
```

Don't forget to test your changes:

```bash
npm run test
```

Or test + watch 🤗:

```bash
npm run test:watch
```

You have more information about development [here](development.md).

# FAQ
### What do I do to validate my development environment is working correctly?
Browse to http://localhost:8001/dashboard. You'll be prompted to login with your gmail account. Go back to /dashboard once you do and try importing

### Where is the marketing website code?
It is in the `index.html` page.

### Where is the blog hosted?
It is generated with Jekyll, and it is located in other [repository](https://gitlab.com/tinybird/blog).

### How can I see the documentation?
There is an automatic deploy job created so every time you merge something in master, if everything goes OK, the latest version of the documentation will be available at https://docs.tinybird.co

## using native clickhouse clickhouse builds with osx

### 1. Using the latest version of Clickhouse already compiled
```
curl -O 'https://builds.clickhouse.tech/master/macos/clickhouse' && chmod a+x ./clickhouse
wget https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/programs/server/config.xml
wget https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/programs/server/users.xml
sudo ./clickhouse server --config config.xml
```

### 2. Recommended: Use the Clickhouse version used in production (20.7.2.30 at 2020-01-19)

To get Clickhouse, you have two options:
- A: Download the compiled version from github from the version you need: `go to commits page, click on the first green checkmark or red cross near commit, and click to the “Details” link right after “ClickHouse Build Check”.`
- B: If you can't find the version you need (the store binaries just for a while), compile your own version following the steps in the documentation. Remember to use the documentation for your version, as the instructions varies between them. You will find those docs inside the repository.

You can find the configuration files (`config.xml` and `users.xml`) inside `tests/clickhouse_config`. Change the configuration paths as you need.

Execute clickhouse as always: `./clickhouse server --config config.xml`