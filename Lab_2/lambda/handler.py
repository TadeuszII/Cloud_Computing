import html
import os
import boto3

endpoint_url = os.environ.get("AWS_ENDPOINT_URL", "http://localstack:4566")
s3 = boto3.client("s3", endpoint_url=endpoint_url)

BUCKET_NAME = "raport-koszykow-templates"
TEMPLATE_KEY = "template.html"


def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    imie = params.get("imie", "").strip()

    if not imie:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": "Błąd 400: Podaj niepusty parametr 'imie' w adresie URL, np. ?imie=Jan"
        }

    obj = s3.get_object(Bucket=BUCKET_NAME, Key=TEMPLATE_KEY)
    template_html = obj["Body"].read().decode("utf-8")

    safe_imie = html.escape(imie, quote=True)
    result_html = template_html.replace("{{IMIE}}", safe_imie)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": result_html
    }