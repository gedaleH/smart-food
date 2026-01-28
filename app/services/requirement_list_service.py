from copy import copy

from app.models.models import Requirement, Ci


def generate_list_from_cis(ci_set : set[Ci]):
    requirement_list : list[Requirement] = []
    for ci in ci_set:
        for req in ci.requirements:
            if any(existing_req.id == req.id for existing_req in requirement_list):
                for existing_req in requirement_list:
                    if existing_req.id == req.id:
                        existing_req.quantity += req.quantity
            else:
                requirement_list.append(copy(req))

    return requirement_list
