import json
import uuid 

class Series:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.name = None 
        self.img_url = None 
        self.sections = []
    
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
        self.contents = []
    
    def __str__(self):
        return f'ID: {self.id}\nContents: {self.contents}'

class Content:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.type = None 
        self.text = None 

    def __str__(self):
        return f'ID: {self.id}\nType: {self.type}\nText: {self.text}'

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



