import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from app.models import Recipe, User, Rating

MOCK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'mock_data')


def load(model):
    with open(os.path.join(MOCK_DATA_DIR, '{}.json'.format(model.__name__.lower()))) as content:
        data_list = json.load(content)

    for data in data_list:
        model.query.create(**data)


if __name__ == '__main__':
    load(Recipe)
    load(User)
    load(Rating)
