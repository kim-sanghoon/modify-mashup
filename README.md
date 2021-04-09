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
- `app.py` : This Flask module handles Webhook responses from the Dialogflow front-end. A valid SSL certificate is required.

    The API endpoint description is as follows:
    - `POST /` handles a Dialogflow webhook request. Check [the webhook request document](https://cloud.google.com/dialogflow/es/docs/fulfillment-webhook#webhook_request) for the detailed information.

- `mashup.py` : This Flask module handles the registered IoT mashups and their history.

    The API endpoint description is as follows:
    - `GET /` responds the current history data and modification log in a numbered list.
    - `GET /{number}` switches the current history & mashup set based on the given number.<br />It would return a `{"setId": "{number}", "status": "ok"}` if okay, or a `{"status": "error"}` response otherwise. **This operation will clear the current modification log.**
    - `GET /check` responds the health of the mashup module.<br />It would return a `{"status": "ok"}` json response if okay, or a `{"status": "error"}` response otherwise.
    - `POST /search` responds the search results of `RulesHistory.search()` method.<br />It would return a `{"status": "ok", "searchResults": "..."}` json response if okay (even if found nothing), or a `{"status": "error", "what": "... the reason of error ..."}` response otherwise.<br />The search results will be dumped by `pickle` library and be encoded into base64, so be cautious of any security issues!
    - `POST /modify` accumulates any modification inputs from a user.<br />Similar to `/search` operation, it will search the target mashup using `RulesHistory.search()` with additional arguments named `modifyType` and `modifyData`, which indicate the user modification input.
    - `POST /type` receives a Google Dialogflow intent and checks the intent matches to the trigger or action of given search context. The detailed specification of json response is as follows:
        - `boolean trigger`: true if the trigger of given search context matches to the user input intent, false otherwise.
        - `boolean action`: true if the action of given search context matches to the user input intent, false otherwise.
        - `list of NominalAction | NominalTrigger intentData`: the nominal objects of user input intent, which are mapped from `intents.json`.

- `logger.py` : The logging module.

- `test/*` : Unit test scripts.

- `src/*`: They are the core source codes of this implementation. Check `src/README.md` for more details.