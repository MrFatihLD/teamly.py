# Introduction

---

This is the documentation for teamly.py, a library for Python to aid in creating applications that communicates with Teamly API.

## **Prerequisites**

---

teamly.py works with Python 3.8 or higher. Support for earlier versions of Python is not provided. Lower than Python 3.8 is not supported.

## **Installing**

---

You can get the library directly from PyPI:

```bash
pip install teamly.py
```
If your pre-installed Python version requires `pip3` instead of `pip`:
```bash
pip3 install teamly-py
```

if you are using Windows, then the following should be used instead:

```bash
pip install teamly.py
```
<br><br>

#### Virtual Enviroments

---

1. Go to your project's working directory:

```bash
cd your-bot-source
python -m venv bot-env
```

2. Activate the virtual enviroment:

```bash
source bot-env/bin/activate
```

On Windows you activate it with:

```bash
bot-env\Scripts\activate.bat
```

3. Use pip like usual:
```bash
pip install teamly.py
```

Congratulations. You now have a virtual environment all set up.
<br><br>


## **Basic Concepts**

---

teamly.py revolves around the concept of events. An event is something you listen to and then respond to. For example, when a message happens, you will receive an event about it that you can respond to.

A quick example to showcase how events work:

```Python
import teamly

client = client.Client()

@client.event
async def on_ready():
    print(f"Logged on as {client.user}!")

@client.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")

client.run("my token")
```
