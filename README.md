# anki-cards-ai-generator
Flash cards and spaced repetition can be combined into powerful and effective tool for many areas of studying, from languages to university subjects.
The creation of these cards is an interesting, but sometimes time-consuming process.
There are many automations (e.g [AnkiBrain](https://ankiweb.net/shared/info/1915225457)) that can create the anki cards from prompts using ChatGPT.
However, these tools do not allow prompt customization or image creation.

## Purpose of this tool
1. Create list of words or sentences with some context
2. Start the generation
3. Enjoy the new Anki deck with generated text, image, audio and dictionary link in your Anki app

## Prerequisites
1. This is an application that automates the cards creation process using the ChatGPT, DALLE and TTS models. Your [OpenAI API](https://platform.openai.com/api-keys) key is required.
2. Add-on [AnkiConnect](https://ankiweb.net/shared/info/2055492159) is used for the import of the cards. It must be installed.
3. Anki is running
4. Tool is compatible with python 3.10+

## Synchronization
Cards are imported into local Anki client, and pictures are copied to the Anki media folder (e.g. to 'C:\\Users\\User\\AppData\\Roaming\\Anki2\\User 1\\collection.media').  
Then Anki can be synchronized with AnkiWeb, and the deck can be used from other devices.

## Usage
Default settings:
```bash
python -m generator.read-generate-import ./demo/input_words.csv ./processing
```

Custom settings:
```bash
python -m generator.read-generate-import ./demo/input_words.csv ./processing --openai_api_key="YOUR_KEY" --deck_name="my_amazing_deck" --anki_media_directory_path="custom_path/Anki2/User/collection.media"
```
### Input
CSV with semicolon as separator (you can use commas in sentences and context), or an Excel file.
Header "word;context" is expected.
Example:
```csv
word;context
purchasing power parity;economy
affect;
consciousness;the state of human being
```

### Output
Card materials are created in the specified directory. 
Tool creates for each word:
- json with card text, paths and links
- png with generated image  
- mp3 with generated audio  

After generation, these files are used for card creation. The cards are imported into Anki deck automatically.

An example can be found in [Demo](demo).

## OpenAI API
Billing: https://platform.openai.com/settings/organization/billing/overview
Text: [gpt-4o](https://platform.openai.com/docs/models/gpt-4o)
Image: [dall-e-3](https://platform.openai.com/docs/guides/images/usage), 3 RPM, 200 RPD - main speed limitation
Audio: [tts-1-hd](https://platform.openai.com/docs/guides/text-to-speech)

### Cost
DALLE-3 call is the most expensive step, 0.05$ pro image. This is expensive compared with free images, but:
- Sometimes it is really difficult to find an image that describes some abstract content.
- These images boost (at least mine) learning process a lot
- Cards are much better than DALLE-2 cards in this use case

Text generation is much cheaper, less than 0.01$ pro image

## FAQ
A: Audio file plays when I'm opening the card, I don't like it!  
Q: By default, Anki automatically plays audio on the front and back of cards. You can choose ["Don't play audio automatically"](https://docs.ankiweb.net/deck-options.html) in deck options. In this case Anki will not play audio until you click the replay audio button.

## Artifacts
[![Workflow Name](https://github.com/ValeriiZhyla/anki-cards-ai-generator/actions/workflows/python-build-windows.yml/badge.svg)](https://github.com/ValeriiZhyla/anki-cards-ai-generator/actions/workflows/python-build-windows.yml)
