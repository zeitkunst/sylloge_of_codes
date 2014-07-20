from models import DBSession, Curator, Group, GroupInfo

def groupfinder(userid, request):
    session = DBSession()
    curator = session.query(Curator).join(Curator.groups).join(Group.group_info).filter(Curator.id == userid).one()

    groupNames = []
    if (curator is not None):
        groups = curator.groups
        for group in groups:
            groupNames.append("group:" + group.group_info.group_name)
    
    return groupNames
