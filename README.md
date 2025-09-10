
data-collectors
Various collectors library configured by JSON configuration.

SW-WB Setup & Test

SETUP
1) MongoDB collectors
{
    "name" : "sr-wb-RabbitToKafka",
    "dest" : {
        "name" : "Kafka",
        "host" : "localhost",
        "port" : 9092,
        "classname" : "KfkProducer",
        "topicname" : "app",
        "role" : "Producer"
    },
    "source" : {
        "name" : "Rabbit q input",
        "host" : "localhost",
        "port" : 5672,
        "classname" : "RabbitConsumer",
        "queuename" : "Orchestrator",
        "role" : "Listener"
    }
}

2) action: Basic Service Operations

3) MongoDB playbookCondition
{
    "_id" : ObjectId("665842a46e0a4e65abc1f6ce"),
    "action" : "Basic Service Operations",
    "playbookName" : "SR_WB",
    "andCondition" : [
        {
            "functionName" : "strEQ",
            "payloadFieldName" : "Source_SysName",
            "arg" : "WB"
        },
        {
            "functionName" : "strEQ",
            "payloadFieldName" : "action",
            "arg" : "Basic Service Operations"
        }
    ],
    "orCondition" : [
    ]
}
{
    "_id" : ObjectId("665842a46e0a4e65abc1f6ce"),
    "action" : "Basic Service Operations",
    "playbookName" : "SR_WB",
    "andCondition" : [
        {
            "functionName" : "strEQ",
            "payloadFieldName" : "Source_SysName",
            "arg" : "SR"
        },
        {
            "functionName" : "strEQ",
            "payloadFieldName" : "action",
            "arg" : "Basic Service Operations"
        }
    ],
    "orCondition" : [
    ]
}

4) MongoDB playbookTemplate: SR_WB
{
    "_id" : ObjectId("666fff1f900064578c679de6"),
    "name" : "SR_WB",
    "status" : "new",
    "category" : "wait",
    "_class" : "com.securegion.eventanalyzer.model.Playbook",
    "output" : "\n",
    "playbookItemList" : [
        {
            "_id" : "1",
            "type" : "rabbitMqSendMessage",
            "status" : "new",
            "output" : "",
            "server" : "localhost",
            "queueName" : "WB_IN"
        },
        {
            "_id" : "2",
            "type" : "waitForResume",
            "status" : "new",
            "output" : "",
            "until" : {
                "andCondition" : [
                    {
                        "functionName" : "strEQlower",
                        "payloadFieldName" : "Source_SysName",
                        "arg" : "WB"
                    },
                    {
                        "functionName" : "strEQlower",
                        "payloadFieldName" : "ActionType",
                        "arg" : "result"
                    }
                ]
            }
        },
        {
            "_id" : "3",
            "type" : "rabbitMqSendMessage",
            "status" : "new",
            "output" : "",
            "server" : "localhost",
            "queueName" : "SR_IN"
        },
        {
            "_id" : "4",
            "type" : "echo",
            "data" : "SR_WB is DONE",
           "status" : "new",
            "output" : ""
        }
    ]
}

TEST
Run 3 apps:
1) analyst-products\components\collectors\data-collectors
2) analyst-products\components\event-analyzer 
3) analyst-products\components\playtbooks 

1.a) publish SR RabbitMQ message (Queue Orchestrator):
{
  "DateTime": 1721210304914.2593,
  "ActionType": "operation",
  "Source_SysName": "SR",
  "Severity ": "High",
  "Payload": {
    "bucket_name": "test",
    "dsm_path": "E2E/DSM",
    "ortho_path": "E2E/Orthophoto",
    "output_path": "E2E/output/lod_1_after_filtering.shp"
  },
  "Source_SysModule": "CLEANER",
  "Description": "finished extraction",
  "Action": "operation"
}
1.b) WB REPLY: publish WB RabbitMQ message:
{
  "DateTime": 1721210304914.2593,
  "ActionType": "result",
  "Source_SysName": "WB",
  "Severity ": "High",
  "Payload": {
    "bucket_name": "test",
    "dsm_path": "E2E/DSM",
    "ortho_path": "E2E/Orthophoto",
    "output_path": "E2E/output/lod_1_after_filtering.shp"
  },
  "Source_SysModule": "CLEANER",
  "Description": "finished extraction",
  "Correlation_id": "ce3fe5c4-d5de-43d6-96a6-10dcb9eba685", <<== PUT THE RIGHT Correlation_id
  "Action": "result"
}
"# operator" 
