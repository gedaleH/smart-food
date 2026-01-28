from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Requirement(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)  # auto-incrément
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default="")
    proposition_id = db.Column(db.Integer, nullable=False)

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

    def to_requirement(self, quantity : int):
        return Requirement(name=self.name, description=self.description, quantity=quantity, proposition_id=self.id)

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