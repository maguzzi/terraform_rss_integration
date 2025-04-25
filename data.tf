data "archive_file" "python_src" {
  type        = "zip"
  source_dir  = "python_src"
  output_path = "target/python.zip"
}

data "archive_file" "python_deps" {
  type        = "zip"
  source_dir  = "./python_deps"
  output_path = "./target/python_deps.zip"
}