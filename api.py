import json
from flask import Flask, jsonify, request
import pandas as pd

api = Flask(__name__)

player_data = pd.read_csv('player_data.txt', index_col=0, sep=' ')
print(player_data)

@api.route('/player_data', methods=['GET'])
def get_player_data():
    return player_data.to_json(orient="index")

if __name__ == '__main__':
   api.run(port=5000)