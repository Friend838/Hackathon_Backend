# API server
## (Optional) Initialize a python virtual environment
- Install virtualenv package if you don't have
```
pip3 install virtualenv
```
- Create a virtual environment with python 3.10 called "backend" and activate it
```
virtualenv  --python=3.10 backend
source backend/bin/activate
```
- Deactivate environment if you want
```
deactivate
```

## Install requirements
- Install requirements
```
pip install -r requirements.txt
```

## Environment variable
- Change `.env.example` to `.env`
- <b> Do not push a real IP to github </b> 

## Start up api server
```
sh launch.sh
```

## Format python script with black formatter
```
sh format.sh
```