#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    try:
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return jsonify(bakeries), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    try:
        bakery = Bakery.query.get(id)
        if bakery:
            return jsonify(bakery.to_dict()), 200
        else:
            return jsonify({'error': 'Bakery not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
        return jsonify(baked_goods_serialized), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    try:
        most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if most_expensive:
            return jsonify(most_expensive.to_dict()), 200
        else:
            return jsonify({'error': 'No baked goods found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)