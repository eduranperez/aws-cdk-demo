const dynamoDb = require('aws-sdk/clients/dynamodb');
const uuid = require('node-uuid');
const tableName = process.env.TABLE_NAME

exports.getAllItemsHandler = async (event, context) => {
    try {
        console.log("Getting all items")
        const params = {
            TableName: tableName,
        };
        const docClient = exports.getDynamoDbDocumentClient();
        
        const response = await docClient.scan(params).promise();

        return {
            'statusCode': 200,
            'body': JSON.stringify({
                items: response
            })
        };
    } catch (err) {
        console.log(err);
        return {
            'statusCode': 500
        }
    }
};

exports.getItemHandler = async (event, context) => {
    try {
        console.log(`Getting item ${itemId}`);
        const itemId = event.pathParameters.itemId;

        const params = {
            TableName: tableName,
            Key: {
              'pk': itemId
            }
        };
        const docClient = exports.getDynamoDbDocumentClient();
        
        const response = await docClient.get(params).promise();

        return {
            'statusCode': 200,
            'body': JSON.stringify({
                item: response
            })
        };
    } catch (err) {
        console.log(err);
        return {
            'statusCode': 500
        }
    }
};

exports.addItemHandler = async (event, context) => {
    try {
        const body = JSON.parse(event.body)
        const name = body.name;
        console.log(`Adding item with name ${name}`);
        const item = {
            'name': name,
            'pk': uuid.v4()
        }

        const params = {
            TableName: tableName,
            Item: item
        };
        const docClient = exports.getDynamoDbDocumentClient();
        
        const response = await docClient.put(params).promise();

        return {
            'statusCode': 200,
            'body': JSON.stringify({
                item: item
            })
        };
    } catch (err) {
        console.log(err);
        return {
            'statusCode': 500
        }
    }
};

exports.getDynamoDbDocumentClient = () => {
    if (process.env.USE_LOCAL_DYNAMODB == "true") {
        console.log('connecting to local instance');
        return new dynamoDb.DocumentClient({'endpoint': 'http://dynamo-local:8000'});
    } else {
        console.log('Connecting to cloud instance');
        return new dynamoDb.DocumentClient();
    }
}
