resource "aws_dynamodb_table" "quotes" {
  name         = "daily-warhammer-quotes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "quote_id"

  attribute {
    name = "quote_id"
    type = "S"
  }
}
