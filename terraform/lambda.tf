data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../dist/package"
  output_path = "${path.module}/../dist/lambda.zip"
}

resource "aws_lambda_function" "bot" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "daily-warhammer-bot"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "src.handler.handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  timeout          = 30
  memory_size      = 512

  environment {
    variables = {
      DYNAMODB_TABLE   = aws_dynamodb_table.quotes.name
      BLUESKY_HANDLE   = var.bluesky_handle
      BLUESKY_PASSWORD = var.bluesky_password
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.bot.function_name}"
  retention_in_days = 14
}
