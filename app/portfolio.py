from flask import Flask, render_template, request, redirect, url_for

from app.models.models import db, Proposition, Ci, Requirement
from app.services.image_download_service import generate_image_for_req, generate_image_for_ci
from app.services.requirement_list_service import generate_list_from_cis

from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_food.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

ci_added_id_list : set[int] = set()
requirement_list = []


@app.route('/')
def index():
    ci_added_list = db.session.query(Ci).filter(Ci.id.in_(ci_added_id_list)).all()
    all_cis = db.session.query(Ci).all()
    return render_template('index.html', ci_list=all_cis, ci_added_list=ci_added_list, requirement_list=requirement_list)

@app.route('/manage_propositions')
def manage_propositions():
    propositions = db.session.query(Proposition).all()
    return render_template('propositions/manage_propositions.html',
                           propositions=propositions,
                           is_from_ci=False)

@app.route('/manage_ci/<int:ci_id>')
def manage_ci(ci_id):
    ci = db.session.get(Ci, ci_id)
    propositions = db.session.query(Proposition).all()
    return render_template('cis/manage_ci.html',
                           ci=ci,
                           requirements=ci.requirements,
                           propositions=propositions,
                           is_from_ci=True,
                           is_created=False)

@app.route('/create_ci')
def create_ci():
    created_ci : Ci = Ci(name="Nouvelle recette", description="")
    db.session.add(created_ci)
    db.session.commit()
    propositions = db.session.query(Proposition).all()
    return render_template('cis/manage_ci.html',
                           ci=created_ci,
                           requirements=created_ci.requirements,
                           propositions=propositions,
                           is_from_ci=True,
                           is_created=True)

@app.route("/add_ci_to_list", methods=["POST"])
def add_ci_to_list():
    ci_id = int(request.form["ci_id"])
    ci_added_id_list.add(ci_id)

    update_list()

    return redirect(url_for("index"))

@app.route("/remove_ci_from_list", methods=["POST"])
def remove_ci_from_list():
    ci_id = int(request.form["ci_id"])
    ci_added_id_list.discard(ci_id)

    update_list()

    return redirect(url_for("index"))

@app.route("/delete_proposition", methods=["POST"])
def delete_proposition():

    proposition_to_delete = Proposition.query.get(int(request.form["prop_id"]))
    db.session.delete(proposition_to_delete)
    db.session.commit()

    return redirect(url_for("manage_propositions"))

@app.route("/delete_ci", methods=["POST"])
def delete_ci():

    ci_to_delete = db.session.get(Ci, int(request.form["ci_id"]))
    db.session.delete(ci_to_delete)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/create_proposition", methods=["POST"])
def create_proposition():

    name = request.form["name"]
    description = request.form["description"]

    proposition = Proposition(name=name, description=description)
    db.session.add(proposition)
    db.session.commit()

    generate_image_for_req(name,proposition.id)

    return (redirect(url_for("manage_propositions")))


@app.route("/add_requirement_to_ci", methods=["POST"])
def add_requirement_to_ci():

    quantity = int(request.form["quantity"])
    prop_id = int(request.form["prop_id"])
    requirement_to_add : Requirement = Proposition.query.get(prop_id).to_requirement(quantity)

    ci_id = int(request.form["ci_id"])
    ci_to_modify = Ci.query.get(ci_id)

    ci_to_modify.requirements.append(requirement_to_add)

    db.session.commit()

    update_list()

    return redirect(url_for("manage_ci", ci_id=ci_id))

@app.route("/remove_requirement_from_ci", methods=["POST"])
def remove_requirement_from_ci():

    req_id = int(request.form["req_id"])
    ci_id = int(request.form["ci_id"])

    requirement_to_delete = Requirement.query.get(req_id)
    db.session.delete(requirement_to_delete)
    db.session.commit()

    update_list()

    return redirect(url_for("manage_ci", ci_id=ci_id))

@app.route("/create_proposition_and_add_requirement_to_ci", methods=["POST"])
def create_proposition_and_add_requirement_to_ci():

    name = request.form["name"]
    description = request.form["description"]

    proposition = Proposition(name=name, description=description)
    db.session.add(proposition)
    db.session.commit()

    prop_id = proposition.id
    generate_image_for_req(name, prop_id)

    quantity = int(request.form["quantity"])
    requirement_to_add : Requirement = Proposition.query.get(prop_id).to_requirement(quantity)

    ci_id = int(request.form["ci_id"])
    ci_to_modify = Ci.query.get(ci_id)

    ci_to_modify.requirements.append(requirement_to_add)

    db.session.commit()

    update_list()

    return redirect(url_for("manage_ci", ci_id=ci_id))


@app.route("/define_created_ci", methods=["POST"])
def define_created_ci():

    ci_id = request.form["ci_id"]
    name= request.form["name"]

    ci_to_modify = Ci.query.get(ci_id)



    ci_to_modify.name = name
    ci_to_modify.description = request.form["description"]

    generate_image_for_ci(name, ci_id)

    db.session.commit()

    return redirect(url_for("manage_ci", ci_id=ci_id))


def update_list():
    requirement_list.clear()
    ci_added_list = db.session.query(Ci).filter(Ci.id.in_(ci_added_id_list)).all()
    requirement_list.extend(generate_list_from_cis(ci_added_list))

def start_app():
    app.run(debug=True)