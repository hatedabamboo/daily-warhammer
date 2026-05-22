output "lambda_arn" {
  value = aws_lambda_function.bot.arn
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.quotes.name
}

output "github_actions_role_arn" {
  description = "Set this as the AWS_ROLE_ARN secret in your GitHub repository"
  value       = aws_iam_role.github_actions.arn
}
