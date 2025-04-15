import json
from flask import Flask, jsonify, request
import pandas as pd

api = Flask(__name__)

kda_data = pd.read_csv('kda_data.txt', index_col=0, sep=' ')
print(f"from flask server: {kda_data}")

# returns specified player's kda; if none specified, then returns every player's kda
@api.route('/kda_data', methods=['GET'])
def get_player_data():
    player = request.args.get('player')
    if player == None:
        return kda_data.to_json(orient="index")
    else:
        return kda_data.loc[player].to_json(orient="index")

if __name__ == '__main__':
   api.run(port=5000)