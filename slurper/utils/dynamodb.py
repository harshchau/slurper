import os
import boto3

class DBUtils:

    def __init__(self):
        # If URLS_TABLE present in os.environ, use it, else use the urls_table
        # This is used in case the table name comes from the serverless setting
        if 'URLS_TABLE' in os.environ: 
            print('GOT OS ENVIRON')
            self.URLS_TABLE = os.environ['URLS_TABLE']
        else: 
            self.URLS_TABLE = 'urls_table'
        dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.table = dynamodb.Table(self.URLS_TABLE)
        self.dynamodbstreamsclient = boto3.client('dynamodbstreams')

    def _insert_urls(self, urls: list):
        resp = ''
        for u in urls:
            resp = self.client.put_item(
                TableName=self.URLS_TABLE,
                Item={
                    'url': {'S': u.url},
                    'domain': {'S': u.domain},
                    'subdomain': {'S': u.subdomain},
                    'url_type': {'S': u.url_type},
                    'time_requested': {'S': str(u.time_requested)},
                    'requesting_user': {'S': '' if u.requesting_user is None else u.requesting_user},
                    'bucket_id': {'S': ''},
                    'data_class': {'S': ''},
                    'child_urls': {'L': []},
                    'ttl': {'N': str(u.ttl)}
                }   
            )
        print('INSERT URLS: ', resp)
        return resp

    def _update_urls(self, urls: list):
        print('EXISTING URLS: ', urls)

    def upsert_urls(self, urls):
        new_urls = []
        existing_urls = []
        for u in urls['parsed_urls']:
            try:
                response = self.table.get_item(
                    Key={
                        'url': u.url
                    }
                )
                item = response['Item']
                if item:
                    existing_urls.append(u)
                print('#####', item)
            except KeyError as err:
                new_urls.append(u)
        self._update_urls(existing_urls)
        self._insert_urls(new_urls)

    def _read_stream(self):
        list_streams = self.dynamodbstreamsclient.list_streams(
            TableName=self.URLS_TABLE,
            Limit=100,
#            ExclusiveStartStreamArn='string'
        )
        stream_arn = list_streams['Streams'][0]['StreamArn']

        describe_stream = self.dynamodbstreamsclient.describe_stream(
#            ExclusiveStartShardId = 'LATEST',
#           "Limit": number,
            StreamArn = stream_arn
        )
#        response = self.dynamodbstreamsclient.get_records(
#            ShardIterator='LATEST',
#            Limit=100
#        )

        print('LIST_STREAMS', list_streams)
        print('STREAM_ARN', stream_arn)
        print('DESCRIBE_STREAMS', describe_stream)

if __name__ == '__main__':
    db = DBUtils()
    db._read_stream()
            