resource "aws_lambda_function" "rss_to_linkedin" {
  filename         = data.archive_file.python_src.output_path
  function_name    = "rss_to_linkedin"
  role             = aws_iam_role.rss_to_linkedin_role.arn
  source_code_hash = data.archive_file.python_src.output_base64sha256
  handler          = "main.process_event"
  runtime          = "python3.13"
  timeout          = 15
  memory_size      = 128
  publish          = false

  environment {
    variables = {
      RSS_URL          = var.rss_url
      ACCESS_TOKEN     = var.access_token
      PROFILE_ID       = var.profile_id
      MESSAGE_TEMPLATE = var.message_template
    }
  }

  layers = [aws_lambda_layer_version.python_deps.arn]
}

resource "aws_lambda_layer_version" "python_deps" {
  filename            = "target/python_deps.zip"
  layer_name          = "python_deps"
  compatible_runtimes = ["python3.13"]
  depends_on          = [data.archive_file.python_deps]
  source_code_hash    = filebase64sha256(data.archive_file.python_deps.output_path)
}

