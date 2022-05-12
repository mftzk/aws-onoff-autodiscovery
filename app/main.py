import os
import sys
from slack import WebClient
from turner import Turner



# class initializer for command line arguments
class Main():
    def __init__(self):
        pass
    
    def readCommand(self):
        ans = sys.argv[1]
        return ans
    
    def tagsDecider(self):
        read = self.readCommand()
        if read == 'up':
            tags = 'StartUp'
        elif read == 'down':
            tags = 'ShutDown'
        else:
            print('Wrong command')
        return tags

# class begining of the action
class Action(Main):
    def __init__(self):
        Main.__init__(self)
        self.tags = self.tagsDecider()
    
    def action(self):
        t = Turner(self.tags)
        msg = t.action()
        return msg

# class for slack message
class Slack_client(Turner, Main):
    def __init__(self, msg):
        Turner.__init__(self, self.tagsDecider())

        self.msg = msg
        self.field = Turner.formatMsg(self)
        pass

    def notify(self):
        sclient = WebClient(token=os.environ['SLACK_TOKEN'])

        blocks = [
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "List of servers " + self.msg + " by Automation AWS: "
                            }
                        ]
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "fields": self.field
                    }
                ]

        sclient.chat_postMessage(channel='#'+ os.environ['SLACK_CHANNEL'], blocks=blocks)

if __name__ == '__main__':
    a = Action()
    msg = a.action()

    s = Slack_client(msg)
    s.notify()