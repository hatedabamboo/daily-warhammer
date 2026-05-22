resource "aws_scheduler_schedule" "daily" {
  name       = "daily-warhammer"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = var.schedule_expression
  schedule_expression_timezone = var.schedule_timezone

  target {
    arn      = aws_lambda_function.bot.arn
    role_arn = aws_iam_role.scheduler.arn
  }
}
