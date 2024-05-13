# anki-cards-ai-generator
Flash cards and spaced repetition can be combined together into powerful and effective tool for many areas of studying, from languages to university subjects.
The creation of these cards is an interesting, but sometimes time-consuming process.
There are many automations (e.g [AnkiBrain](https://ankiweb.net/shared/info/1915225457)) that can create the anki cards from promts using ChatGPT.
However, these tools do not allow promt customization or image creation.

## Prerequisites
1. This is an application that automates the cards creation process. Your [OpenAI API](https://platform.openai.com/api-keys) key is required.
2. Add-on [AnkiConnect](https://ankiweb.net/shared/info/2055492159) is used for the import of the cards. It must be installed.

## Workflow
1. This tool reads a list of words and corresponding context
2. For each file, a new OpenAI session is created. Rules for ChatGPT are passed with preconfigured prompts.
3. For each element from the list one flash card is created.

## Synchronization
Cards are imported into local Anki client, and pictures are copied to the Anki media folder (e.g. to 'C:\\Users\\User\\AppData\\Roaming\\Anki2\\User 1\\collection.media')
Then Anki can be synchronized with AnkiWeb, and the deck can be used from other devices.

## Usage
### Input

### Output

## Interface


## OpenAI API
DALLE 3: 'dall-e-3', 3 RPM, 200 RPD