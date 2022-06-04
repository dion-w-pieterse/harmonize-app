###############################################
######### MODELS for Schema ###################
###############################################
from harmonize_package import db, admin, login_manager
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from flask_login import UserMixin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR



class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

from sqlalchemy import desc, Index


# Flask-Login Requirement
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Monitor(db.Model):
    '''
    Purpose: This table is for the monitoring system. A user can monitor another user.
    '''
    __table_args__ = (db.UniqueConstraint('monitor_id', 'monitoree_id'), )
    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    monitoree_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class BlogEntryLike(db.Model):
    '''
    Purpose: This table records all the likes for every blog entry for all user types
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    blog_entry_id = db.Column(db.Integer, db.ForeignKey('blog_entry.id', ondelete='CASCADE'))


class ConvoResponseLike(db.Model):
    '''
    Purpose: This table records all the likes for forum convo response from all user types
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    convo_response_id = db.Column(db.Integer, db.ForeignKey('convo_response.id', ondelete='CASCADE'))


class GrantedPrivacyAccess(db.Model):
    '''
    Purpose: This table holds all the granted privacy access from patient to provider,
    to view private patient entries.
    '''
    __table_args__ = (db.UniqueConstraint('grantor_id', 'grantee_id'), )
    id = db.Column(db.Integer, primary_key=True)
    grantor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    grantee_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class UserBlogsMention(db.Model):
    '''
    Purpose: This table keeps track of which blog entries contain mentions of user aliases.
    '''
    # __table_args__ = (db.UniqueConstraint('blog_entry_id', 'user_id'), )
    id = db.Column(db.Integer, primary_key=True)
    blog_entry_id = db.Column(db.Integer, db.ForeignKey('blog_entry.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class UserForumMention(db.Model):
    '''
    Purpose: This table keeps track of which forum conversation responses contain mentions of user aliases.
    '''
    id = db.Column(db.Integer, primary_key=True)
    convo_response_id = db.Column(db.Integer, db.ForeignKey('convo_response.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class User(db.Model, UserMixin):
    '''
    Purpose: This table is the user table for all user types.
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_alias = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    addr_street = db.Column(db.String(255), nullable=True)
    addr_city = db.Column(db.String(255), nullable=True)
    addr_state = db.Column(db.String(255), nullable=True)
    addr_zip = db.Column(db.String(255), nullable=True)
    addr_country = db.Column(db.String(255), nullable=True)
    ph_number = db.Column(db.String(255), nullable=True)
    account_img = db.Column(db.String(255), nullable=False, default='placeholder_img.jpg')
    user_type = db.Column(db.String(255), nullable=False, server_default='patient')
    seeking_status = db.Column(db.Boolean, nullable=True, default=True)
    non_searchable = db.Column(db.Boolean, nullable=True, default=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bio = db.Column(db.Text, nullable=True)
    chosen_insurance = db.Column(db.String(255), nullable=True)
    # Foreign Keys and Relationships:
    entries = db.relationship('BlogEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    forum_rooms = db.relationship('ForumRoom', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    convo_responses = db.relationship('ConvoResponse', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    chosen_conditions = db.relationship('ChosenCondition', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    insurance_co_accepted = db.relationship('InsuranceCoAccepted', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    out_of_network_services_for = db.relationship('OutOfNetServicesFor', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    blog_entry_likes = db.relationship('BlogEntryLike', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    convo_response_likes = db.relationship('ConvoResponseLike', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    # experiment
    user_blogs_mention = db.relationship('UserBlogsMention', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    user_forum_mention = db.relationship('UserForumMention', backref='user', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return '<User %r>' % (self.email)


class ChosenCondition(db.Model):
    '''
    Purpose: This table holds all the chosen conditions from both user types.
    '''
    __table_args__ = (db.UniqueConstraint('user_id', 'condition_name'), )
    id = db.Column(db.Integer, primary_key=True)
    condition_name = db.Column(db.String(255), nullable=False)
    # Foreign Keys and Relationships:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    #conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Chosen Condition: %r>' % (self.condition_name)


class ConvoChosenCondition(db.Model):
    '''
    Purpose: This table holds all the chosen conditions from both user types.
    '''
    __table_args__ = (db.UniqueConstraint('conversation_id', 'condition_name'), )
    id = db.Column(db.Integer, primary_key=True)
    condition_name = db.Column(db.String(255), nullable=False)
    # Foreign Keys and Relationships:
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Convo Condition: %r>' % (self.condition_name)


class InsuranceCoAccepted(db.Model):
    '''
    Purpose: These are the insurance companies that are accepted by the provider.
    '''
    __table_args__ = (db.UniqueConstraint('insurance_name', 'user_id'), )
    id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String(255), nullable=True)
    # Foreign Keys and Relationships:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Insurance Name %r>' % (self.insurance_name)


class OutOfNetServicesFor(db.Model):
    '''
    Purpose:
    This is the list of Out-Of-Network services provided in an In-Network Insurance Co. Facility
    (At time of service, the provider was deemed Out-of-Network).
    '''
    #__table_args__ = (db.UniqueConstraint('insurance_name', 'user_id'), )
    id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String(255), nullable=True)
    # Foreign Keys and Relationships:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Out of Network Services For Insurance Name %r>' % (self.insurance_name)


class BlogEntry(db.Model):
    '''
    Purpose: This is a blog entry for both user types.
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    entry_img = db.Column(db.String(255), nullable=True, default='blog_placeholder_img.jpg')
    body = db.Column(db.Text, nullable=False)
    private_entry = db.Column(db.Boolean, nullable=True, default=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    analysis_neg_score = db.Column(db.Float)
    analysis_neu_score = db.Column(db.Float)
    analysis_pos_score = db.Column(db.Float)
    analysis_compound_score = db.Column(db.Float)
    # Foreign Keys & Relationships:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    blog_entry_likes = db.relationship('BlogEntryLike', backref='blog_entry', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    # experiment: (might need to delete: many to many)
    user_blogs_mention = db.relationship('UserBlogsMention', backref='blog_entry', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    # start for Full-Text-Search PostgreSQL
    __ts_vector__ = db.Column(TSVector(), db.Computed(
        "to_tsvector('english', title || ' ' || body)", persisted=True
    ))

    __table_args__ = (Index('ix_blog_entry___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)
    # end Full-Text-Search

    def __repr__(self):
        return '<Post f{}'.format(self.title)


class ForumRoom(db.Model):
    '''
    Purpose: This holds all the Rooms, which each contain conversations.
    '''
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), unique=True)
    room_summary = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    private_room = db.Column(db.Boolean, nullable=True, default=False)
    # Foreign Keys & Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    conversations = db.relationship('Conversation', backref='forum_room', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return '<ForumRoom %r>' % (self.room_name)


class Conversation(db.Model):
    '''
    Purpose: This is a specific conversation which resides in a specific Room.
    '''
    id = db.Column(db.Integer, primary_key=True)
    convo_name = db.Column(db.String(255))
    convo_summary = db.Column(db.String(255))
    convo_init_body = db.Column(db.Text, nullable=True)
    private_conversation = db.Column(db.Boolean, nullable=True, default=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Foreign Keys & Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    forum_room_id = db.Column(db.Integer, db.ForeignKey('forum_room.id', ondelete='CASCADE'))
    convo_responses = db.relationship('ConvoResponse', backref='conversation', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    convo_chosen_conditions = db.relationship('ConvoChosenCondition', backref='conversation', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return '<Conversation %r>' % (self.convo_name)


class ConvoResponse(db.Model):
    '''
    Purpose: This is a response to a specific conversation.
    '''
    id = db.Column(db.Integer, primary_key=True)
    resp_img = db.Column(db.String(255), nullable=True, default='resp_placeholder_img.jpg')
    body = db.Column(db.Text, nullable=True)
    private_response = db.Column(db.Boolean, nullable=True, default=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Foreign Keys & Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id', ondelete='CASCADE'))

    # experiment
    user_forum_mention = db.relationship('UserForumMention', backref='convo_response', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    convo_response_likes = db.relationship('ConvoResponseLike', backref='convo_response', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    # start for Full-Text-Search PostgreSQL
    __ts_vector__ = db.Column(TSVector(), db.Computed(
        "to_tsvector('english', body)", persisted=True
    ))

    __table_args__ = (Index('ix_convo_response___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)
    # end Full-Text-Search

    def __repr__(self):
        return '<Reply %r>' % (self.body)


###########################################################
#### Flask-Admin Override BaseModelView Table Settings ####
###########################################################

class UserView(ModelView):
    column_exclude_list = ['addr_street', 'addr_city', 'addr_state', 'addr_zip', 'addr_country', 'bio']
    export_types = ['csv', 'xls', 'xlsx', 'json']
    can_export = True
    column_sortable_list = ['email', 'user_alias', 'password', 'first_name', 'last_name', 'ph_number', 'account_img', 'user_type', 'seeking_status', 'non_searchable', 'created_date', 'last_login', 'chosen_insurance']
    column_default_sort = 'last_name'
    column_searchable_list = ['email', 'user_alias', 'password', 'first_name', 'last_name', 'ph_number', 'created_date', 'last_login', 'chosen_insurance']
    column_filters = ['email', 'user_alias', 'password', 'first_name', 'last_name', 'ph_number', 'account_img', 'user_type', 'seeking_status', 'non_searchable', 'created_date', 'last_login', 'chosen_insurance']


class ConversationView(ModelView):
    column_exclude_list = ['convo_summary', 'convo_init_body']
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'convo_name'
    column_sortable_list = ['convo_name', 'convo_summary', 'convo_init_body', 'created_date', 'user_id', 'forum_room_id']
    column_searchable_list = ['convo_name', 'convo_summary', 'convo_init_body', 'created_date', 'user_id', 'forum_room_id']
    column_filters = ['convo_name', 'convo_summary', 'convo_init_body', 'created_date', 'user_id', 'forum_room_id']


class BlogEntryView(ModelView):
    column_exclude_list = ['user_id', '__ts_vector__']
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'title'
    column_sortable_list = ['title', 'entry_img', 'body', 'created_date', 'analysis_neg_score', 'analysis_neu_score', 'analysis_pos_score', 'analysis_compound_score']
    column_searchable_list = ['title', 'entry_img', 'body', 'created_date', 'analysis_neg_score', 'analysis_neu_score', 'analysis_pos_score', 'analysis_compound_score']
    column_filters = ['title', 'entry_img', 'body', 'created_date', 'analysis_neg_score', 'analysis_neu_score', 'analysis_pos_score', 'analysis_compound_score']


class ForumRoomView(ModelView):
    column_exclude_list = ['room_summary', 'user_id']
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'room_name'
    column_sortable_list = ['room_name', 'room_summary', 'created_date', 'private_room', 'user_id']
    column_filters = ['room_name', 'room_summary', 'created_date', 'private_room', 'user_id']
    column_searchable_list = ['room_name', 'room_summary', 'created_date', 'private_room', 'user_id']


class ConvoResponseView(ModelView):
    column_exclude_list = ['__ts_vector__']
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'user_id'
    column_sortable_list = ['resp_img', 'body', 'created_date', 'user_id', 'conversation_id']
    column_filters = ['resp_img', 'body', 'created_date', 'user_id', 'conversation_id']
    column_searchable_list = ['resp_img', 'body', 'created_date', 'user_id', 'conversation_id']


class UserBlogsMentionView(ModelView):
    column_exclude_list = []
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'blog_entry_id'
    column_sortable_list = ['blog_entry_id', 'user_id', 'created_date']
    column_filters = ['blog_entry_id', 'user_id', 'created_date']
    column_searchable_list = ['blog_entry_id', 'user_id', 'created_date']


class ChosenConditionView(ModelView):
    column_exclude_list = []
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'condition_name'
    column_sortable_list = ['condition_name', 'user_id']
    column_filters = ['condition_name', 'user_id']
    column_searchable_list = ['condition_name', 'user_id']


class OutOfNetServicesForView(ModelView):
    column_exclude_list = []
    can_export = True
    export_types = ['csv', 'xls', 'xlsx', 'json']
    column_default_sort = 'insurance_name'
    column_sortable_list = ['insurance_name', 'user_id']
    column_filters = ['insurance_name', 'user_id']
    column_searchable_list = ['insurance_name', 'user_id']


#############################################
#### Flask-Admin Add Default Base Models ####
#############################################
admin.add_view(UserView(User, db.session))
admin.add_view(BlogEntryView(BlogEntry, db.session))
admin.add_view(ForumRoomView(ForumRoom, db.session))
admin.add_view(ConversationView(Conversation, db.session))
admin.add_view(ConvoResponseView(ConvoResponse, db.session))
admin.add_view(UserBlogsMentionView(UserBlogsMention, db.session))
admin.add_view(ChosenConditionView(ChosenCondition, db.session))
admin.add_view(OutOfNetServicesForView(OutOfNetServicesFor, db.session))
