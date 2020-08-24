# Product Vision Document
- [PVD Link via Google Drive](https://docs.google.com/document/d/1knAudgln1EaXTWT0zidmijN8Yyaqc2OoOcUgqC702SM/edit?usp=sharing)

# Flask API
https://med-cab4.herokuapp.com/
- A FLASK web application that returns the Effect and Flavor request with a recommendation for a strain of Cannabis to try. 

- /predict = returns recommendation
- /trending = returns top recommended strain 
- /predict_medical = (coming soon!) return recommend strain based on medical conditions

# Setup
- Activate the virtual environment with 
```
pipenv shell
```
- Launch the app inside the virtual environment 
```
FLASK_APP=app.py flask run
```


# Use Example 
- GET a json response with 
```
{
    'effect':'Creative', 
    'flavor':'Apple'
    }
```

```
>>> [{"description":{"0":"Alien Sour Apple is a sativa-dominant hybrid...}]
```
- Or using URL parameters

https://med-cab4.herokuapp.com/predict?effect=Creative&flavor=Apple

- note: when assigning key:value pairs, use lowercase 'key' and first letter uppercase 'value'






