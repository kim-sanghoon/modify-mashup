# Editing an IoT Mashup Through Conversational Channel

This repository contains the back-end implementation of conversational mashup editing agent.

### Preparing for the installation
The implementation has been tested on Python 3.5.

1. Install requirements.
    ```bash
    pip3 install -r requirements.txt
    ```
2. Locate a valid SSL certificate on the root project directory with the filename of `server.crt` and `server.key`.
3. Import the agent (`Currently, we do not disclose the dialogflow agent file.`) to your dialogflow console, and configure the webhook settings.
4. Command `sudo python3 mashup.py` to initialize the mashup module.
5. Command `sudo python3 app.py` to initialize the back-end module.

### Descriptions
- `app.py` : This Flask module handles Webhook responses from the Dialogflow front-end.
- `mashup.py` : This Flask module handles the registered IoT mashups and their history.
- `logger.py` : The logging module.
- `test/*` : Unit test scripts.
- `src/*`: They are the core source codes of this implementation. Check `src/README.md` for more details.