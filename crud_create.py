from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheesepizza = MenuItem(
	name = "Cheese Pizza",
	description = "Made with all natural ingredients and fresh mozzarella",
	course = "Entree",
	price = "$8.99",
	restaurant = myFirstRestaurant
	)
session.add(cheesepizza)
session.commit()

firstResult = session.query(Restaurant).first()
firstResult.name

allRestaurants = session.query(Restaurant).all()
for restaurant in allRestaurants:
	print restaurant.name, restaurant.id

items = session.query(MenuItem).all()
for item in items:
	print(item.name)



veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
	print(veggieBurger.id)
	print(veggieBurger.price)
	print(veggieBurger.restaurant.name)
	print("\n")



UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()
print(UrbanVeggieBurger.price)

UrbanVeggieBurger.price = "$2.95"
session.add(UrbanVeggieBurger)
session.commit()


veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
	if veggieBurger.price != "$2.99":
		veggieBurger.price = '$2.99'
		session.add(veggieBurger)
		session.commit()


spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinach)
for spinac in spinach:
	print(spinac.restaurant.name)
	session.delete(spinac)
	session.commit()