@echo off

python -m generator.read-generate-import .\demo\input_words.csv .\processing ^
          --language="german" ^
          --level="B2" ^
          --openai_api_key="YOUR_KEY" ^
          --deck_name="my_amazing_deck" ^
          --anki_media_directory_path="custom_path\Anki2\User\collection.media" ^
          --card_model="Basic (type in the answer)" ^
          --image_generation_mode="replicate" ^
          --replicate_api_key="YOUR_REPLICATE_KEY" ^
          --replicate_model_url="your_replicate_model_url"

pause