import datetime
from django.db import models
from django.utils.html import escape
import gamecon.constants as constants
from datetime import datetime

# should these be constants?


class Convention(models.Model):
    name = models.CharField(max_length=40)
    tag = models.CharField(max_length=10)
    start_day_time = models.DateTimeField()
    end_day_time = models.DateTimeField()

    event_submissions_open = models.DateTimeField()
    event_submissions_close = models.DateTimeField()
    signups_open = models.DateTimeField()
    signups_close = models.DateTimeField()

    @property
    def duration(self):
        days = self.end_day_time.timetuple().tm_yday \
            - self.start_day_time.timetuple().tm_yday + 1
        # future: add support for a convention across more than one year
        return days

    @property
    def day_list(self):
        start_day = self.start_day_time.timetuple().tm_yday
        end_day = self.end_day_time.timetuple().tm_yday
        days = [(d, datetime.date.fromordinal(d).strftime('%A'))
                for d in range(start_day, end_day+1)]
        return days

    def __str__(self):
        return self.name


class GCUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    # WP User ID is sent by the WordPress side
    wp_user_id = models.PositiveSmallIntegerField(unique=True, db_index=True)
    is_member = models.BooleanField(default=False)
    age = models.SmallIntegerField(blank=True, null=True)
    session_key = models.CharField(max_length=100, db_index=True, blank=True, null=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = "GameCon User"

    @property
    def is_an_admin(self):
        try:
            a = Admin.objects.get(gc_user=self)
            if a.active:
                return True
        except models.ObjectDoesNotExist:
            pass
        return False

    @property
    def is_a_scheduler(self):
        try:
            s = Scheduler.objects.get(gc_user=self)
            if s.active:
                return True
        except models.ObjectDoesNotExist:
            try:
                a = Admin.objects.get(gc_user=self)
                if a.active:
                    return True
            except models.ObjectDoesNotExist:
                pass
        return False

    @property
    def is_a_manager(self):
        try:
            m = Manager.objects.get(gc_user=self)
            if m.active:
                return True
        except models.ObjectDoesNotExist:
            try:
                a = Admin.objects.get(gc_user=self)
                if a.active:
                    return True
            except models.ObjectDoesNotExist:
                pass
        return False

    @property
    def is_an_editor(self):
        try:
            e = Editor.objects.get(gc_user=self)
            if e.active:
                return True
        except models.ObjectDoesNotExist:
            pass
        return False

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class Privilege(models.Model):
    gc_user = models.OneToOneField(GCUser, unique=True, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.active:
            state = 'active'
        else:
            state = 'inactive'
        return '%s [%s]' % (self.gc_user.__str__(), state)

    class Meta:
        abstract = True
        ordering = ['gc_user']


class Manager(Privilege):
    pass


class Admin(Privilege):
    pass


class Scheduler(Privilege):
    pass
    '''
    location_set = models.ManyToManyField(Location,
                                          through='SchedulerAssignment',
                                          through_fields='area'
                                          )
    '''


class Editor(Privilege):
    pass


class Area(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Location(models.Model):
    location_type = models.CharField(max_length=5,
                                     choices=constants.LocationTypes.LOCATION_CHOICES
                                     )
    # Every table must be assigned to exactly one area.
    # A room will only be assigned to an area if there are no
    # tables in it
    #
    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.DO_NOTHING)
    room = models.ForeignKey("self", blank=True, null=True, related_name='room_location', on_delete=models.DO_NOTHING)
    capacity = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=40)
    tag = models.CharField(max_length=10, unique=True)
    table_type = models.CharField(max_length=6,
                                  choices=constants.TableTypes.TABLE_CHOICES_LOCATION,
                                  default=constants.TableTypes.LONG,
                                  blank=True,
                                  null=True,
                                  )
    # Any given table should have either length and width *or* diameter
    length_in_inches = models.SmallIntegerField(blank=True, null=True)
    width_in_inches = models.SmallIntegerField(blank=True, null=True)
    diameter_in_inches = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['tag']
        index_together = [
            ["capacity", "table_type"],
            ["table_type", "capacity"],
        ]

    def __str__(self):
        return self.name


class SchedulerAssignment(models.Model):
    scheduler = models.ForeignKey(Scheduler, on_delete=models.DO_NOTHING)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    start = models.DateTimeField()
    end = models.DateTimeField()


    def __str__(self):
        start = self.start.strftime('%d-%b-%Y %H:%M')
        end = self.end.strftime('%d-%b-%Y %H:%M')
        return '%s  is  scheduler for  %s  from %s to %s' % \
               (self.scheduler, self.area, start, end)

    class Meta():
        unique_together = ('area', 'start')
        ordering = ['scheduler', 'start']


'''
class ORCSystem(models.Model):
-    system = models.CharField(max_length=30)

    def __str__(self):
        return self.system

class ORCCharacterOption(models.Model):
    option = models.CharField(max_length=30)

    def __str__(self):
        return self.option


class ORCSystemOption(models.Model):
    system = models.ForeignKey(ORCSystem)
    option = models.ForeignKey(ORCCharacterOption)

    def __str__(self):
        return '%s: %s' % (self.system, self.option)
'''


class Game(models.Model):
    event_name = models.CharField(max_length=100)
    submitter = models.ForeignKey(GCUser, db_index=True, related_name='%(class)s_submitter', on_delete=models.DO_NOTHING)
    duration_in_minutes = models.PositiveSmallIntegerField(help_text='Duration',
                                                           verbose_name='Duration',
                                                           choices=constants.Duration.DURATION_CHOICES
                                                           )
    player_max = models.SmallIntegerField(
        help_text='Maximum number of players, including GM if they will be playing',
        )
    short_description = models.TextField(help_text='Maximum 400 characters',
                                         verbose_name=escape('Short Description'))
    long_description = models.TextField(help_text='Maximum 2500 characters',
                                        verbose_name='Long Description')
    url = models.URLField(null=True, blank=True, verbose_name='URL')
    game_system = models.CharField(max_length=50, blank=True, null=True, help_text='D&D 3.5, GURPS, etc')
    conflict_type = models.SmallIntegerField(choices=constants.ConflictTypes.CONFLICT_CHOICES,
                                             default=constants.ConflictTypes.RESTRICTED
                                             )
    proofread = models.BooleanField(default=False)
    proofread_time = models.DateTimeField(null=True, blank=True)
    proofread_by = models.ForeignKey(GCUser, null=True, blank=True, on_delete=models.DO_NOTHING)
    # This is duplicated in Event. In should have been here in the first place
    track = models.CharField(max_length=5, db_index=True,
                             choices=constants.Tracks.TRACK_CHOICES,
                             # choices=constants.Tracks.ORYCON_TRACKS,
                             )

    # orc_game_system = models.ForeignKey(ORCSystem, blank=True, null=True)

    def __str__(self):
        return self.event_name

    class Meta:
        abstract = True


class CatalogEntry(Game):
    active = models.BooleanField(default=True)
    in_library = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Catalog Entries"

# per con count of submissions per catalog entry


class Event(Game):
    convention = models.ForeignKey(Convention, default=1, on_delete=models.DO_NOTHING)
    # The Catalog Entry should only be set on Event creation
    catalog_entry = models.ForeignKey(CatalogEntry, blank=True, null=True, on_delete=models.DO_NOTHING)

    # automatic field
    creation_date = models.DateTimeField(auto_now_add=True)

    # scheduler accessible fields
    public = models.BooleanField(default=False)
    scheduler = models.ForeignKey(GCUser, null=True, blank=True, related_name='event_scheduler', on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    # user-input fields
    gm_is_player = models.BooleanField(default=False,
                                       help_text='Check if GM will be playing the game',
                                       verbose_name='GM is a player')
    gm_is_designer = models.BooleanField(default=False, help_text='Check if GM designed the game')
    user_notes = models.TextField(blank=True, default='', verbose_name='Note to Scheduler')
    scheduler_notes = models.TextField(blank=True, default='')
    experience = models.CharField(max_length=3,
                                  choices=constants.ExpLevels.EXPERIENCE_CHOICES,
                                  default=constants.ExpLevels.NOVICE,
                                  )
    status = models.CharField(max_length=4, db_index=True,
                              choices=constants.Status.STATUS_CHOICES,
                              )
    age_group = models.CharField(max_length=3,
                                 choices=constants.AgeGroups.AGE_CHOICES,
                                 default=constants.AgeGroups.ALL,
                                 )
    table_type = models.CharField(max_length=6,
                                  choices=constants.TableTypes.TABLE_CHOICES_EVENT,
                                  default=constants.TableTypes.NO_PREF,
                                  )
    event_type = models.CharField(max_length=5,
                                  choices=constants.EventTypes.EVENT_TYPE_CHOICES,
                                  default=constants.EventTypes.GAME,
                                  )
    more_tracks = models.BooleanField(default=False)

    class Meta:
        ordering = ['convention', 'start_time']
        index_together = [
            ['convention', 'track', 'status'],
            ['convention', 'submitter', 'track'],
            ['convention', 'start_time', 'track', 'event_name'],
            ['convention', 'track', 'start_time', 'event_name'],
            ['convention', 'event_name', 'start_time'],
            ['convention', 'track', 'public']
        ]

    @property
    def day(self):
        return self.start_time.timetuple().tm_yday

    @property
    def sort_name(self):
        name = self.event_name

        # A list of flags to check each `title` against.
        starts_with_flags = [
            'the ',
            'an ',
            'a '
        ]

        for flag in starts_with_flags:
            if name.lower().startswith(flag):
                return name[len(flag)]
            else:
                pass
        return self.event_name

    def get_user_names(self, role):
        # This is a stripped-down version of the function in utilities
        # Importing from utilities caused import error for models module
        #
        cnx_set = Connection.objects.filter(event=self, role=role)
        user_list = []
        for cnx in cnx_set:
            user_list.append(cnx.user.full_name)
        result = ', '.join(user_list)
        return result

    # The following properties are defined to facilitate serialization for REST

    @property
    def gm_names(self):
        return self.get_user_names(constants.Roles.GM)

    @property
    def coordinator_names(self):
        return self.get_user_names(constants.Roles.COORDINATOR)

    @property
    def panelist_names(self):
        return self.get_user_names(constants.Roles.PANELIST)

    @property
    def player_count(self):
        cnx_set = Connection.objects.filter(event=self, role=constants.Roles.PLAYER)
        return len(cnx_set)

    @property
    def track_names(self):
        # returns a comma-separated string of the names of tracks
        track_names = self.get_track_display()
        if self.more_tracks:
            track_assg_set = TrackAssignment.objects.filter(event=self)
            for assg in track_assg_set:
                track_names += ', %s' % assg.get_track_display()
        return track_names

    @property
    def tracks(self):
        # returns a comma-separated list of tracks (db tags)
        tracks =  [self.track]
        if self.more_tracks:
            track_assg_set = TrackAssignment.objects.filter(event=self)
            for assg in track_assg_set:
                tracks.append(assg.track)
        return tracks

    @property
    def location_tags(self):
        # returns a comma-separated list of locations (db tags) as a string
        # if no locations are found, returns an empty string
        assignment_set = LocationAssignment.objects.filter(event=self)
        location_list = [assignment.location.tag for assignment in assignment_set]
        locations = ', '.join(location_list)
        return locations

    @property
    def location_names(self):
        # returns a comma-separated list of location names as a string
        # if no locations are found, returns an empty string
        assignment_set = LocationAssignment.objects.filter(event=self)
        location_list = [assignment.location.name for assignment in assignment_set]
        locations = ', '.join(location_list)

        return locations


class TrackAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    track = models.CharField(max_length=5, db_index=True,
                             choices=constants.Tracks.TRACK_CHOICES,
                             )

    class Meta:
        unique_together = ('event', 'track')

    def __str__(self):
        return '%s  -->  track %s' % (self.event, self.get_track_display())

'''
class StaffEvent(models.Model):
    catalog_entry = models.ForeignKey(CatalogEntry)
    start_time = models.FloatField()
    end_time = models.FloatField()
    department = models.CharField(max_length=4,
                                  choices=StaffTypes.STAFF_CHOICES,
                                  )
'''


class Connection(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(GCUser, related_name='user_connection', null=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, related_name='event_connection', null=False, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=8,
                            choices=constants.Roles.ROLE_CHOICES,
                            null=False,
                            )
    conflict_type = models.SmallIntegerField(choices=constants.ConflictTypes.CONFLICT_CHOICES,
                                             default=constants.ConflictTypes.RESTRICTED
                                             )

    def __str__(self):
        return '%s is %s for %s' % (self.user,
                                    self.get_role_display(),
                                    self.event.event_name,
                                    )

    class Meta:
        index_together = [
            ['event', 'role'],
            ['user', 'role'],
            ['event', 'user', 'role'],
        ]
        ordering = ['event']
        unique_together = ('user', 'event', 'role')


class LocationAssignment(models.Model):
    event = models.ForeignKey(Event, related_name='event_assignment', on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, related_name='location_assignment', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('event', 'location')
        verbose_name_plural = "Location Assignments"

    def __str__(self):
        s = '%s is at location %s' % (self.event, self.location)
        return s


class Favorite(models.Model):
    user = models.ForeignKey(GCUser, related_name='user_favorite', null=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, related_name='event_favorite', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('user', 'event')
