# anki-cards-ai-generator
Flash cards and spaced repetition can be combined together into powerful and effective tool for many areas of studying, from languages to university subjects.
The creation of these cards is an interesting, but sometimes time-consuming process.
There are many automations (e.g [AnkiBrain](https://ankiweb.net/shared/info/1915225457)) that can create the anki cards from promts using ChatGPT.
However, these tools do not allow promt customization or image creation.

## Prerequisites
1. This is an application that automates the cards creation process. Your [OpenAI API](https://platform.openai.com/api-keys) key is required.
2. Add-on [AnkiConnect](https://ankiweb.net/shared/info/2055492159) is used for the import of the cards. It must be installed.

## Workflow
1. This tool reads a list of words and corresponding context. Duplicated words will be ignored
2. For each element from the list one flash card is created as following:
   1. ChatGPT creates a card text for a word (or a phrase)
   2. Card text is saved locally
   3. ChatGPT uses a word and generated card text to generate a prompt for DALLE 
   4. DALLE creates a picture for this word and return a URL 
   5. Picture is downloaded and stored locally 
   6. Add to the processed files
   7. Wait 20 seconds (to not exceed a DALLE RPM)
3. After all words processed, the results are validated
4. Pictures are copied to the Anki media folder, HTML card is formatted and added to a target deck. Duplicates are skipped
5. Generation results from OpenAI are archived

2a. On any error: save list of processed words. Next processing will ignore them.

## Synchronization
Cards are imported into local Anki client, and pictures are copied to the Anki media folder (e.g. to 'C:\\Users\\User\\AppData\\Roaming\\Anki2\\User 1\\collection.media')
Then Anki can be synchronized with AnkiWeb, and the deck can be used from other devices.

## Usage
### Input

### Output

## Interface


## OpenAI API
DALLE 3: 'dall-e-3', 3 RPM, 200 RPD