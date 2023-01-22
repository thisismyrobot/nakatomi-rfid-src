pipenv run python build\pyboard.py --device COM4 -f cp mfrc522.py :mfrc522.py
pipenv run python build\pyboard.py --device COM4 -f cp neopixel.py :neopixel.py
pipenv run python build\pyboard.py --device COM4 -f cp program.py :main.py
pause
