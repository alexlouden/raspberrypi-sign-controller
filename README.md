# raspberry-pi-sign

Basic website / API to control a sign using a Raspberry Pi + DotStar RGB LED strips

## Initial Pi setup

1. Install raspbian to microSD card, enable SSH (`touch /Volumes/boot/ssh`)

2. Power on Pi and SSH in (`pi`/`raspberry`)

3. Run `raspi-config` to enable SPI and choose country for Wifi, set up wifi details

4. Install fabric on your laptop (with Python 2, ugh) `pip install fabric`

5. Run `fab setup` & `fab deploy` from a clone of this repo

## Update sign code

1. Modify `sign.py` e.g. to add a new mode

2. Run `fab deploy`

## API

Locally: `http://signhostname.local:5000`

- GET `/change_mode` to cycle through the modes
- GET `/color/<r>,<g>,<b>` (r/g/b 0-255) to set a fixed colour
- GET `/off`
- GET `/green`
- GET `/red`

Note: API uses `GET` to be super easy to play with via your browser URL bar, and so you don't need CORS. Feel free to change to POST if you want to play it [safe](https://developer.mozilla.org/en-US/docs/Glossary/Safe)!

## Ngrok

`ngrok.service` runs `~/ngrok http 5000` which exposes port 5000 to the internet at `????.ngrok.io` (a randomly generated URL). You need to connect it to an ngrok account (run `~/ngrok authtoken <your_auth_token>`, or modify the [ngrok config file](https://ngrok.com/docs#config)).

See https://ngrok.com/

If you'd like a static subdomain (e.g. `sign.yourcompany.com`) you can set up a subdomain: https://ngrok.com/docs#subdomain

## Animation to music

Two of the modes (`animate_audio_hue` and `animate_audio_vis` in [`sign.py`](./sign.py)) use some basic signal processing (see `signal_processing.py`) to process audio from a USB microphone. It streams audio in chunks at 20 Hz using PyAudio, then uses `scipy` to extract the bandpower for both bass (20 - 250 Hz) and mid (250 Hz - 2 kHz) frequency ranges.

You can run `python signal_processing.py` to see a basic ascii visualisation in your terminal.
