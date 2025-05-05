resource "aws_iam_role" "rss_to_linkedin_role" {
  name = "rss_to_linkedin_role"

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

resource "aws_iam_policy" "rss_to_linkedin_policy" {
  name        = "rss_to_linkedin_policy"
  description = "IAM policy for Lambda execution"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect : "Allow",
        Action : [
          "translate:*"
        ],
        "Resource" : "*"
      },
      {
        Effect : "Allow",
        Action : [
          "dynamodb:*"
        ],
        "Resource" : aws_dynamodb_table.processed_post.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rss_to_linkedin_policy_attachment" {
  role       = aws_iam_role.rss_to_linkedin_role.name
  policy_arn = aws_iam_policy.rss_to_linkedin_policy.arn
}