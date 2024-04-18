project setup
=============

Project setup instructions here.

1.  install poetry:
        -> https://python-poetry.org/docs/#installing-with-the-official-installer
    check poetry version:
        -> poetry --version

2.  install redis
        -> https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/

3.  install rejson
        -> Add rejson to control redis cache https://gist.github.com/britisharmy/ca0c3e37be4b20ccf2f9fc802c52ed63 

        -> set redis password (sudo redis-cli / config set requirepass redis_password) for linux  

        -> It used to blacklist the access token after logout

4.  Run
        -> inside scool management directory run command  

        -> mv env.txt .env  

        -> set all environment veriable according to you

5.  Run
        -> make project_setup

6.  See Makefile for all commands
