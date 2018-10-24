# S.T.A.L.K.E.R.

Application to track social media posts based on usernames with a goal to support a wide range of social channels. S.T.A.L.K.E.R. will scrape the supported social channels and return well formatted posts to a Slack webook for consumption.

### Motivation

This project was created as a learning exercise for Python, consuming REST APIs, and general application architecture and testing.

### Author

Mike Dunn is a senior Front-end Developer with 5+ years of professional experience. Seeking to help deliver high quality applications through excellent coding practices and technical leadership. Specializing in semantics, optimization and system design.

### Application Structure

`/services/messaging.py` - Messaging service that delivers the social classes formatted message

`/services/runner` - Instantiates social classes based on channel and calls required methods

`/social` - Contains files concerning social channel specific logic

`/main.py` - Entry point for Python

### Getting Started

##### Python Setup

Prerequisites:

* [Python 3.6](https://www.python.org/)
* [PIP](https://pip.pypa.io)

Commands to install and run application:

```
$ git clone git@github.com:MikeyDunn/S.T.A.L.K.E.R..git
$ cd S.T.A.L.K.E.R.
$ pip install -r requirements.txt
$ cp config_sample.yml config.yml
$ vi config.yml

// fill in your respected channels information

$ python main.py
```

##### Docker Setup

Coming Soon

### Testing

Coming Soon
