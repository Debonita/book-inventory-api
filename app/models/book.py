class Book:
    def __init__(self,id:str,title:str,author:str,genre:str,price:float,available:bool=True):
        self.id=id
        self.title=title
        self.author=author
        self.genre=genre
        self.price=price
        self.available=available
    
    def to_dict(self):
        return {
            "id": self.id,
            "title":self.title,
            "author":self.author,
            "genre":self. genre,
            "price":self.price,
            "available":self.available
        }
    