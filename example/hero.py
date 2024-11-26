

class Hero():
    def __init__(self,name,level,race):
        self.name=name
        self.level=level
        self.race=race
        self.health =100
    def show_hero(self):
        discription=(self.name +' Level is: '+ f'{self.level} '+'Race is: '+ self.race + ' Health is:' +str(self.health)).title()  
        print(discription)
    def level_up(self):
        self.level +=1
    def set_health(self,new_health):
        self.health=new_health
    
    def move(self):
        print('Herro ' + self.name + 'start moving...')
        

class SuperHero(Hero):
    def __init__(self, name, level, race, magiclevel):
        super().__init__(name, level, race)
        self.magiclevel=magiclevel
        self.__magic=100
    def makemagic(self):
        self.__magic-=10
    def show_hero(self):
        discription=(self.name +' Level is: '+ f'{self.level} '+'Race is: '+ self.race + ' Health is:' +str(self.health) +
                     " Magic is: "+f'{self.__magic}').title() 
        print(discription)
    



myhero1=Hero('vurdalak ',5,'orc ')
myhero2=Hero('alexander ',4,'human ')
myhero1.show_hero()
myhero2.move()
myhero1.level_up()
myhero1.show_hero()

