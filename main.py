from flask import Flask, jsonify, request
from fastavro import parse_schema, writer, reader
from io import BytesIO
import json
import random
import string
import time
import base64

app = Flask(__name__)


def generate_random_data(field_type):
    if isinstance(field_type, dict) and field_type["type"] == "array":
        return [generate_random_data(field_type["items"])]
    elif isinstance(field_type, dict) and field_type["type"] == "record":
        return generate_random_avro_data(field_type)
    elif isinstance(field_type, dict) and field_type["type"] == "enum":
        # Handle Enum types
        symbols = field_type["symbols"]
        return random.choice(symbols)
    elif isinstance(field_type, dict) and field_type["type"] == "map":
        # Handle Map types
        key_type = field_type["values"]
        return generate_random_data({"type": key_type})
    elif isinstance(field_type, dict) and field_type["type"] == "fixed":
        # Handle Fixed types
        size = field_type["size"]
        if size > 0:
            byte_data = bytes(random.randint(0, 255) for _ in range(size))
            return base64.b64encode(byte_data).decode("utf-8")[:size]
        else:
            return None
    elif isinstance(field_type, dict) and field_type["type"] == "string":
        return "".join(random.choices(string.ascii_letters, k=10))
    elif isinstance(field_type, dict) and field_type["type"] == "long":
        return random.randint(1, 1000000)
    elif isinstance(field_type, dict) and field_type["type"] == "boolean":
        return random.choice([True, False])
    elif isinstance(field_type, dict) and field_type["type"] == "int":
        return random.randint(1, 100)
    else:
        return None


def generate_random_avro_data(schema):
    random_data = {}
    for field in schema["fields"]:
        field_name = field["name"]
        field_type = field["type"]

        if "default" in field:
            random_data[field_name] = field["default"]
        if isinstance(field_type, list):
            # Handle Union types
            non_null_types = [t for t in field_type if t != "null"]
            if non_null_types:
                random_data[field_name] = generate_random_data(
                    {"type": non_null_types[random.randint(0, len(non_null_types) - 1)]}
                )
        elif field_type == "array":
            # Check if the field is an empty list (simulating optional field)
            value = generate_random_data(field["items"])
            random_data[field_name] = value
        elif field_type == "record":
            # Recursively handle nested records
            nested_data = generate_random_avro_data(field)
            if nested_data is not None:
                random_data[field_name] = nested_data
        elif field_type == "string":
            random_data[field_name] = "".join(
                random.choices(string.ascii_letters, k=10)
            )
        elif field_type == "long":
            random_data[field_name] = random.randint(1, 1000000)
        elif field_type == "boolean":
            random_data[field_name] = random.choice([True, False])
        elif field_type == "int":
            random_data[field_name] = random.randint(1, 100)
        else:
            random_data[field_name] = generate_random_data(field_type)
    return random_data


def get_all_keys(data):
    keys = set()

    if isinstance(data, dict):
        keys.update(data.keys())
        # for value in data.values():
        # keys.update(get_all_keys(value))
    elif isinstance(data, list):
        for item in data:
            keys.update(get_all_keys(item))

    return keys


@app.route("/convert", methods=["POST"])
def convert_avro_to_json():
    try:
        """
        #  Get the entire JSON file
        j_file = request.get_json()
        json_data = json.load(j_file)
        all_keys = get_all_keys(dict(json_data))

        num_objects = None
        avro_schema = None
        for key in all_keys:
            # Get Number of Objects to Create in Json
            if key == "num_objects":
                num_objects = json_data["num_objects"]
                try:
                    num_objects = int(num_objects)
                except:
                    return jsonify({"error": "num_objects must be an integer"})
            # num_objects = request.get_json()["num_objects"]
            # Get Avro schema
            else:
                avro_schema = json_data[key]
                try:
                    avro_schema = json.loads(avro_schema)
                except:
                    return jsonify({"error": "avro_schema must be a valid JSON string"})
            # avro_schema = request.get_json()["schema"]
        """

        # Get Avro schema
        avro_schema = request.get_json()["schema"]

        # Get Number of Objects to Create in Json
        num_objects = request.get_json()["num_objects"]

        # Parse the Avro schema
        parsed_schema = parse_schema(avro_schema)

        # Generate random Avro data based on the schema for 'num_objects' times
        avro_objects = []
        for i in range(num_objects):
            avro_data = generate_random_avro_data(parsed_schema)
            avro_objects.append(avro_data)

            # Introduce a delay based on the loop index
            time.sleep(0.1)

        # Create Avro bytes data
        bytes_data = BytesIO()
        writer(bytes_data, parsed_schema, avro_objects)

        # Reset the bytes_data position to the beginning
        bytes_data.seek(0)

        # Decode Avro bytes to JSON using fastavro's reader function
        json_data = list(reader(bytes_data, parsed_schema))

        return jsonify({"avro_json": json_data})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
