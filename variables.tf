variable "rss_url" {
  type        = string
  description = "url for the rss feed"
}

variable "access_token" {
  type        = string
  description = "access token got by linkedin"
}

variable "profile_id" {
  type        = string
  description = "linkedin profile"
}

variable "message_template" {
  type = string
  description = "template for linkedin message"
  default = "$translated_text"
}
      