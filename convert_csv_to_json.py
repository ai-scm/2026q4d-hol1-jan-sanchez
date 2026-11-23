import boto3
import csv
import io
import json


INPUT_BUCKET = "bld-tseed-workshop-input-semillero-2026-q4"
OUTPUT_BUCKET = "bld-tseed-workshop-output-semillero-2026-q4-d"

INPUT_KEY = "jan-sanchez/users_dataset_100.csv"
OUTPUT_PREFIX = "jan-sanchez/"


def lambda_handler(event, context):
    s3 = boto3.client("s3")

    response = s3.get_object(
        Bucket=INPUT_BUCKET,
        Key=INPUT_KEY
    )

    content = response["Body"].read().decode("utf-8-sig")
    csv_file = io.StringIO(content)
    reader = csv.DictReader(csv_file)

    generated_files = []

    for row_number, row in enumerate(reader, start=1):
        clean_row = {
            key.strip(): value.strip() if value is not None else ""
            for key, value in row.items()
        }

        output_key = (
            f"{OUTPUT_PREFIX}"
            f"users_dataset_100_registro_{row_number}.json"
        )

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=json.dumps(clean_row, ensure_ascii=False),
            ContentType="application/json"
        )

        generated_files.append(output_key)

    print(
        f"CSV leído: s3://{INPUT_BUCKET}/{INPUT_KEY}"
    )
    print(
        f"Archivos generados: {len(generated_files)}"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "source": f"s3://{INPUT_BUCKET}/{INPUT_KEY}",
            "generated": len(generated_files),
            "files": generated_files
        })
    }