resource "aws_dynamodb_table" "processed_post" {
  name         = "processed_post"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "rss_id"
  range_key = "post_id"

  attribute {
    name = "rss_id"
    type = "S"
  }

  attribute {
    name = "post_id"
    type = "S"
  }

}