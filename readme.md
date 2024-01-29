# Avro Data Generator

This Flask application generates random Avro data based on a given schema.

## Concept
The generate_random_data function generates random data for Avro schema types, including arrays, strings, longs, and booleans. The generate_random_avro_data function utilizes this to create a random Avro record based on a given schema, producing a dictionary with field names and corresponding random data. These functions are valuable for generating diverse and synthetic Avro data for testing and development purposes.


## Usage
### Running Locally
Run Virtual Venv and Check Requirements.txt

1. Install the required dependencies:

   ```bash
   pip install flask fastavro
   python app.py
   ```
Application is Available locallly on localhost:8000


 Curl Testing


 1:
```bash
curl -X POST  -H "Content-Type: application/json" -d '{
    "schema": {
        "type": "record",
        "name": "UserSession",
        "fields": [
            {
                "name": "id",
                "type": "string"
            },
            {
                "name": "createdAt",
                "type": "string"
            },
            {
                "name": "userId",
                "type": "string"
            },
            {
                "name": "eventType",
                "type": "string"
            },
            {
                "name": "previousSessionStats",
                "type": {
                    "type": "record",
                    "name": "PreviousSessionStats",
                    "fields": [
                        {
                            "name": "id",
                            "type": "string"
                        },
                        {
                            "name": "sessionDuration",
                            "type": "int"
                        },
                        {
                            "name": "pagesVisited",
                            "type": "int"
                        },
                        {
                            "name": "endType",
                            "type": "string"
                        }
                    ]
                }
            },
            {
                "name": "sessionParams",
                "type": {
                    "type": "record",
                    "name": "SessionParams",
                    "fields": [
                        {
                            "name": "windowInnerWidth",
                            "type": "int"
                        },
                        {
                            "name": "windowInnerHeight",
                            "type": "int"
                        },
                        {
                            "name": "screenWidth",
                            "type": "int"
                        },
                        {
                            "name": "screenHeight",
                            "type": "int"
                        },
                        {
                            "name": "os",
                            "type": "string"
                        },
                        {
                            "name": "osVersion",
                            "type": "int"
                        },
                        {
                            "name": "browser",
                            "type": "string"
                        },
                        {
                            "name": "browserVersion",
                            "type": "string"
                        },
                        {
                            "name": "pixelRatio",
                            "type": "int"
                        },
                        {
                            "name": "platformType",
                            "type": "string"
                        }
                    ]
                }
            },
            {
                "name": "customerProfileInfo",
                "type": {
                    "type": "record",
                    "name": "CustomerProfileInfo",
                    "fields": [
                        {
                            "name": "orderCount",
                            "type": "int"
                        },
                        {
                            "name": "totalOrderBrutPrice",
                            "type": "int"
                        },
                        {
                            "name": "customerRank",
                            "type": "int"
                        }
                    ]
                }
            },
            {
                "name": "additionalParams",
                "type": "string"
            }
        ]
    },
    "num_objects": 5
}' http://localhost:8000/convert


2:
```bash
curl -X POST http://localhost:8000/convert -H "Content-Type: application/json" -d '{
    "schema": {
        "type": "record",
        "name": "ComplexRecord",
        "fields": [
            {
                "name": "id",
                "type": "string"
            },
            {
                "name": "timestamp",
                "type": "long"
            },
            {
                "name": "previousSessionStats",
                "type": {
                    "type": "record",
                    "name": "PreviousSessionStats",
                    "fields": [
                        {
                            "name": "id",
                            "type": "string"
                        },
                        {
                            "name": "endType",
                            "type": "string"
                        }
                    ]
                }
            },
            {
                "name": "arrayOfRecords",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "record",
                        "name": "ArrayRecord",
                        "fields": [
                            {
                                "name": "id",
                                "type": "string"
                            },
                            {
                                "name": "sessionDuration",
                                "type": "int"
                            },
                            {
                                "name": "pagesVisited",
                                "type": "int"
                            },
                            {
                                "name": "endType",
                                "type": "string"
                            }
                        ]
                    }
                }
            }
        ]
    },
    "num_objects": 5
}'

3:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "schema": {
        "type": "record",
        "name": "example",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "age",
                "type": "int"
            },
            {
                "name": "emails",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "name": "email"
                    }
                }
            },
            {
                "name": "address",
                "type": "string"
            }
        ]
    },
    "num_objects": 3
}' http://localhost:8000/convert



4:
```bash
curl -X POST http://localhost:8000/convert -H "Content-Type: application/json" -d '{
    "schema": {
        "type": "record",
        "name": "Person",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "age",
                "type": "int"
            },
            {
                "name": "city",
                "type": "string"
            }
        ]
    },
    "num_objects": 5
}'

5:
```bash
curl -X POST http://localhost:7000/convert -H "Content-Type: application/json" -d '{
    "schema": {
        "type": "record",
        "name": "ComplexRecordWithTypes",
        "fields": [
            {
                "name": "id",
                "type": "string"
            },
            {
                "name": "timestamp",
                "type": "long"
            },
            {
                "name": "previousSessionStats",
                "type": {
                    "type": "record",
                    "name": "PreviousSessionStats",
                    "fields": [
                        {
                            "name": "id",
                            "type": "string"
                        },
                        {
                            "name": "endType",
                            "type": "string"
                        }
                    ]
                }
            },
            {
                "name": "arrayOfRecords",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "record",
                        "name": "ArrayRecord",
                        "fields": [
                            {
                                "name": "id",
                                "type": "string"
                            },
                            {
                                "name": "sessionDuration",
                                "type": "int"
                            },
                            {
                                "name": "pagesVisited",
                                "type": "int"
                            },
                            {
                                "name": "endType",
                                "type": "string"
                            }
                        ]
                    }
                }
            },
            {
                "name": "unionField",
                "type": [
                    "string",
                    "int",
                    "boolean",
                    "null"
                ]
            },
            {
                "name": "enumField",
                "type": {
                    "type": "enum",
                    "name": "ExampleEnum",
                    "symbols": [
                        "SYMBOL1",
                        "SYMBOL2"
                    ]
                }
            }
        ]
    },
    "num_objects": 3
}'




