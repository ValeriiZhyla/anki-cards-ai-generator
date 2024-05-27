@echo off

python -m generator.read-generate-import .\demo\input_words.csv .\processing ^
          --language="german" ^
          --level="B2" ^
          --openai_api_key="YOUR_KEY" ^
          --deck_name="my_amazing_deck" ^
          --anki_media_directory_path="custom_path\Anki2\User\collection.media"

pause