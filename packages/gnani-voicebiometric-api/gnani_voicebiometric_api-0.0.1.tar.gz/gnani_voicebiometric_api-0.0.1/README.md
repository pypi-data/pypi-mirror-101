# Python Text-to-speech Client

## Installation

### Ubuntu
- apt-get install python3.6
- apt-get install python3-pip

### Mac OSX
- `brew install python3`
- `brew install python3-pip`
___
### How to run Applicatiton
- update details in `user.config` file.
- `pip3 install requests`
- `pip3 install pytz`
- `Place the certificate in root directiory`

### Step 1: To Enroll your voice with VoiceBiometric server
- `python3 enroll.py` 

### Step 2: To Authenticate your voice with VoiceBiometric server
- `python3 authenticate.py` 

### Step 2: To disenroll your voice with VoiceBiometric server
- `python3 disenroll.py` 

### PyPi Package Link.
- For package link: [Package Link](https://pypi.org/project/gnani-asr-grpc-api/0.0.1/)

### Installation of package. 
- `pip install gnani-asr-grpc-api==0.0.1`

## Note:
- Please make sure you are running the python command from the directory which has certificate file and the audio file. 

### Import commands:
- `from gnani_grpc_client import client`
- Enter the required inputs.

- To get the transcription run :
- `client.start(url,token, accesskey, encoding, lang_code, format, audio_name)`
- note: please enter the value of each ones within single inverted comas ' ' for example: client.start('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9..-KwcxWz45Q', '26ac22bd1c4ac4941c75e86' , 'pcm16', 'hi-IN', 'wav')
