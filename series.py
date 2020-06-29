import json
import uuid 

'''
Domain model for medium-harvester.
The structure is:

- Series            # base object
    id              # id 
    name            # name or title 
    img_url         # bakground image of medium series if available
    uber_mkdwn      # Markdown representing the entire post in one place
    - Section       # list of section objects denoted by section in the HTML. A section is either a page in series or <placeholder> in a post
        id          # id
        mkdwn       # markdown for a particular section 
        - Content   # content object. Typ[ically this is a text instance in a section e.g. one paragraph in a post
        id          # id
        type        # text, img or url 
        text        # text
        url         # url in case of imge or href 

'''

class Series:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.name = None 
        self.img_url = None 
        self.sections = None 
        self.uber_mkdwn = None
    
    def __str__(self):
        return f'ID: {self.id}\nName: {self.name} \nImage URL: {self.img_url} \nSections: {self.sections}'

    def to_json_str(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_json(self):
        return json.loads(json.dumps(self, default = lambda o: o.__dict__))

    def pretty_print_json(self):
        return json.dumps(json.loads(json.dumps(self, default = lambda o: o.__dict__)), indent = 4)


class Section:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.contents = None 
        self.mkdwn = None
    
    def __str__(self):
        return f'ID: {self.id}\nContents: {self.contents}'

class Content:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.type = None
        self.text = None 
        self.url = None # Only applicable for URL's or images

    def __str__(self):
        return f'ID: {self.id}\nText: {self.text}'

def populate_test():
    s = Series()
    s.id = 1
    s.name = 'Series name'
    s.img_url = None 
    # s.sections 

    section = Section()
    section.id = 1

    content = Content()
    content.id = 1
    content.type = 'Text'
    content.text = 'Some text'

    section.contents.append(content)
    s.sections.append(section)

    json_string = s.to_json_str()
    print(type(json_string))
    json_object = s.to_json()
    print(type(json_object))
    print(json_object)

    print(s.pretty_print_json())



if __name__ == '__main__':
    populate_test()



