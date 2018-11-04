from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from categoryproj.database import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(username="Saad Adel", email="saad.adel539@yahoo.com",
             password="123456789", image="static/me.jpg")
session.add(user1)
session.commit()

category1 = Category(name="Soccer", user=user1)

session.add(category1)
session.commit()

item1 = Item(name="Shinguards", description='''
Football boots, called cleats or soccer shoes in North America,[1] are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.
''', category=category1, user=user1)

session.add(item1)
session.commit()


item2 = Item(name="Boots", description='''
Football boots, called cleats or soccer shoes in North America,[1] are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.
''', category=category1, user=user1)

session.add(item2)
session.commit()


item3 = Item(name="Goal", description='''
a goal is a physical structure or area where an attacking team must send the ball or puck in order to score points. In several sports, a goal is the sole method of scoring, and thus the final score is expressed in the total number of goals scored by each team.
''', category=category1, user=user1)

session.add(item3)
session.commit()


category2 = Category(name="BasketBall", user=user1)

session.add(category2)
session.commit()

item1 = Item(name="The Ball", description='''
The Ball
The most important thing for training is the ball. There are certain guidelines which one needs to follow when buying a basketball. For practicing, one can play with a rubber ball. 
''', category=category2, user=user1)

session.add(item1)
session.commit()


item2 = Item(name="Shot Clock", description='''
The offense is allowed a maximum of 24 seconds to have a ball in hand before shooting. These 24 seconds are counted on the shot clock. If the offense fails to shoot a ball that hits the rim, they will lose the possession of the ball to the other team.
''', category=category2, user=user1)

session.add(item2)
session.commit()


item3 = Item(name="Whistle", description='''
The coach or referee uses a whistle to indicate the start or end of a game. S/he can even use the whistle to stop the play in the middle of a game. Whistle also helps to indicate fouls, timeout, or out of bound balls to the players. In order to get the attention of the players, many times coaches use the whistle to gather 
''', category=category2, user=user1)

session.add(item3)
session.commit()


category3 = Category(name="BaseBall", user=user1)

session.add(category3)
session.commit()

item1 = Item(name="Bat", description='''
A rounded, solid wooden or hollow aluminum bat. Wooden bats are traditionally made from ash wood, though maple and bamboo is also sometimes used. Aluminum bats are not permitted in professional leagues, but are frequently used in amateur leagues. Composite bats are also available, essentially wooden bats with a metal rod inside. Bamboo bats are also becoming popular.
''', category=category3, user=user1)

session.add(item1)
session.commit()


item2 = Item(name="Base", description='''
One of four corners of the infield which must be touched by a runner in order to score a run; more specifically, they are canvas bags (at first, second, and third base) and a rubber plate (at home).
''', category=category3, user=user1)

session.add(item2)
session.commit()


item3 = Item(name="Catcher's mitt", description='''
Leather mitt worn by catchers. It is much wider than a normal fielder's glove and the four fingers are connected. The mitt is also better-padded than the standard fielder's glove.
''', category=category3, user=user1)

session.add(item3)
session.commit()


category4 = Category(name="Hockey", user=user1)

session.add(category4)
session.commit()

item1 = Item(name="Shin pads", description='''
A rounded, solid wooden or hollow aluminum bat. Wooden bats are traditionally made from ash wood, though maple and bamboo is also sometimes used. Aluminum bats are not permitted in professional leagues, but are frequently used in amateur leagues. Composite bats are also available, essentially wooden bats with a metal rod inside. Bamboo bats are also becoming popular.
''', category=category4, user=user1)

session.add(item1)
session.commit()


item2 = Item(name="Hockey socks", description='''
One of four corners of the infield which must be touched by a runner in order to score a run; more specifically, they are canvas bags (at first, second, and third base) and a rubber plate (at home).
''', category=category4, user=user1)

session.add(item2)
session.commit()


item3 = Item(name="Skates", description='''
Leather mitt worn by catchers. It is much wider than a normal fielder's glove and the four fingers are connected. The mitt is also better-padded than the standard fielder's glove.
''', category=category4, user=user1)

session.add(item3)
session.commit()


category5 = Category(name="Skating", user=user1)

session.add(category5)
session.commit()

item1 = Item(name="Boots", description='''
Ice skating boots are constructed from stiff leather to provide support to the ankle and foot. The most important thing to consider when buying ice skating boots is the fit. The boot should be snug and your foot should not be able to move around much.
''', category=category5, user=user1)

session.add(item1)
session.commit()


item2 = Item(name="Blades", description='''
Football boots, called cleats or soccer shoes in North America,[1] are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.
''', category=category5, user=user1)

session.add(item2)
session.commit()


item3 = Item(name="Clothing", description='''
There is not a dress code for ice rinks or frozen ponds, but you do want to consider some important aspects when deciding what to wear. You want clothing that stretches and moves with you, such as leotards, tights, stretchy pants and tops.
''', category=category5, user=user1)

session.add(item3)
session.commit()


print "added menu items!"
