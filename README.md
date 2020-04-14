# Minimal WebPush Topic Demo

This is a suite of things to help show how sites can use WebPush topics.

Topics are a special class of WebPush messages that will automatically replace
themselves if the user hasn't gotten them yet. Think of messages like "You have
4 pending notifications". Instead of getting a bunch of messages showing your
 increasing popularity, you'll just get the one "topic".

## Getting Started

 This demo was written on a Linux box. This means that macs may work too, but
 older installs of Windows might have a harder time of things.

  In addition, you'll need to either serve the `./page` directory from your
  local web server or run `bin/topic_server` with enough privileges to be able
  to start a web server at port 80 (default port is: *8200*). This is
  because of
  a restriction enforced by ServiceWorkers. ServiceWorker scripts must either
  be served from a secure server (one that can run `https://` or from `localhost`)

### Prerequisites

  * `build-essential` or equivalent cc, make, etc. meta package
  * libssl-dev
  * $PYTHON development libraries (e.g. `python3-dev`)

### Setup

    PYTHON=python3
    git clone https://github.com/jrconlin/topics.git
    cd topics
    virtualenv -p $PYTHON venv
    source venv/bin/activate
    python setup.py develop
    venv/bin/topic_server


 Now start your browser and go to the topic `page` being served.
 (Again,
 either this is under a server running on your local machine, or by
 running
 `bin/topic_server -p 8200`)

 The page is fairly self explanatory, but basically, click on the ***Subscribe***
 button, and say "Allow" when prompted.

## Sending Messages

 Once you've successfully sent the browser credentials to the server, you can
  use them to send WebPush notifications to yourself.

  Feel free to run `bin/topic_pusher --msg "Hello, I'm a message!"` and you
  should see a notification pop up. That's a normal WebPush Message.

  If you've successfully sent a message, things are working. To get the full
  topic experience, close the browser.

  Once it's closed, send a few normal messages, and then send a few
  messages with a topic like

      bin/topic_pusher --msg "I'm message #1" --topic MyTopic
      bin/topic_pusher --msg "I'm message #2" --topic MyTopic


  When you re-open your browser, you should see all of the pending messages,
  but you should only see the latest message for `MyTopic`. NOTE: Currently
  the topic name is not sent as part of the data. The `msg` can be any content,
  so it's trivial to turn it into a JSON object that includes the topic name
  if you wanted that info passed along.

## Installation Errors

### Could not find required distribution pyasn1

If you get the following error:

    error: Could not find required distribution pyasn1

Then re-run:

    python setup.py develop


### OSX Users - SSL error

Apple has deprecated OpenSSL in favor of its own TLS and crypto libraries.
If you get an SSL error on OSX (El Capitan), install OpenSSL with brew, then
link brew libraries and install cryptography.
NOTE: /usr/local/opt/openssl is symlinked to brew Cellar:


    brew install openssl
    ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" \
      CFLAGS="-I/usr/local/opt/openssl/include" pip install cryptography

Then re-run:

    python setup.py develop

