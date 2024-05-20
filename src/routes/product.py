from flask import Blueprint, g, request

from src.database import db
from src.models.user import User
from src.models.product import Product
from src.utils.check_token import login_required


product_bp = Blueprint('product', __name__)

@product_bp.route('/add-product', methods = ['POST'])
@login_required
def add_new_product():
    product = request.json
    product['user_id'] = g.user.id
    product = Product(**product)
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return request.get_json()


@product_bp.route('/get-product/<product_id>', methods = ['GET'])
@login_required
def get_single_product(product_id):
    product = db.session.query(Product).filter(Product.id==product_id).first()
    if product:
        product_detail = {
            'name':product.name,
            'description':product.description,
            'price':product.price,
            'product_id':product.id
        }
        return product_detail
    return {'error':'product not found'}


@product_bp.route('/edit-product/<product_id>', methods = ['PUT'])
@login_required
def edit_product(product_id):
    if g.user.is_admin:
        product = db.session.query(Product).filter(Product.id==product_id).first()
    else:
        product = db.session.query(Product).filter(Product.id==product_id, Product.user_id==g.user.id).first()

    if product:
        for key,val in request.json.items():
            setattr(product, key, val)
        db.session.commit()
        db.session.refresh(product)
        product = db.session.query(Product).filter(Product.id==product_id).first()  
        product_detail = {
            'name':product.name,
            'description':product.description,
            'price':product.price,
            'product_id':product.id
        }
        return product_detail
    return {'error':'product not found'}


@product_bp.route('/delete-product/<product_id>', methods = ['DELETE'])
@login_required
def delete_product(product_id):
    product = db.session.query(Product).filter(Product.id==product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message':'product is deleted'}
    return {'error':'product not found'}


@product_bp.route("/get-all-product", methods = ['GET'])
@login_required
def get_all_product():
    try:
        user = db.session.query(User).filter(User.id==g.user.id).first()
        if not user.is_deleted and user.is_admin:
            products = db.session.query(Product).all()
            data = []
            for product in products:
                product_detail = {
                    'name':product.name,
                    'description':product.description,
                    'price':product.price,
                    'product_id':product.id
                }
                data.append(product_detail)
            return data
        return {'error':'You do not have permission'}
    except Exception as e:
        return {'error':str(e)}
    

@product_bp.route("/get-user-product", methods = ['GET'])
@login_required
def get_all_user_product():
    try:
        user = db.session.query(User).filter(User.id==g.user.id).first()
        if not user.is_deleted:
            products = db.session.query(Product).filter(Product.user_id==user.id).all()
            data = []
            for product in products:
                product_detail = {
                    'name':product.name,
                    'description':product.description,
                    'price':product.price,
                    'product_id':product.id
                }
                data.append(product_detail)
            return data
        return {'error':'You do not have permission'}
    except Exception as e:
        return {'error':str(e)}