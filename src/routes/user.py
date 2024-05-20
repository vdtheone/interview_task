from flask import Blueprint, request, g
from flask_bcrypt import Bcrypt

from src.database import db
from src.models.user import User
from src.utils.check_token import login_required
from src.utils.jwt_token import generate_jwt_tokens


bcrypt = Bcrypt()
user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def create_user():
    try:
        user_details = request.json
        password = user_details.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user_details["password"] = hashed_password
        user = User(**user_details)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return request.get_json()
    except Exception as e:
        return {"error": str(e)}


@user_bp.route("/login", methods=["POST"])
def login():
    try:
        user_detail = request.json
        email = user_detail.get("email")
        password = user_detail.get("password")
        user = db.session.query(User).filter(User.email == email).first()
        if user.is_approved:
            if bcrypt.check_password_hash(user.password, password):
                if not user.is_deleted:
                    return generate_jwt_tokens({"user_id": user.id})
            else:
                return {"error": "Invalid email, password, or account not approved/deleted."}, 401  # Unauthorized
        return {
            "error": "Access Denied: Your profile is pending approval by the administrator. Please wait until your profile is approved before attempting to login."
        }
    except Exception as e:
        return {"error": str(e)}


@user_bp.route("/edit", methods=["PUT"])
@login_required
def edit_user_details():
    try:
        user_details = request.json
        user = db.session.query(User).filter(User.id == g.user.id).first()
        if not user.is_deleted:
            for key, val in user_details.items():
                setattr(user, key, val)
            db.session.commit()
            db.session.refresh(user)
            return {"user": "updated"}
        return {"error": "User not found"}, 404  # Not Found
    except Exception as e:
        return {"error": str(e)}, 500


@user_bp.route("/delete", methods=["DELETE"])
@login_required
def delete_user():
    try:
        user = db.session.query(User).filter(User.id == g.user.id).first()
        if not user.is_deleted:
            user.is_deleted = True
            db.session.commit()
            db.session.refresh(user)
            return {"user": "User deleted"}
        return {"error": "User not found"}, 404  # Not Found
    except Exception as e:
        return {"error": str(e)}, 500


@user_bp.route("/get-user", methods=["GET"])
@login_required
def get_single_user():
    try:
        user = db.session.query(User).filter(User.id == g.user.id).first()
        if not user.is_deleted:
            user_detail = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            return user_detail
        return {"error": "User not found"}, 404  # Not Found
    except Exception as e:
        return {"error": str(e)}, 500


@user_bp.route("/get-all-user", methods=["GET"])
@login_required
def get_all_user():
    try:
        user = db.session.query(User).filter(User.id == g.user.id).first()
        if not user.is_deleted and user.is_admin:
            users = db.session.query(User).all()
            data = []
            for i in users:
                user_detail = {
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                    "email": i.email,
                    "is_admin": i.is_admin,
                    "is_approved": i.is_approved,
                    "is_deleted": i.is_deleted,
                    "created_at": i.created_at,
                    "updated_at": i.updated_at,
                }
                data.append(user_detail)
            return data
        return {"error": "You do not have permission"}
    except Exception as e:
        return {"error": str(e)}, 500


@user_bp.route("/approve-user/<user_id>", methods=["POST"])
@login_required
def admin_approve_user_to_login(user_id):
    try:
        user_flag = request.json
        if g.user.is_admin:
            user = db.session.query(User).filter(User.id == user_id).first()
            if user:
                user.is_approved = user_flag.get("flag")
                db.session.commit()
                db.session.refresh(user)
                return {"message": "user can login"}
        return {"error": "You do not have permission"}
    except Exception as e:
        return {"error": str(e)}, 500
