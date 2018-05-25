### https://youtu.be/Avunr6oTWqQ
# Light

## Description
This project allows you to change your city for the better side, reporting us about faulty flashlights in our city
## Installation
### Getting the code
```bash
$ git clone https://github.com/Rosovskyy/courseWorkBySerhiyRosovskyy
$ python -m pip install pymongo
$ python -m pip install flask
```
### Database
#### Linux
```bash
$ sudo apt-key adv —keyserver hkp://keyserver.ubuntu.com:80 —recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```

## Usage
For the moment it's a program on a local server
```bash
$ cd .../courseWork
$ python3 routes.py
```
### Input data
#### Registration
**username** - your username on the site
**email** - valid email
**password** - your passwords on the site
#### Form
**name** - your real first and second name
**street** - street, where you noticed the idle lamp
### Output data
Json file with such structure:
```
```
## Structure of project
```
├── docs
│   ├── 1stStage.docx
│   ├── ...
|   └── 5thStage.docx
├── helpfulData
|   └── publicUtilities.txt
├── static
|   ├── img
|   ├── admin.css
|   ├── ...
|   └── singup.css
├── templates
|   ├── form.html
|   ├── ...
|   └── thanks.html
├── adt.py
├── regionsMap.py
└── routes.py
```
## License and copyright
© Serhiy Rosovskyy, student of the Ukrainian Catholic University
