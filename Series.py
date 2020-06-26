import json

class Series:
    def __init__(self) -> None:
        self.id = None 
        self.name = None 
        self.img_url = None 
        self.sections = []
    
    def __str__(self):
        return f'ID: {self.id}\nName: {self.name} \nImage URL: {self.img_url} \nSections: {self.sections}'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class Section:
    def __init__(self) -> None:
        self.id = None 
        self.contents = []
    
    def __str__(self):
        return f'ID: {self.id}\nContents: {self.contents}'

class Content:
    def __init__(self) -> None:
        self.id = None 
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

    json_string = s.to_json()
    json_object = json.loads(json_string)
    print(json_object)



if __name__ == '__main__':
    populate_test()



