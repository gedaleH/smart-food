import random
from copy import copy

from flask import Flask, render_template, request, redirect, url_for

from app.models.models import db, Proposition
from app.services.image_download_service import generate_image_for_req, generate_image_for_ci
from app.services.requirement_list_service import generate_list_from_cis
from app.models.rcp import ci_set, Ci, requirement_set, Requirement

from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_food.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

ci_added_list : set[Ci] = set()
requirement_list = generate_list_from_cis(ci_added_list)

created_ci : Ci = Ci("Nouveau CI", [], 0, "Description du CI")

@app.route('/')
def index():
    return render_template('index.html', ci_list=ci_set, ci_added_list=ci_added_list, requirement_list=requirement_list)

@app.route('/manage_requirements')
def manage_requirements():
    propositions = db.session.query(Proposition).all()
    return render_template('requirements/manage_requirements.html',
                           requirements=propositions,
                           is_from_ci=False)

@app.route('/manage_ci/<int:ci_id>')
def manage_ci(ci_id):
    ci_displayed : Ci = next(ci for ci in ci_set if ci.ci_id == ci_id)
    return render_template('cis/manage_ci.html',
                           ci=ci_displayed,
                           requirements=ci_displayed.requirements,
                           requirements_to_add=requirement_set,
                           is_from_ci=True,
                           is_created=False)

@app.route('/create_ci')
def create_ci():
    return render_template('cis/manage_ci.html',
                           ci=created_ci,
                           requirements=created_ci.requirements,
                           requirements_to_add=requirement_set,
                           is_from_ci=True,
                           is_created=True)

@app.route("/add_ci", methods=["POST"])
def add_ci():
    ci_id = int(request.form["ci_id"])
    ci_to_add = next(ci for ci in ci_set if ci.ci_id == ci_id)
    ci_added_list.add(ci_to_add)

    update_list()

    return redirect(url_for("index"))

@app.route("/remove_ci_from_list", methods=["POST"])
def remove_ci_from_list():
    ci_id = int(request.form["ci_id"])
    ci_to_del = next(ci for ci in ci_set if ci.ci_id == ci_id)
    ci_added_list.discard(ci_to_del)

    update_list()

    return redirect(url_for("index"))

@app.route("/delete_requirement", methods=["POST"])
def delete_requirement():

    proposition_to_delete = Proposition.query.get(int(request.form["id"]))  # récupère l'élément avec id = 1
    db.session.delete(proposition_to_delete)
    db.session.commit()

    return redirect(url_for("manage_requirements"))

@app.route("/create_requirement", methods=["POST"])
def create_requirement():

    name = request.form["name"]
    description = request.form["description"]

    proposition = Proposition(name=name, description=description)
    db.session.add(proposition)
    db.session.commit()

    generate_image_for_req(name,proposition.id)

    return (redirect(url_for("manage_requirements")))


@app.route("/add_requirement_to_ci", methods=["POST"])
def add_requirement_to_ci():
    req_id = int(request.form["req_id"])
    req_to_add = next(req for req in requirement_set if req.req_id == req_id)

    quantity = int(request.form["quantity"])
    req_to_add.quantity = quantity

    ci_id = int(request.form["ci_id"])
    if ci_id != 0 :
        ci_to_modify = next(ci for ci in ci_set if ci.ci_id == ci_id)
    else:
        ci_to_modify = created_ci

    ci_to_modify.requirements = [req for req in copy(ci_to_modify.requirements) if req.req_id != req_id]
    ci_to_modify.requirements.append(req_to_add)

    update_list()

    if ci_id != 0 :
        return redirect(url_for("manage_ci", ci_id=ci_id))
    return redirect(url_for("create_ci"))

@app.route("/delete_requirement_from_ci", methods=["POST"])
def delete_requirement_from_ci():
    req_id = int(request.form["req_id"])

    ci_id = int(request.form["ci_id"])

    if ci_id != 0 :
        ci_to_modify = next(ci for ci in ci_set if ci.ci_id == ci_id)
    else:
        ci_to_modify = created_ci

    ci_to_modify.requirements = [req for req in copy(ci_to_modify.requirements) if req.req_id != req_id]


    update_list()

    if ci_id != 0 :
        return redirect(url_for("manage_ci", ci_id=ci_id))
    return redirect(url_for("create_ci"))

@app.route("/create_requirement_from_ci", methods=["POST"])
def create_requirement_from_ci():
    req_id = random.randint(50, 7000)
    name = request.form["name"]
    quantity = 0
    generate_image_for_req(name,req_id)
    description = request.form["description"] or None
    requirement = Requirement(req_id=req_id, name=name, quantity=quantity, description=description)
    requirement_set.add(requirement)

    req_to_add = next(req for req in requirement_set if req.req_id == req_id)

    quantity = int(request.form["quantity"])
    req_to_add.quantity = quantity

    ci_id = int(request.form["ci_id"])
    if ci_id != 0 :
        ci_to_modify = next(ci for ci in ci_set if ci.ci_id == ci_id)
    else:
        ci_to_modify = created_ci

    ci_to_modify.requirements = [req for req in copy(ci_to_modify.requirements) if req.req_id != req_id]
    ci_to_modify.requirements.append(req_to_add)

    update_list()

    if ci_id != 0 :
        return redirect(url_for("manage_ci", ci_id=ci_id))
    return redirect(url_for("create_ci"))

@app.route("/add_created_ci", methods=["POST"])
def add_created_ci():
    ci_id = random.randint(50, 7000)
    created_ci.ci_id = ci_id

    name = request.form["name"]
    generate_image_for_ci(name, ci_id)

    description = request.form["description"]
    created_ci.name = name
    created_ci.description = description

    ci_set.add(copy(created_ci))

    created_ci.reset_ci()

    return redirect(url_for("index"))


def update_list():
    requirement_list.clear()
    requirement_list.extend(generate_list_from_cis(ci_added_list))

def start_app():
    app.run(debug=True)