data "aws_iam_policy_document" "lambda_exec_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_exec_cloudwatch" {
  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

data "aws_iam_policy_document" "lambda_exec_dynamodb" {
  statement {
    sid    = "DynamoDB"
    effect = "Allow"
    actions = [
      "dynamodb:Scan",
      "dynamodb:UpdateItem",
    ]
    resources = [aws_dynamodb_table.quotes.arn]
  }
}

data "aws_iam_policy_document" "scheduler_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "scheduler_invoke_lambda" {
  statement {
    sid       = "InvokeLambda"
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.bot.arn]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "daily-warhammer-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_exec_assume_role.json
}

resource "aws_iam_policy" "lambda_exec_cloudwatch" {
  name   = "daily-warhammer-lambda-cloudwatch"
  policy = data.aws_iam_policy_document.lambda_exec_cloudwatch.json
}

resource "aws_iam_role_policy_attachment" "lambda_exec_cloudwatch" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_exec_cloudwatch.arn
}

resource "aws_iam_policy" "lambda_exec_dynamodb" {
  name   = "daily-warhammer-lambda-dynamodb"
  policy = data.aws_iam_policy_document.lambda_exec_dynamodb.json
}

resource "aws_iam_role_policy_attachment" "lambda_exec_dynamodb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_exec_dynamodb.arn
}

resource "aws_iam_role" "scheduler" {
  name               = "daily-warhammer-scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume_role.json
}

resource "aws_iam_policy" "scheduler_invoke_lambda" {
  name   = "daily-warhammer-scheduler-invoke-lambda"
  policy = data.aws_iam_policy_document.scheduler_invoke_lambda.json
}

resource "aws_iam_role_policy_attachment" "scheduler_invoke_lambda" {
  role       = aws_iam_role.scheduler.name
  policy_arn = aws_iam_policy.scheduler_invoke_lambda.arn
}
