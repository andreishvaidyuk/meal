# https://www.themealdb.com/api.php
# https://www.thecocktaildb.com/api.php

from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from http import HTTPStatus

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")


class Meal:
    url = "https://www.themealdb.com/api/json/v1/1"

    def about(self, request: Request):
        return template.TemplateResponse("about.html", {"request": request})

    def greeting(self, request: Request):
        """
        Return greeting page
        :param request:
        :return:
        """
        return template.TemplateResponse("greating.html", {"request": request})

    def get_meal_by_name(self, request, name):
        """
        Return meal detail info in dictionary. Dictionary will parsed on HTML side
        :param request:
        :param name: Meal name
        :return: Meal detail dictionary
        """
        route = self.url + '/search.php?s=' + name
        response = requests.get(route)
        if response.status_code == HTTPStatus.OK:
            result = response.json()['meals'][0]
            return template.TemplateResponse("meal_detail.html", {"request": request, "meal_detail": result})
        else:
            return "Sorry. Requested page not found."

    def get_categories(self, request):
        """
        Return categories description in dictionary.  Dictionary will parsed on HTML side
        :param request:
        :return: Categories detail dictionary
        """
        route = self.url + '/categories.php'
        response = requests.get(route)
        if response.status_code == HTTPStatus.OK:
            result = response.json()["categories"]
            return template.TemplateResponse("categories.html", {"request": request, "categories": result})
        else:
            return "Sorry. Requested page not found."

    def get_list(self, request, alias):
        """
        Return list of all Categories, Area, Ingredients
        :param alias: aliases: a - Area, c - Categories, i - Ingredients
        :return:
        """
        route = self.url + '/list.php?' + alias + '=list'
        response = requests.get(route)
        if response.status_code == HTTPStatus.OK:
            result = response.json()['meals']
            return template.TemplateResponse("list.html", {"request": request, "list": result, "alias": alias})
        else:
            return "Sorry. Requested page not found."

    def get_filtered(self, request,  alias, name):
        route = self.url + '/filter.php?' + alias + '=' + name
        response = requests.get(route)
        if response.status_code == HTTPStatus.OK:
            result = response.json()["meals"]
            return template.TemplateResponse("filter.html", {"request": request, "filtered_data": result, "filter": name})
        else:
            return "Sorry. Requested page not found."


meal = Meal()


@app.get("/")
def get_greeting(request: Request):
    return meal.greeting(request)

@app.get("/about")
def get_greeting(request: Request):
    return meal.about(request)

# List all meal categories
@app.get("/categories")
def get_categories(request: Request):
    return meal.get_categories(request)


# List all Categories, Area, Ingredients
@app.get("/list/{alias}")
def get_list(request: Request, alias):
    return meal.get_list(request, alias)


# Filter by main ingredient
@app.get("/filter/{alias}/{name}")
def get_filtered_list(request: Request, alias, name):
    return meal.get_filtered(request, alias, name)


# Search meal by name
@app.get("/{name}")
def get_meal(request: Request, name: str):
    return meal.get_meal_by_name(request, name)
