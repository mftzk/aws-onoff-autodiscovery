# Addtional Information
   Add tags on your instances `ShutDown:True` for auto shutdown `StartUp: True` for auto start

   Dont forget to configure your aws cli

## Install Dependencies
```
pip install -r requirements.txt
```

## Environment Setup
```
export SLACK_TOKEN=<your_slack_token>
export SLACK_CHANNEL=<your_slack_channel>
```

## How to use
1. for start vm
```
python3 main.py up
```

2. for stop vm
```
python3 main.py down
```