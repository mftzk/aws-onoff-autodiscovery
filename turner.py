import boto3

# construction of the client
client = boto3.client('ec2', region_name='ap-southeast-1')

# class for get the instance id and name
class Wrapper(object):
    def __init__(self, tags):
        self.tags = tags
        pass

    def filterInstanceIds(self, state):
        response = client.describe_instances(
        Filters=[
            {
            'Name': 'tag:' + self.tags,
            'Values': [
                'True',
            ]
            },
            {
            'Name': 'instance-state-name',
            'Values': [state]
            }
        ]
        )
        return response

    instance_ids = []
    list_name = []
    def getInstancesIds(self, state):
        
        response = self.filterInstanceIds(state)
        for i in response['Reservations']:
            for j in i['Instances']:
                self.instance_ids.append(j['InstanceId'])
                for x in j['Tags']:
                    if x['Key'] == 'Name':
                        self.list_name.append(x['Value'])
        return self.instance_ids, self.list_name

# class for turn on and off the instance and formatting slack message
class Turner(Wrapper):
    def __init__(self, tags):
        if tags == 'StartUp':
            state = "stopped"
        elif tags == 'ShutDown':
            state = "running"

        Wrapper.__init__(self, tags)
        self.getId = self.getInstancesIds(state)
        self.instance_ids = self.getId[0]
        self.list_name = self.getId[1]
    
    def action(self):
        if self.tags == 'StartUp':
            msg = 'turned on'
            self.turnon()
        elif self.tags == 'ShutDown':
            msg = 'turned off'
            self.turnoff()
        return msg

    def formatMsg(self):
        if len(self.list_name) == 0:
            field = [{
                "type": "plain_text",
                "text": "No instance",
                "emoji": True
            }]
        else:
            field = []
            for y in self.list_name:
                z = {
                    "type": "plain_text",
                    "text": y,
                    "emoji": True
                }
                field.append(z)
        return field

    def turnon(self):
        for a in self.instance_ids:
                client.start_instances(
                    InstanceIds=[
                        a
                    ]
                )

    def turnoff(self):
        for a in self.instance_ids:
                client.stop_instances(
                    InstanceIds=[
                        a
                    ]
                )

