# Sports Item Catalog
Wep app that display a number of sports and it's items, you can create an account to Create, Update, and Delete items.

## Requirments
Install [Vagrant](https://www.vagrantup.com/downloads.html),  [VirtualBox](https://www.virtualbox.org/wiki/Downloads), and [Python](https://www.python.org/downloads/) 
then you have to install the needed libraries, with this commands


## Download
` git clone *the repo link*` 

## Running
Open your command prompot and type
```
cd *path to your file location*
vagrant up
vagrant ssh
cd /vagrant/catalog/Project4
pip install flask_bcrypt
pip install flask_login
python lotsofcategories.py
Python run.py
```

## JSON Endpoins
-	you can find a json endpoint for all sports categories and in's items at localhost://5000/catalog.json
-	and a specific category endpoint at localhost://5000/catalog.json/<category_name>
-	and a specific item endpoint at localhost://5000/catalog.json/<category_name>/<item_name>
