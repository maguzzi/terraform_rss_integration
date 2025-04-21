resource "aws_lambda_function" "rss_parser" {
  filename      = data.archive_file.rss_parser_zip.output_path
  function_name = "get_rss_content"
  role          = aws_iam_role.lambda_role.arn
  handler       = "rss_parser.handler"
  runtime       = "python3.13"
  timeout       = 15
  memory_size   = 128
  publish       = false

  environment {
    variables = {
      RSS_URL      = var.rss_url
      ACCESS_TOKEN = var.access_token
      PROFILE_ID   = var.profile_id
    }
  }

  layers = [aws_lambda_layer_version.python_deps.arn]
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "IAM policy for Lambda execution"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_layer_version" "python_deps" {
  filename            = "target/python_deps.zip"
  layer_name          = "python_deps"
  compatible_runtimes = ["python3.13"]
  depends_on          = [data.archive_file.python_deps]
}

data "archive_file" "rss_parser_zip" {
  type        = "zip"
  source_dir  = "lambda_functions/rss_parser"
  output_path = "target/rss_parser.zip"
}

data "archive_file" "python_deps" {
  type        = "zip"
  source_dir  = "./python_deps"
  output_path = "./target/python_deps.zip"
}
