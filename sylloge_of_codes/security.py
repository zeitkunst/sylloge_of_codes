USERS = {"curator": "curator",
        "viewer": "viewer"}
GROUPS = {"curator": ["group:curators"]}

def groupfinder(userid, request):
    if (userid in USERS):
        return GROUPS.get(userid, [])


