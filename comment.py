
class Comment:
    text = "" #to store the text of the comment
    path = "" #to store the XPath of each comment

    def __init__(self,text,path):
        self.text = text
        self.path = path

class Post:
    link = "" #stores the link of the post
    image_loc = ""  # stores the image of the post

    def __init__(self):
        self.link = ""
        self.image_loc = ""

    def get_image(self):
        return self.image_loc
