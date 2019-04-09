class o:
    pass

def dub(s):
    return [(e,e) for e in s]

LocationTypes = o()
LocationTypes.LOCATION_CHOICES = dub(["here", "there"])

TableTypes = o()
TableTypes.TABLE_CHOICES_LOCATION = dub(["hither", "thither"])
TableTypes.LONG = "thither"
TableTypes.TABLE_CHOICES_EVENT = dub(["mine", "yours"])
TableTypes.NO_PREF = "yours"

Duration = o()
Duration.DURATION_CHOICES = dub(["short", "medium", "extra medium"])

ConflictTypes = o()
ConflictTypes.CONFLICT_CHOICES = dub(["nope", "denied", "you dun goofed"])
ConflictTypes.RESTRICTED = "nope"

Tracks = o()
Tracks.TRACK_CHOICES = dub(["choo choo", "jamaican"])

ExpLevels = o()
ExpLevels.EXPERIENCE_CHOICES = dub(["level 1", "level 9001"])
ExpLevels.NOVICE = "level 1"

Status = o()
Status.STATUS_CHOICES = dub(["here today", "gone tomorrow"])

AgeGroups = o()
AgeGroups.AGE_CHOICES = dub(["all", "none"])
AgeGroups.ALL = "all"

EventTypes = o()
EventTypes.EVENT_TYPE_CHOICES = dub(["magic", "more magic"])
EventTypes.GAME = "more magic"

Roles = o()
Roles.ROLE_CHOICES = dub(["yer mom", "teh boss", "blab", "Sam"])
Roles.GM = "yer mom"
Roles.COORDINATOR = "teh boss"
Roles.PANELIST = "blab"
Roles.PLAYER = "Sam"


