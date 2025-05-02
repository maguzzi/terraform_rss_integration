variable "rss_url" {
  type        = string
  description = "url for the rss feed"
}

variable "access_token" {
  type        = string
  sensitive   = true
  description = "access token got by linkedin"
}

variable "profile_id" {
  type        = string
  sensitive   = true
  description = "linkedin profile"
}

variable "message_template" {
  type        = string
  description = "template for linkedin message"
  default     = "$translated_text"
}
      