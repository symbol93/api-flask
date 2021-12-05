import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from utils import insert_db, get_db, update_db, delete_db

''' CRUD Operations
'''

'''
INSERT ENDPOINT 
first element path is the name of the table that we want to populate
'''


@app.route('/menu/add', methods=['POST'])
@app.route('/category/add', methods=['POST'])
@app.route('/item/add', methods=['POST'])
@app.route('/group_option/add', methods=['POST'])
@app.route('/option_addon/add', methods=['POST'])
def insert_db_endpoint():
    try:
        json = request.args
        table_name = request.path.split('/')[1]
        rez = insert_db(table_name, json)
        if not rez:
            respone = jsonify('%s added successfully!' % table_name)
            respone.status_code = 200
            return respone
        else:
            return jsonify(rez)
    except Exception as e:
        return jsonify(str(e))


'''
GET ENDPOINT 
first element path is the name of the table that we want to get
params:
    columns : string with comma separated with the names of the columns that we want to receive e.g : columns : 'name','description'
'''


@app.route('/menu', methods=['GET'])
@app.route('/menu/<int:id>', methods=['GET'])
@app.route('/category', methods=['GET'])
@app.route('/category/<int:id>', methods=['GET'])
@app.route('/item', methods=['GET'])
@app.route('/item/<int:id>', methods=['GET'])
@app.route('/group_option', methods=['GET'])
@app.route('/group_option/<int:id>', methods=['GET'])
@app.route('/option_addon', methods=['GET'])
@app.route('/option_addon/<int:id>', methods=['GET'])
def get_db_endpoint(id=False):
    try:
        columns = '*'
        if 'columns' in request.args:
            columns = request.args['columns']
        respone = jsonify(get_db(request.path.split('/')[1], columns, id))
        respone.status_code = 200
        return respone
    except Exception as e:
        return jsonify(str(e))


@app.route('/menu/update', methods=['PUT'])
@app.route('/category/update', methods=['PUT'])
@app.route('/item/update', methods=['PUT'])
@app.route('/group_option/update', methods=['PUT'])
@app.route('/option_addon/update', methods=['PUT'])
def update_db_endpoint():
    try:
        json = dict(request.args)
        if 'id' in json:
            id = json['id']
            del json['id']
            table_name = request.path.split('/')[1]
            rez = update_db(table_name, json, id)
            if not rez:
                respone = jsonify('%s updated successfully!' % table_name)
                respone.status_code = 200
                return respone
            else:
                return jsonify(rez)
        else:
            return not_found()
    except Exception as e:
        return jsonify(str(e))


@app.route('/menu/delete/<int:id>', methods=['DELETE'])
@app.route('/category/delete/<int:id>', methods=['DELETE'])
@app.route('/item/delete/<int:id>', methods=['DELETE'])
@app.route('/group_option/delete/<int:id>', methods=['DELETE'])
@app.route('/option_addon/delete/<int:id>', methods=['DELETE'])
def delete_db_endpoint(id):
    try:
        table_name = request.path.split('/')[1]
        rez = delete_db(table_name, id)
        if not rez:
            respone = jsonify('%s deleted successfully!' % table_name)
            respone.status_code = 200
            return respone
        else:
            return jsonify(rez)
    except Exception as e:
        return jsonify(str(e))


@app.route('/get_menu/<int:id>', methods=['GET'])
def get_menu_json(id):
    try:
        rez = get_db('menu', "id,currency", id)
        join_category = "LEFT JOIN menu m on c.menu_id = m.id "
        where_category = "WHERE m.id = %s" % id
        categories = get_db('category c', "c.id,c.name,c.description", False, join_category, where_category)
        for category in categories:
            join_items = "LEFT JOIN category c on c.id = i.category_id"
            where_items = "WHERE c.id = %s" % category['id']
            items = get_db('item i', "i.id,i.name,i.description,i.price", False, join_items, where_items)
            for item in items:
                join_groups = "LEFT JOIN item i on i.id = g.item_id"
                where_groups = "WHERE i.id = %s" % item['id']
                groups = get_db('group_option g', "g.id,g.name,g.required", False, join_groups, where_groups)
                for group in groups:
                    join_options = "LEFT JOIN group_option g on g.id=o.group_id"
                    where_options = "WHERE g.id = %s" % group['id']
                    options = get_db('option_addon o', "o.id,o.name,o.price", False, join_options, where_options)
                    group['options'] = options
                    group['required'] = group['required'] == 1 and True or False
                item['groups'] = groups
            category['items'] = items
            join_groups_category = "LEFT JOIN category c on c.id = g.category_id"
            where_groups_category = "WHERE c.id = %s" % category['id']
            groups_category = get_db('group_option g', "g.id,g.name,g.required", False, join_groups_category, where_groups_category)
            for group in groups_category:
                join_options = "LEFT JOIN group_option g on g.id=o.group_id"
                where_options = "WHERE g.id = %s" % group['id']
                options = get_db('option_addon o', "o.id,o.name,o.price", False, join_options, where_options)
                group['options'] = options
                group['required'] = group['required'] == 1 and True or False
            category['groups'] = groups_category
        rez['categories'] = categories
        response = jsonify(rez)
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify(str(e))


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()
