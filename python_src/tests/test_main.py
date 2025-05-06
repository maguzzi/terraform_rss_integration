import unittest
import main
import social_publish_linkedin

class TestMain(unittest.TestCase):

    #actual integration, runs on AWS!
    def test_process_event(self):
        event = {}
        result = main.process_event(event, None)
        self.assertIsNone(result)

    #template test
    def test_template(self):
        processed_post = {
            "summary":"abcdef"
        }
        print(social_publish_linkedin.prepare_text(processed_post,"ghijkl"))

         

    #only for reading the whole post
    #def test_full_text_conversion(self):
    #    rss_url = main.get_rss_url() # TODO maybe mock?
    #    print(f"rss_url: {rss_url}")
    #    full_text = main.process_latest_rss_post(rss_url)["summary"]
    #    result2 = social_publish_linkedin.remove_html_tags_with_newlines(full_text)
    #    print(result2)

    #def test_remove_html_to_spaces(self):
    #    self.maxDiff=None

        #text_with_html = """<p>In this article we’ll explore a RSS to social (e.g. LinkedIn) integration using AWS Lambda with Python. We’ll use Amazon Translate to provide the content of the post in Italian for the social platform. The architecture will be defined via Terraform. We’ll proceed as follows:</p>
#<ul>
#<li>Definition of the Lambda infrastructure in Terraform<ul>
#<li>How Terraform manages python code</li>
#</ul>
#</li>
#<li>Python software components<ul>
#<li>Production code</li>
#<li>Unit and integration test code</li>
#</ul>
#</li>
#<li>Integration examples</li>
#<li>Upcoming improvements</li>
#</ul>"""
#        result1 = social_publish_linkedin.remove_html_tags_with_newlines(text_with_html)
#        print(f"***{result1}***")
        
#        self.assertEqual("""In this article we’ll explore a RSS to social (e.g. LinkedIn) integration using AWS Lambda with Python. We’ll use Amazon Translate to provide the content of the post in Italian for the social platform. The architecture will be defined via Terraform. We’ll proceed as follows:

#Definition of the Lambda infrastructure in Terraform
#How Terraform manages python code

#Python software components
#Production code
#Unit and integration test code

#Integration examples
#Upcoming improvements""",result1)

#    def test_remove_html_preserve_links(self):
#        text_with_html = "text before <a href=\"link\">link text</a> text after"
#        result = social_publish_linkedin.remove_html_tags_with_newlines(text_with_html)
#        self.assertEqual("text before link text text after",result)

#    def test_escape_special_chars(self):
#        text_with_html = "text before (this will be written) text after"
#        result = social_publish_linkedin.escape_special_chars(text_with_html)
#        self.assertEqual("text before \\(this will be written\\) text after",result)

if __name__ == '__main__':
    unittest.main()