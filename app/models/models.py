from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Requirement(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)  # auto-incrément
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default="")

    ci_id = db.Column(db.Integer, db.ForeignKey("cis.id"), nullable=True)

    def __repr__(self):
            return f"<Requirement {self.name}>"

class Proposition(db.Model):
    __tablename__ = "propositions"

    id = db.Column(db.Integer, primary_key=True)  # auto-incrément
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")

    def __repr__(self):
        return f"<Poposition {self.name}>"

class Ci(db.Model):
    __tablename__ = "cis"

    id = db.Column(db.Integer, primary_key=True)  # auto-incrément
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")

    requirements = db.relationship(
        "Requirement",
        backref="ci",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CI {self.name}>"