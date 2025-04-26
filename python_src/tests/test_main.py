import unittest
import main
import social_publish_linkedin

class TestMain(unittest.TestCase):

    def test_process_event(self):
        event = {}
        result = main.process_event(event, None)
        self.assertIsNone(result)

    def test_remove_html(self):
        text_with_html = "<div class=\"content\"><p>In this article ... which is 2025-04.<br>The content will be as follow:</p><ul><li>Prerequisites...</li><li>Oauth2 in Action</li><li>URN</li><li>content</li></ul></div>"
        result = social_publish_linkedin.remove_html_tags_with_newlines(text_with_html)
        print(result)
        self.assertEqual("In this article ... which is 2025-04.\nThe content will be as follow:\n - Prerequisites...\n - Oauth2 in Action\n - URN\n - content",result)

if __name__ == '__main__':
    unittest.main()