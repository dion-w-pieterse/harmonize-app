###################################
######### ROUTES ###################
####################################
from harmonize_package import app, db, queries, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, url_for, request, g, jsonify, session
from harmonize_package.forms import UserLoginForm, UserRegisterForm, BlogEntryForm, AccountEditForm, ProvInsuranceSrvces, PublicRoomForm, PublicConvoForm, EditPublicConvoForm, PublicRespForm, EditPublicRespForm, SearchSiteForm, SearchUserAliasForm, ChangePasswordForm
from harmonize_package.models import BlogEntry, Conversation, User, ChosenCondition, OutOfNetServicesFor, ForumRoom, ConvoResponse, ConvoChosenCondition
from werkzeug.security import check_password_hash, generate_password_hash
from harmonize_package.image_processing import ImageProcessor
from harmonize_package.mention_processing import MentionProcessor
from harmonize_package.resp_mention_processing import RespMentionProcessor
from harmonize_package.mention_edit_processing import MentionEditProcessor
from harmonize_package.resp_mention_edit_processing import RespMentionEditProcessor
from harmonize_package.sentiment_analysis import SentimentAnalyzer

# experiment
from sqlalchemy.exc import IntegrityError
# end
from flaskext.markdown import Markdown
Markdown(app)
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
spacy_nat_lang_processor = spacy.load('en_core_web_sm')
from spacy import displacy

# import for save_picture method
import secrets
import os
from PIL import Image

# regular expressions
import re

@app.before_request
def before_request():
    # instantiate SearchForm object
    # g.third_search_form = ThirdSearchForm()
    g.search_site_form = SearchSiteForm()


def find_user_mentions(entry_body):
    user_mention_list = []
    possible_user_mention = ''
    # tokenize the entry body into list of space delimited words
    # token_list = entry_body.split(' ')
    token_list = re.split(' |\r\n|\n', entry_body)
    for word in token_list:
        print(word)
        if word.startswith('@'):
            # add potential user mention to list
            possible_user_mention = word
            user_mention_list.append(possible_user_mention)
    # print candidate list before cleaning
    print(f'User mention list before cleaning: {user_mention_list}')
    # remove the @ char from the beginning of every potential user mention candidate
    user_alias_recommendations = []
    for candidate in user_mention_list:
        # remove the @ char from the candidate
        user_alias_recommendations.append(candidate.replace('@', ''))

    print(f'Token List: { token_list }')
    print(f'User Mention List After Cleaning: { user_alias_recommendations }')
    return user_alias_recommendations


def set_blogs_user_mentions(validated_mentions):
    # now add validated mentions to user_blogs_mentions table (process list into set)
    unique_validated_aliases = set(validated_mentions)
    # read the id of the latest blog entry from the database
    blog_entry_id = queries.get_latest_blog_entry_id()
    for alias in unique_validated_aliases:
        # look up user by unique alias
        user_id = queries.get_user_id_by_alias(user_alias=alias)['id']
        print(f'Check type: {user_id}')
        queries.set_user_blogs_mention(blog_entry_id=blog_entry_id, user_id=user_id)
    return


###########################################################
### BLOG
###########################################################

@app.route('/blog/<int:user_id>', methods=['GET', 'POST'])
@login_required
def blog(user_id):

    # get user by user_id
    found_user = User.query.filter_by(id=user_id).first()
    # check if blog is searchable
    non_searchable = queries.chk_non_searchable(user_id=user_id)
    print(f'SEARCHABLE: {non_searchable}')
    if found_user is None:
        flash("That user's blog could not be found!")
        return redirect(url_for('index'))
    elif (current_user.id == user_id) or (current_user.id != user_id and non_searchable is None):
        current_page = request.args.get('current_page', type=int)
        user_blog = found_user.entries.order_by(BlogEntry.id.desc()).paginate(page=current_page, per_page=4)
        print(user_blog)
    elif found_user and non_searchable and current_user.id != user_id:
        flash('This user has their blog set to non-searchable. You cannot view this blog.')
        return redirect(url_for('index'))

    return render_template('user_blog_landing.html', user_blog=user_blog, found_user=found_user, queries=queries)


@app.route('/blog/<int:user_id>/entry/<int:blog_entry_id>', methods=['GET', 'POST'])
@login_required
def view_blog_entry(user_id, blog_entry_id):
    blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()

    return render_template('user_blog_entry.html', blog_entry=blog_entry)


@app.route('/blog/<int:user_id>/entry/<int:blog_entry_id>/analysis', methods=['GET', 'POST'])
@login_required
def view_journal_entry_analysis(user_id, blog_entry_id):
    blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()
    # extract entry text body
    entry_text_to_analyze = blog_entry.body
    # instantiate analyzer
    sent_analyzer = SentimentAnalyzer(entry_text_to_analyze)
    # get polarity scores
    #polarity_scores = sent_analyzer.get_polarity_scores()
    # get polarity percentages
    #polarity_percent_value_list = sent_analyzer.get_polarity_score_percentages()

    #### NER ####
    # create a document (for python 3 all strings are unicode by default, no need to cast)
    entry_document = sent_analyzer.process_text_w_snlp()
    snlp = sent_analyzer.get_snlp()

    return render_template('view_journal_entry_analysis.html', user_id=user_id,\
                                                               blog_entry=blog_entry,\
                                                               entry_document=entry_document,\
                                                               displacy=displacy,\
                                                               snlp=snlp)


@app.route('/blog/<int:user_id>/entry/<int:blog_entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog_entry(user_id, blog_entry_id):
    blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()

    be_form = BlogEntryForm()
    # POST
    if be_form.validate_on_submit():
        # process mentions
        mention_edit_processor = MentionEditProcessor(be_form, blog_entry_id, user_id)
        mention_edit_processor.find_user_mentions_for_edit()
        mention_edit_processor.process_collected_mentions_for_edit()
        mention_edit_processor.set_blog_user_mentions_for_edit()

        flash('Your Blog Entry was Updated Successfully.')
        return redirect(url_for('view_blog_entry', user_id=user_id, blog_entry_id=blog_entry_id))
    # GET
    # pre-populate the form with information stored in the database
    be_form.title.data = blog_entry.title
    be_form.body.data = blog_entry.body
    be_form.private_entry.data = blog_entry.private_entry

    return render_template('edit_blog_entry.html', be_form=be_form, blog_entry=blog_entry)


@app.route('/blog/<int:user_id>/write', methods=['GET', 'POST'])
@login_required
def write_blog_entry(user_id):

    be_form = BlogEntryForm()
    # POST
    if be_form.validate_on_submit():
        mention_processor = MentionProcessor(be_form)
        mention_processor.find_user_mentions()
        mention_processor.process_collected_mentions()
        mention_processor.set_blog_user_mentions()
        return redirect(url_for('blog', user_id=user_id))
    # GET
    return render_template('write_blog_entry.html', be_form=be_form)


@app.route('/blog/<int:user_id>/entry/<int:blog_entry_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_blog_entry(user_id, blog_entry_id):
    # locate blog entry for deletion
    blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()
    # delete the blog entry
    db.session.delete(blog_entry)
    db.session.commit()
    flash(f'Blog Entry ID: {blog_entry.id } was deleted.')
    return redirect(url_for('blog', user_id=user_id))


@app.route('/blog/like_blog_entry/<int:blog_entry_id>', methods=['GET', 'POST'])
@login_required
def like_blog_entry(blog_entry_id):
    print(f'Requesting page: {request.referrer}')
    print(f'Liked Blog Entry ID: {blog_entry_id}')
    found_blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()
    # Check logged in user is not trying to like their own posts
    if current_user.id != found_blog_entry.user.id:
        # check the user has not already liked the same post (only one like per user)
        print(queries.chk_user_liked_entry(user_id=current_user.id, blog_entry_id=blog_entry_id))
        if not queries.chk_user_liked_entry(user_id=current_user.id, blog_entry_id=blog_entry_id):
            # record the blog entry like by the current logged in user
            queries.set_blog_entry_like(user_id=current_user.id, blog_entry_id=blog_entry_id)
        else:
            flash('You cannot like a blog entry more than once.')
    else:
        flash('You Cannot Like Your Own Blog Entries.')
    # return back to the blog of the user where you liked their entry
    return redirect(request.referrer)


@app.route('/blog/unlike_blog_entry/<int:blog_entry_id>', methods=['GET', 'POST'])
@login_required
def unlike_blog_entry(blog_entry_id):
    print(f'Requesting page: {request.referrer}')
    print(f'Liked Blog Entry ID: {blog_entry_id}')
    found_blog_entry = BlogEntry.query.filter_by(id=blog_entry_id).first()
    # Check logged in user is not trying to like their own posts
    if current_user.id != found_blog_entry.user.id:
        # check the user has not already liked the same post (only one like per user)
        print(queries.chk_user_liked_entry(user_id=current_user.id, blog_entry_id=blog_entry_id))
        if queries.chk_user_liked_entry(user_id=current_user.id, blog_entry_id=blog_entry_id):
            # record the blog entry like by the current logged in user
            queries.set_blog_entry_unlike(user_id=current_user.id, blog_entry_id=blog_entry_id)
        else:
            flash('You cannot un-like a blog entry more than once.')
    else:
        flash('You Cannot Un-Like Your Own Blog Entries.')
    # return back to the blog of the user where you liked their entry
    return redirect(request.referrer)


@app.route('/forum/like_forum_response/<int:convo_response_id>', methods=['GET', 'POST'])
@login_required
def like_forum_response(convo_response_id):
    print(f'Requesting page: {request.referrer}')
    print(f'Liked Forum Response ID: {convo_response_id}')
    found_forum_resp = ConvoResponse.query.filter_by(id=convo_response_id).one()
    # Check logged in user is not trying to like their own posts
    if current_user.id != found_forum_resp.user.id:
        # check the user has not already liked the same resp (only one like per user)
        print(queries.chk_user_liked_resp(user_id=current_user.id, convo_response_id=convo_response_id))
        if not queries.chk_user_liked_resp(user_id=current_user.id, convo_response_id=convo_response_id):
            # record the blog entry like by the current logged in user
            queries.set_forum_response_like(user_id=current_user.id, convo_response_id=convo_response_id)
        else:
            flash('You cannot like a forum response more than once.')
    else:
        flash('You Cannot Like Your Own Forum Response.')
    # return back to the conversation where the response was liked.
    return redirect(request.referrer)


@app.route('/forum/unlike_forum_response/<int:convo_response_id>', methods=['GET', 'POST'])
@login_required
def unlike_forum_response(convo_response_id):
    print(f'Requesting page: {request.referrer}')
    print(f'Liked Blog Entry ID: {convo_response_id}')
    found_forum_resp = ConvoResponse.query.filter_by(id=convo_response_id).one()
    # Check logged in user is not trying to like their own forum response
    if current_user.id != found_forum_resp.user.id:
        # check the user has not already liked the same response (only one like per user)
        print(queries.chk_user_liked_resp(user_id=current_user.id, convo_response_id=convo_response_id))
        if queries.chk_user_liked_resp(user_id=current_user.id, convo_response_id=convo_response_id):
            # record the forum response like by the current logged in user
            queries.set_forum_response_unlike(user_id=current_user.id, convo_response_id=convo_response_id)
        else:
            flash('You cannot un-like a forum response more than once.')
    else:
        flash('You Cannot Un-Like Your Own Forum Response.')
    # return back to the conversation where the response was unliked.
    return redirect(request.referrer)


###########################################################
### FORUM
###########################################################


######## ROOM #######

@app.route('/forum_rooms', methods=['GET', 'POST'])
@ login_required
def forum_rooms():
    current_page = request.args.get('current_page', 1, type=int)
    # grab all posts from the database
    available_rooms = ForumRoom.query.order_by(ForumRoom.created_date.desc()).paginate(page=current_page, per_page=4)

    return render_template('forum_rooms.html', available_rooms=available_rooms)


@app.route('/forum_rooms/<int:room_id>', methods=['GET', 'POST'])
def room_view(room_id):
    current_page = request.args.get('current_page', 1, type=int)
    # get the room from the database
    found_room = ForumRoom.query.filter_by(id=room_id).one()
    # grab all posts from the database
    conversations = Conversation.query.filter_by(forum_room_id=found_room.id).order_by(Conversation.created_date.desc()).paginate(page=current_page, per_page=4)

    return render_template('public_room.html', found_room=found_room, conversations=conversations)


@app.route('/forum_rooms/write', methods=['GET', 'POST'])
@ login_required
def room_write():
    # instantiate new form for room creation
    public_room_form = PublicRoomForm()

    # POST
    if public_room_form.validate_on_submit():
        # all the user's form data is valid, proceed to create the public room
        room_name = public_room_form.room_name.data
        room_summary = public_room_form.room_summary.data
        user_id = current_user.id

        # create a new public room
        new_room = ForumRoom(room_name=room_name, room_summary=room_summary, private_room=False, user_id=user_id)
        # add to db session
        db.session.add(new_room)
        # commit to database
        db.session.commit()
        # get the id of the room that was just created
        room_id = queries.get_latest_public_forum_room_id()
        # redirect to the newly created room.
        return redirect(url_for('room_view', room_id=room_id))

    # GET
    return render_template('write_public_room.html', public_room_form=public_room_form)


@app.route('/forum_rooms/<int:room_id>/edit', methods=['GET', 'POST'])
@ login_required
def room_edit(room_id):
    # create a new form to edit the room
    public_room_form = PublicRoomForm()
    # look up the room in the database
    found_room = ForumRoom.query.filter_by(id=room_id).one()

    # POST
    if public_room_form.validate_on_submit():
        # all the user's form data is valid, proceed to create the public room
        found_room.room_name = public_room_form.room_name.data
        found_room.room_summary = public_room_form.room_summary.data
        # commit changes to database (no need to add to session)
        db.session.commit()
        flash('The Room Has Been Updated With Your Edits.')
        redirect(url_for('room_edit', room_id=room_id))
    # GET
    # pre-populate room form with data from the database
    public_room_form.room_name.data = found_room.room_name
    public_room_form.room_summary.data = found_room.room_summary
    # GET
    return render_template('edit_public_room.html', public_room_form=public_room_form, room_id=room_id, found_room=found_room)


@app.route('/forum_rooms/<int:room_id>/remove', methods=['GET', 'POST'])
@ login_required
def room_remove(room_id):
    # locate room for deletion
    found_room = ForumRoom.query.filter_by(id=room_id).first()
    # delete the room
    db.session.delete(found_room)
    # commit changes to database
    db.session.commit()
    flash(f'Room: {found_room.room_name} has been destroyed along with all its conversations.')
    return redirect(url_for('forum_rooms'))


######## CONVERSATION #######

@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>', methods=['GET', 'POST'])
@ login_required
def convo_view(room_id, convo_id):
    current_page = request.args.get('current_page', 1, type=int)
    # get the room from the database
    found_room = ForumRoom.query.filter_by(id=room_id).one()
    # get conversation from db
    found_convo = Conversation.query.filter_by(id=convo_id).one()
    # grab all convo responses from the database
    responses = ConvoResponse.query.filter_by(conversation_id=convo_id).order_by(ConvoResponse.created_date.asc()).paginate(page=current_page, per_page=4)

    # GET
    return render_template('public_conversation.html', found_room=found_room, found_convo=found_convo, queries=queries, responses=responses)


@app.route('/forum_rooms/<int:room_id>/convos/write', methods=['GET', 'POST'])
@ login_required
def convo_write(room_id):
    # instantiate convo form
    public_convo_form = PublicConvoForm()
    # find the room in the database
    found_room = ForumRoom.query.filter_by(id=room_id).one()
    # POST
    if public_convo_form.validate_on_submit():
        # all the user's form data is valid, proceed to create the public conversation
        convo_name = public_convo_form.convo_name.data
        convo_summary = public_convo_form.convo_summary.data
        convo_init_body = public_convo_form.convo_init_body.data
        user_id = current_user.id

        # create a new public conversation
        new_convo = Conversation(convo_name=convo_name, convo_summary=convo_summary, convo_init_body=convo_init_body, private_conversation=False, user_id=user_id, forum_room_id=found_room.id)
        # add to db session
        db.session.add(new_convo)
        # commit to database
        db.session.commit()

        # get the id of the conversation that was just created
        convo_id = queries.get_latest_public_convo_id()

        # add the chosen conditions to the newly created conversation
        for condition in public_convo_form.chosen_conditions.data:
            # if user has condition, don't try add it, skip it
            if queries.chk_convo_has_condition_in_db(condition_name=condition, conversation_id=convo_id):
                continue
            else:
                try:
                    new_condition = ConvoChosenCondition(condition_name=condition, conversation_id=convo_id)
                    db.session.add(new_condition)
                    db.session.commit()
                except IntegrityError:
                    # if the condition has already been chosen, don't do anything.
                    db.session.rollback()
                    flash('Inside Integrity Error')
        # redirect to the newly created conversation
        return redirect(url_for('convo_view', room_id=room_id, convo_id=convo_id))
    # GET
    return render_template('write_public_convo.html', public_convo_form=public_convo_form, found_room=found_room)


@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/edit', methods=['GET', 'POST'])
@ login_required
def convo_edit(room_id, convo_id):
    # instantiate a new form to edit the convo
    edit_public_convo_form = EditPublicConvoForm()
    # look up the room and convo in the db
    found_room = ForumRoom.query.filter_by(id=room_id).one()
    found_convo = Conversation.query.filter_by(id=convo_id).one()

    # POST
    if edit_public_convo_form.validate_on_submit():
        # all the user's form data is valid, proceed to create the public convo
        found_convo.convo_name = edit_public_convo_form.convo_name.data
        found_convo.convo_summary = edit_public_convo_form.convo_summary.data
        found_convo.convo_init_body = edit_public_convo_form.convo_init_body.data

        # experiment
        db_set = ConvoChosenCondition.query.filter_by(conversation_id=convo_id).all()
        old_set = set()
        for each in db_set:
            old_set.add(each.condition_name)

        new_set = set(edit_public_convo_form.chosen_conditions.data)

        if len(old_set) > len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_convo_condition(condition_name=each, conversation_id=convo_id)
        elif len(old_set) == len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_convo_condition(condition_name=each, conversation_id=convo_id)

        # Otherwise fall through and add the condition
        for condition in edit_public_convo_form.chosen_conditions.data:
            # if user has condition, don't try add it, skip it
            if queries.chk_convo_has_condition_in_db(condition_name=condition, conversation_id=convo_id):
                continue
            else:
                try:
                    new_condition = ConvoChosenCondition(condition_name=condition, conversation_id=convo_id)
                    db.session.add(new_condition)
                    db.session.commit()
                except IntegrityError:
                    # if the condition has already been chosen, don't do anything.
                    db.session.rollback()
                    flash('Inside Integrity Error')
        # end experiment
        # commit changes to database (no need to add to session)
        db.session.commit()
        flash('Your Conversation Has Been Updated Successfully.')
        redirect(url_for('convo_edit', room_id=room_id, convo_id=convo_id))
    # GET
    # pre-populate conversation form with data from the database
    edit_public_convo_form.convo_name.data = found_convo.convo_name
    edit_public_convo_form.convo_summary.data = found_convo.convo_summary
    edit_public_convo_form.convo_init_body.data = found_convo.convo_init_body
    found_conditions = ConvoChosenCondition.query.filter_by(conversation_id=convo_id).all()
    edit_public_convo_form.chosen_conditions.data = [(item.condition_name) for item in found_conditions]
    # GET
    return render_template('edit_public_conversation.html', edit_public_convo_form=edit_public_convo_form, found_room=found_room, found_convo=found_convo)


@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/remove', methods=['GET', 'POST'])
@ login_required
def convo_remove(room_id, convo_id):
    # locate conversation for deletion
    found_convo = Conversation.query.filter_by(id=convo_id).first()
    # delete the room
    db.session.delete(found_convo)
    # commit changes to database
    db.session.commit()
    flash(f'Conversation: {found_convo.convo_name} Has Been Destroyed Successfully.')
    return redirect(url_for('room_view', room_id=room_id))


######## RESPONSE #######

@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/response/<int:resp_id>', methods=['GET', 'POST'])
@ login_required
def response_view(room_id, convo_id, resp_id):
    found_room = ForumRoom.query.filter_by(id=room_id)
    found_convo = Conversation.query.filter_by(id=convo_id)
    found_resp = ConvoResponse.query.filter_by(id=resp_id)

    return render_template('public_response.html', found_resp=found_resp)


@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/write_response', methods=['GET', 'POST'])
@ login_required
def response_write(room_id, convo_id):

    public_resp_form = PublicRespForm()
    # POST
    if public_resp_form.validate_on_submit():
        resp_mention_processor = RespMentionProcessor(public_resp_form, room_id, convo_id)
        resp_mention_processor.find_user_mentions()
        resp_mention_processor.process_collected_mentions()
        resp_mention_processor.set_forum_user_mentions()
        return redirect(url_for('convo_view', room_id=room_id, convo_id=convo_id))
    # GET
    return render_template('write_forum_response.html', public_resp_form=public_resp_form, room_id=room_id, convo_id=convo_id)


@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/response/<int:resp_id>/edit', methods=['GET', 'POST'])
@ login_required
def response_edit(room_id, convo_id, resp_id):
    print(resp_id)
    response = ConvoResponse.query.filter_by(id=resp_id).one()

    eprf_form = EditPublicRespForm()
    # POST
    if eprf_form.validate_on_submit():
        # process mentions
        resp_mention_edit_processor = RespMentionEditProcessor(eprf_form, room_id, convo_id, resp_id)
        resp_mention_edit_processor.find_user_mentions_for_edit()
        resp_mention_edit_processor.process_collected_mentions_for_edit()
        resp_mention_edit_processor.set_forum_user_mentions_for_edit()
        flash('Your Response was Updated Successfully.')
        return redirect(url_for('convo_view', room_id=room_id, convo_id=convo_id))
    # GET
    # pre-populate the form with information stored in the database
    eprf_form.body.data = response.body
    return render_template('edit_forum_response.html', eprf_form=eprf_form, room_id=room_id, convo_id=convo_id, resp_id=resp_id)


@app.route('/forum_rooms/<int:room_id>/convos/<int:convo_id>/response/<int:resp_id>/remove', methods=['GET', 'POST'])
@ login_required
def response_remove(room_id, convo_id, resp_id):
    # locate response
    found_resp = ConvoResponse.query.filter_by(id=resp_id).one()
    # add to session
    db.session.delete(found_resp)
    # commit to db
    db.session.commit()
    flash(f'Response ID: {found_resp.id} Has Been Removed Successfully.')
    # redirect to convo
    return redirect(url_for('convo_view', room_id=room_id, convo_id=convo_id))

###########################################################
### INDEX
###########################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


###########################################################
### LANDING PAGE
###########################################################

# landing page for all user_types (public information, willing to share)
@app.route('/landing_page/<int:user_id>', methods=['GET', 'POST'])
@login_required
def landing_page(user_id):
    # Look up user based on unique user id
    found_user = queries.get_user(user_id=user_id)
    # get conditions of user whose page is being viewed
    found_conditions = ChosenCondition.query.filter_by(user_id=user_id).all()
    # check monitoring status of user_id
    chk_if_monitoring_user = queries.chk_if_monitoring_user(monitor_id=current_user.id, monitoree_id=user_id)
    print(f'Check If Monitoring User Status: {chk_if_monitoring_user}')

    return render_template('landing_page.html', found_user=found_user, found_conditions=found_conditions, queries=queries, chk_if_monitoring_user=chk_if_monitoring_user)


###########################################################
### SPLASHBOARD & ROUTES
###########################################################

@app.route('/patient_splashboard', methods=['GET', 'POST'])
@login_required
def patient_splashboard():
    return render_template('patient_splashboard.html')


@app.route('/provider_splashboard', methods=['GET', 'POST'])
@login_required
def provider_splashboard():
    return render_template('provider_splashboard.html')


@app.route('/monitored_user_entry_feed', methods=['GET', 'POST'])
@login_required
def monitored_user_entry_feed():
    # get list of all monitored users (monitorees)
    with queries.transaction():
        monitored_entries = list(queries.get_monitored_entries(monitor_id=current_user.id))
    print(list(queries.get_monitored_entries(monitor_id=current_user.id)))
    print(f'Get monitored users list: {monitored_entries}')

    return render_template('monitored_user_entry_feed.html', monitored_entries=monitored_entries, queries=queries)


@app.route('/monitored_journal_entry_feed', methods=['GET', 'POST'])
@login_required
def monitored_journal_entry_feed():
    # get list of all monitored users (monitorees)
    with queries.transaction():
        monitored_entries = list(queries.get_monitored_journal_entries(monitor_id=current_user.id))
    print(list(queries.get_monitored_journal_entries(monitor_id=current_user.id)))
    print(f'Get monitored journal users list: {monitored_entries}')

    return render_template('monitored_journal_entry_feed.html', monitored_entries=monitored_entries, queries=queries)


@app.route('/monitored_blog_entry_feed', methods=['GET', 'POST'])
@login_required
def monitored_blog_entry_feed():
    # get list of all monitored users (monitorees)
    with queries.transaction():
        monitored_entries = list(queries.get_monitored_blog_entries(monitor_id=current_user.id))
    print(list(queries.get_monitored_blog_entries(monitor_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_entries}')

    return render_template('monitored_blog_entry_feed.html', monitored_entries=monitored_entries, queries=queries)


@app.route('/monitored_user_response_feed', methods=['GET', 'POST'])
@login_required
def monitored_user_response_feed():
    # get list of all monitored users (monitorees)
    with queries.transaction():
        monitored_responses = list(queries.get_monitored_responses(monitor_id=current_user.id))
    print(list(queries.get_monitored_responses(monitor_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_responses}')

    return render_template('monitored_user_response_feed.html', monitored_responses=monitored_responses, queries=queries)


@app.route('/monitored_patient_response_feed', methods=['GET', 'POST'])
@login_required
def monitored_patient_response_feed():
    # get list of all monitored patients (monitorees)
    with queries.transaction():
        monitored_responses = list(queries.get_monitored_patient_responses(monitor_id=current_user.id))
    print(list(queries.get_monitored_patient_responses(monitor_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_responses}')

    return render_template('monitored_patient_response_feed.html', monitored_responses=monitored_responses, queries=queries)


@app.route('/monitored_provider_response_feed', methods=['GET', 'POST'])
@login_required
def monitored_provider_response_feed():
    # get list of all monitored patients (monitorees)
    with queries.transaction():
        monitored_responses = list(queries.get_monitored_provider_responses(monitor_id=current_user.id))
    print(list(queries.get_monitored_provider_responses(monitor_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_responses}')

    return render_template('monitored_provider_response_feed.html', monitored_responses=monitored_responses, queries=queries)


@app.route('/monitored_provider_journal_mentions', methods=['GET', 'POST'])
@login_required
def monitored_provider_journal_mentions():
    with queries.transaction():
        monitored_mentions = list(queries.get_monitored_provider_journal_mentions(current_user_id=current_user.id))
    print(list(queries.get_monitored_provider_journal_mentions(current_user_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_mentions}')

    return render_template('monitored_provider_journal_mentions.html', monitored_mentions=monitored_mentions, queries=queries)


@app.route('/monitored_provider_forum_mentions', methods=['GET', 'POST'])
@login_required
def monitored_provider_forum_mentions():
    with queries.transaction():
        monitored_mentions = list(queries.get_monitored_provider_forum_mentions(current_user_id=current_user.id))
    print(list(queries.get_monitored_provider_forum_mentions(current_user_id=current_user.id)))
    print(f'Get monitored blog users list: {monitored_mentions}')

    return render_template('monitored_provider_forum_mentions.html', monitored_mentions=monitored_mentions, queries=queries)


@app.route('/show_granted_access_users', methods=['GET', 'POST'])
@login_required
def show_granted_access_users():
    # get list of all monitored users (grantees)
    with queries.transaction():
        granted_access_users = list(queries.get_granted_privacy_access_users(grantor_id=current_user.id))
    print(list(queries.get_granted_privacy_access_users(grantor_id=current_user.id)))
    print(f'Get monitored users list: {granted_access_users}')

    return render_template('show_granted_access_users.html', granted_access_users=granted_access_users, queries=queries)


@app.route('/list_private_access_user_journals', methods=['GET', 'POST'])
@login_required
def list_private_access_user_journals():
    # get list of all monitored users (grantees)
    with queries.transaction():
        users_who_granted_me_private_access = list(queries.get_users_who_granted_me_privacy_access(grantee_id=current_user.id))
    print(list(queries.get_users_who_granted_me_privacy_access(grantee_id=current_user.id)))
    print(f'Get monitored users list: {users_who_granted_me_private_access}')

    return render_template('list_private_access_user_journals.html', users_who_granted_me_private_access=users_who_granted_me_private_access, queries=queries)


@app.route('/forum_convos_of_interest', methods=['GET', 'POST'])
@login_required
def forum_convos_of_interest():
    # get conversation that would interest the current user
    with queries.transaction():
        convos_of_interest = list(queries.get_convos_of_interest(user_id=current_user.id))

    return render_template('convos_of_interest.html', convos_of_interest=convos_of_interest)


# rename query maybe later, the name is not optimal, but query works correctly (come back later)
@app.route('/recommend_patient_to_patient_associations', methods=['GET', 'POST'])
@login_required
def recommend_patient_to_patient_associations():
    # get conversation that would interest the current user
    with queries.transaction():
        patient_to_patient_associations = list(queries.recommend_patient_to_patient_associations(current_user_id=current_user.id))

    return render_template('recommend_patient_to_patient_associations.html', patient_to_patient_associations=patient_to_patient_associations)


@app.route('/recommend_provider_associations', methods=['GET', 'POST'])
@login_required
def recommend_provider_associations():
    with queries.transaction():
        provider_associations = list(queries.recommend_provider_associations(current_user_id=current_user.id))

    return render_template('recommend_provider_associations.html', provider_associations=provider_associations)


@app.route('/get_grantor_private_access_user_journals', methods=['GET', 'POST'])
@login_required
def get_grantor_private_access_user_journals():
    # get conversation that would interest the current user
    with queries.transaction():
        grantor_private_access_user_journals = list(queries.get_grantor_private_access_user_journals(grantee_id=current_user.id))

    return render_template('grantor_private_access_user_journals.html', grantor_private_access_user_journals=grantor_private_access_user_journals, queries=queries)


@app.route('/who_mentioned_me_lately', methods=['GET', 'POST'])
@login_required
def who_mentioned_me_lately():
    #
    with queries.transaction():
        who_mentioned_me = list(queries.who_mentioned_me_lately(current_user_id=current_user.id))

    return render_template('who_mentioned_me_lately.html', who_mentioned_me=who_mentioned_me)


@app.route('/match_out_of_network_specialists', methods=['GET', 'POST'])
@login_required
def match_out_of_network_specialists():
    specialists = list(queries.match_out_of_network_specialists(user_id=current_user.id))
    return render_template('match_out_of_network_specialists.html', specialists=specialists)


@app.route('/crisis_information', methods=['GET', 'POST'])
@login_required
def crisis_information():
    # GET
    return render_template('crisis_information.html')


###########################################################
### GRANT / REMOVE PRIVACY ACCESS
###########################################################

@app.route('/grant_patient_privacy_access/<int:user_id>', methods=['GET', 'POST'])
@login_required
def grant_privacy_access(user_id):
    # get the grantree user
    grantee_user = queries.get_user(user_id=user_id)

    if current_user.id != user_id:
        flash(f"You Have Granted { grantee_user['user_alias'] } Privacy Access")
        with queries.transaction():
            grantor_result = queries.set_privacy_access_relationship(grantor_id=current_user.id, grantee_id=user_id)
            print(f'MONITOR DEBUG: {grantor_result}')
            print('\n')
    else:
        flash('You Cannot Grant Privacy Access To Yourself.')

    # return user back to the user's landing page, after granting privacy access
    return redirect(url_for('landing_page', user_id=user_id))


@app.route('/remove_privacy_access/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove_privacy_access(user_id):
    # retrieve user that is having privacy access removed
    ungranted_user = queries.get_user(user_id=user_id)
    print(ungranted_user)
    # remove privacy access relationship
    remove_privacy_access = queries.remove_privacy_access(grantor_id=current_user.id, grantee_id=user_id)
    flash(f"You Have Removed Privacy Access For { ungranted_user['user_alias'] }.")
    # return the user back to the user's landing page.
    return redirect(url_for('landing_page', user_id=user_id))


###########################################################
### MONITOR
###########################################################

@app.route('/show_monitored_users', methods=['GET', 'POST'])
def show_monitored_users():
    monitored_users = queries.get_monitored_users(monitor_id=current_user.id)

    return render_template('show_monitored_users.html', monitored_users=monitored_users)


# monitoring user_type: 'patient'
@app.route('/monitor_patient/<int:user_id>', methods=['GET', 'POST'])
@login_required
def monitor_patient(user_id):
    # get the monitoree user
    monitoree_user = queries.get_user(user_id=user_id)

    if current_user.id != user_id:
        flash(f"You are now monitoring { monitoree_user['user_alias'] }")
        with queries.transaction():
            monitor_result = queries.set_monitoring_relationship(monitor_id=current_user.id, monitoree_id=user_id)
            print(f'MONITOR DEBUG: {monitor_result}')
            print('\n')
    else:
        flash('You cannot monitor yourself.')

    # return user back to the patient's landing page, after following them
    return redirect(url_for('landing_page', user_id=user_id))


# monitoring user_type: 'provider'
@app.route('/monitor_provider/<int:user_id>', methods=['GET', 'POST'])
@login_required
def monitor_provider(user_id):
    # get the monitoree user
    monitoree_user = queries.get_user(user_id=user_id)

    if current_user.id != user_id:
        flash(f"You are now monitoring { monitoree_user['user_alias'] }")
        with queries.transaction():
            monitor_result = queries.set_monitoring_relationship(monitor_id=current_user.id, monitoree_id=user_id)
            print(f'MONITOR DEBUG: {monitor_result}')
            print('\n')
    else:
        flash('You cannot monitor yourself.')
    # return user back to the provider's landing page, after following them
    return redirect(url_for('landing_page', user_id=user_id))


# monitored feed (give me all user posts by people I monitor
@app.route('/monitoring_feed', methods=['GET', 'POST'])
@login_required
def monitoring_feed():
    # Look up user based on unique user id
    get_monitored_entries = list(queries.get_monitored_entries(monitor_id=current_user.id))
    print(get_monitored_entries)
    return render_template('monitored_entries.html', get_monitored_entries=get_monitored_entries)


# monitoree feed (give me all user posts by users that are monitoring me
@app.route('/monitoree_feed', methods=['GET', 'POST'])
@login_required
def monitoree_feed():
    # Look up user based on unique user id
    get_monitoree_entries = list(queries.get_monitoree_entries(monitoree_id=current_user.id))
    print(get_monitoree_entries)
    return render_template('monitoree_entries.html', get_monitoree_entries=get_monitoree_entries)


@app.route('/un_monitor/<int:user_id>', methods=['GET', 'POST'])
@login_required
def un_monitor(user_id):
    # retrieve user that is being unmonitored
    unmonitored_user = queries.get_user(user_id=user_id)
    print(unmonitored_user)
    # remove monitoring relationship
    remove_monitoring = queries.un_monitor_user(monitor_id=current_user.id, monitoree_id=user_id)
    flash(f"You are not monitoring { unmonitored_user['user_alias'] } anymore.")
    # return the user back to the unmonitored person's landing page.
    return redirect(url_for('landing_page', user_id=user_id))


###########################################################
### SEARCH
###########################################################

@app.route('/search_site', methods=['GET', 'POST'])
@login_required
def search_site():
    # if not g.third_search_form.validate():
    #     return redirect(url_for('index'))
    current_page = request.args.get('current_page', 1, type=int)
    raw_search_query = request.args.get('search')
    print(raw_search_query)
    print(type(raw_search_query))
    # prepare search query for to_tsquery format per PostgreSQL Full-Text Search Documentation format:

    print(f"First time in /search, PAGE value: {current_page}")
    print(f"FIRST TIME IN /search, form data passed: {raw_search_query}")
    process_query = []
    process_query = raw_search_query.split(' ')
    final_search_query = ''
    for term in process_query:
        final_search_query += " | " + term
        print(final_search_query)
    final_search_query = final_search_query[3:]
    print(f"The FINAL SEARCH TERM: {final_search_query}")

    # Documentation: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
    #results = BlogEntry.query.filter(BlogEntry.__ts_vector__.match(final_search_query, postgresql_regconfig='english')).paginate(per_page=5, page=page, error_out=True)
    forum_results = ConvoResponse.query.filter(ConvoResponse.__ts_vector__.match(final_search_query, postgresql_regconfig='english')).paginate(per_page=4, page=current_page, error_out=True)

    # results = db.session.query(User.id, BlogEntry.title, BlogEntry.body, ConvoResponse.body).distinct()\
    #                     .join(BlogEntry, BlogEntry.user_id == User.id)\
    #                     .join(ConvoResponse, ConvoResponse.user_id == User.id) \
    #                     .group_by(User.id, BlogEntry.title, BlogEntry.body, ConvoResponse.body) \
    #                     .filter(BlogEntry.__ts_vector__.match(final_search_query, postgresql_regconfig='english')) \
    #                     .filter(ConvoResponse.__ts_vector__.match(final_search_query, postgresql_regconfig='english')) \
    #                     .paginate(per_page=5, page=page, error_out=True)
    # # add the forum results to the blog results
    # for user_id, be_title, be_body, cr_body in results.items:
    #     print(f'BLOG Result: Title: {be_title}, Body: {be_body}')
    #     print(f'FORUM Result: Response Body: {cr_body}')

    # get total number of results
    #total = BlogEntry.query.filter(BlogEntry.__ts_vector__.match(final_search_query, postgresql_regconfig='english')).paginate(per_page=5, page=page, error_out=True).total
    #print(f"The TOTAL is: {total}")
    print(f"FORM DATA PASSED: {g.search_site_form.search.data}")

    return render_template('search_site_results.html', forum_results=forum_results, raw_search_query=raw_search_query)


# old search method
# @app.route('/third_search', methods=['GET', 'POST'])
# @login_required
# def third_search():
#
#     # if not g.third_search_form.validate():
#     #     return redirect(url_for('index'))
#     page = request.args.get('page', 1, type=int)
#     raw_search_query = request.args.get('search')
#     print(raw_search_query)
#     print(type(raw_search_query))
#     # prepare search query for to_tsquery format per PostgreSQL Full-Text Search Documentation format:
#
#     print(f"First time in /search, PAGE value: {page}")
#     print(f"FIRST TIME IN /search, form data passed: {raw_search_query}")
#     process_query = []
#     process_query = raw_search_query.split(' ')
#     final_search_query = ''
#     for term in process_query:
#         final_search_query += " | " + term
#         print(final_search_query)
#     final_search_query = final_search_query[3:]
#     print(f"The FINAL SEARCH TERM: {final_search_query}")
#
#     # experiment
#
#     # end experiment
#
#     # Documentation: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
#     results = BlogEntry.query.filter(BlogEntry.__ts_vector__.match(final_search_query, postgresql_regconfig='english')).paginate(per_page=5, page=page, error_out=True)
#     # get total number of results
#     total = BlogEntry.query.filter(BlogEntry.__ts_vector__.match(final_search_query, postgresql_regconfig='english')).paginate(per_page=5, page=page, error_out=True).total
#     print(f"The TOTAL is: {total}")
#     print(f"FORM DATA PASSED: {g.third_search_form.search.data}")
#     next_url = url_for('third_search', search=raw_search_query, page=page + 1) \
#         if total > page * 5 else None
#     prev_url = url_for('third_search', search=raw_search_query, page=page - 1) \
#         if page > 1 else None
#
#     return render_template('third_search_results.html', results=results, next_url=next_url, prev_url=prev_url)


###########################################################
### USER ACCOUNT
###########################################################

@app.route('/user_account/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_account(user_id):
    # look up user via unique user id
    found_user = User.query.filter_by(id=user_id)
    acct_edit_form = AccountEditForm()
    # POST
    if acct_edit_form.validate_on_submit():
        # GET (pre-populate form with current database filed entries)
        current_user.email = acct_edit_form.email.data
        current_user.user_alias = acct_edit_form.user_alias.data
        current_user.password = generate_password_hash(acct_edit_form.password.data, method='sha256', salt_length=32)
        current_user.first_name = acct_edit_form.first_name.data
        current_user.last_name = acct_edit_form.last_name.data
        current_user.addr_street = acct_edit_form.addr_street.data
        current_user.addr_city = acct_edit_form.addr_city.data
        current_user.addr_state = acct_edit_form.addr_state.data
        current_user.addr_zip = acct_edit_form.addr_zip.data
        current_user.addr_country = acct_edit_form.addr_country.data
        current_user.ph_number = acct_edit_form.ph_number.data
        # Store account image if available
        if acct_edit_form.account_img.data:
            img_processor = ImageProcessor(acct_edit_form.account_img.data)
            picture_name = img_processor.format_img_for_account()
            current_user.account_img = picture_name
            print(f'Changed current_user.account_img value: {current_user.account_img}')
            print(picture_name)
        # end store account image section
        current_user.seeking_status = acct_edit_form.seeking_status.data
        current_user.non_searchable = acct_edit_form.non_searchable.data

        print(acct_edit_form.chosen_conditions.data)
        #########################
        #### PUGSQL Option #1: Update Conditions
        #########################
        # # delete conditions
        # queries.remove_user_conditions(user_id=current_user.id)
        # # set the chosen conditions
        # for condition in acct_edit_form.chosen_conditions.data:
        #     queries.set_user_condition(condition_name=condition, user_id=current_user.id)

        #########################
        #### SQLALCHEMY Option #2: Update Conditions
        #########################

        db_set = ChosenCondition.query.filter_by(user_id=current_user.id).all()
        old_set = set()
        for each in db_set:
            old_set.add(each.condition_name)

        new_set = set(acct_edit_form.chosen_conditions.data)

        if len(old_set) > len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_user_condition(condition_name=each, user_id=current_user.id)
        elif len(old_set) == len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_user_condition(condition_name=each, user_id=current_user.id)

        # Otherwise fall through and add the condition
        for condition in acct_edit_form.chosen_conditions.data:
            # if user has condition, don't try add it, skip it
            if queries.chk_user_has_condition_in_db(condition_name=condition, user_id=current_user.id):
                continue
            else:
                try:
                    new_condition = ChosenCondition(condition_name=condition, user_id=current_user.id)
                    db.session.add(new_condition)
                    db.session.commit()
                except IntegrityError:
                    # if the condition has already been chosen, don't do anything.
                    db.session.rollback()
                    flash('Inside Integrity Error')

        current_user.bio = acct_edit_form.bio.data
        current_user.chosen_insurance = acct_edit_form.chosen_insurance.data
        # commit changes to database
        db.session.commit()
        flash('Your Account Information Has Been Updated Successfully.')
        redirect(url_for('user_account', user_id=user_id))

    # GET (pre-populate form with current database filed entries
    acct_edit_form.email.data = current_user.email
    acct_edit_form.user_alias.data = current_user.user_alias
    acct_edit_form.password.data = current_user.password
    acct_edit_form.first_name.data = current_user.first_name
    acct_edit_form.last_name.data = current_user.last_name
    acct_edit_form.addr_street.data = current_user.addr_street
    acct_edit_form.addr_city.data = current_user.addr_city
    acct_edit_form.addr_state.data = current_user.addr_state
    acct_edit_form.addr_zip.data = current_user.addr_zip
    acct_edit_form.addr_country.data = current_user.addr_country
    acct_edit_form.ph_number.data = current_user.ph_number
    # no need to pre-populate image, the field will appear automatically when the form loads.
    acct_edit_form.seeking_status.data = current_user.seeking_status
    acct_edit_form.non_searchable.data = current_user.non_searchable
    found_conditions = ChosenCondition.query.filter_by(user_id=current_user.id).all()
    acct_edit_form.chosen_conditions.data = [(item.condition_name) for item in found_conditions]
    acct_edit_form.bio.data = current_user.bio
    acct_edit_form.chosen_insurance.data = current_user.chosen_insurance

    return render_template('user_account.html', acct_edit_form=acct_edit_form)


@app.route('/insurance_provider_out_net_svces', methods=['GET', 'POST'])
@login_required
def insurance_provider_out_net_svces():

    out_net_svces_form = ProvInsuranceSrvces()

    # POST
    if out_net_svces_form.validate_on_submit():
        db_set = OutOfNetServicesFor.query.filter_by(user_id=current_user.id).all()
        old_set = set()
        for each in db_set:
            old_set.add(each.insurance_name)

        new_set = set(out_net_svces_form.insurance_name.data)

        if len(old_set) > len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_insurance_choice(insurance_name=each, user_id=current_user.id)
        elif len(old_set) == len(new_set):
            delete_set = old_set - new_set
            for each in delete_set:
                queries.remove_specific_insurance_choice(insurance_name=each, user_id=current_user.id)

        # Otherwise fall through and add the condition
        for insurance in out_net_svces_form.insurance_name.data:
            # if user has condition, don't try add it, skip it
            if queries.chk_user_insurance_choice_is_in_db(insurance_name=insurance, user_id=current_user.id):
                continue
            else:
                try:
                    new_insurance = OutOfNetServicesFor(insurance_name=insurance, user_id=current_user.id)
                    db.session.add(new_insurance)
                    db.session.commit()
                except IntegrityError:
                    # if the insurance has already been chosen, don't do anything.
                    db.session.rollback()
                    flash('Inside Integrity Error')
        flash('Your Out-of-Network Insurance Choices Have Been Updated Successfully.')
        redirect(url_for('insurance_provider_out_net_svces'))
    # GET (Pre-populate the form with database data)
    found_insurance_companies = OutOfNetServicesFor.query.filter_by(user_id=current_user.id).all()
    out_net_svces_form.insurance_name.data = [(item.insurance_name) for item in found_insurance_companies]

    return render_template('insurance_provider_out_net_svces.html', out_net_svces_form=out_net_svces_form)


###########################################################
### REGISTER
###########################################################

@app.route('/register', methods=['GET', 'POST'])
def register():
    # check if user logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserRegisterForm()
    # POST
    if form.validate_on_submit():
        # hash the pw user entered
        hash_user_pw = generate_password_hash(form.password.data, method='sha256', salt_length=32)
        # create new user
        new_user = User(first_name=form.first_name.data,\
                        last_name=form.last_name.data,\
                        user_alias=form.user_alias.data,\
                        email=form.email.data,\
                        user_type=form.user_type.data,\
                        password=hash_user_pw)
        db.session.add(new_user)
        # commit to db
        db.session.commit()
        flash('You have successfully registered. You were automatically logged in.')
        login_user(new_user, remember=True)
        # return to home screen
        return redirect(url_for('index'))
    # GET
    return render_template('register.html', form=form)


###########################################################
### LOGIN
###########################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserLoginForm()
    # POST
    if form.validate_on_submit():
        # look up user
        user = User.query.filter_by(email=form.email.data).first()

        #if user and password check out
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # record last login date and time UTC
            with queries.transaction():
                login_result = queries.set_last_login_date(user_id=current_user.id)

            # redirect user to page they tried to access (if they did)
            if 'next' in session and session['next']:
                print(session['next'])
                original_destination = session['next']
                session['next'] = ''
                session.modified = True
                return redirect(original_destination)
            else:
                return redirect(url_for('index'))
        else:
            flash('We Could Not Log You In, Please Try Again!')
    # GET
    return render_template('login.html', form=form)


###########################################################
### LOGOUT
###########################################################

@app.route('/logout', methods=['GET'])
def logout():
    # log the current user out
    logout_user()
    # once logged out, redirect them to the home page
    return redirect(url_for('index'))


@app.route('/pug_test', methods=['GET', 'POST'])
def pug_test():
    # run a PugSQL test function
    with queries.transaction():
        single_result = queries.select_user_test(id_arg=1)
        print(single_result)
        print('\n')

    # Get all Posts Test
    with queries.transaction():
        entries = list(queries.get_all_entries())
        print(entries)
        print('\n')

    # JOIN Test: JOIN 3 tables, and return various column values across all tables.
    with queries.transaction():
        join_results = list(queries.join_test())
        print(join_results)

    return render_template('pug_test.html', single_result=single_result, entries=entries, join_results=join_results)


###########################################################
### SEARCH FOR USER ALIAS
###########################################################
@app.route('/search_for_user_alias', methods=['GET', 'POST'])
@login_required
def search_for_user_alias():
    search_form = SearchUserAliasForm()
    # POST
    if search_form.validate_on_submit():
        print(search_form.search.data)
        user_alias = search_form.search.data
        results = list(queries.get_search_results_for_user_alias(user_alias=user_alias))
        print(results)
        return render_template('search_for_user_alias.html', search_form=search_form, results=results)
    # GET
    return render_template('search_for_user_alias.html', search_form=search_form)


###########################################################
### CHANGE PASSWORD
###########################################################
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():

    chg_pw_form = ChangePasswordForm()
    # POST
    if chg_pw_form.validate_on_submit():
        # hash the pw user entered
        hash_user_pw = generate_password_hash(chg_pw_form.password.data, method='sha256', salt_length=32)
        # find the current user
        found_user = User.query.filter_by(id=current_user.id).one()
        # update their new password
        found_user.password = hash_user_pw
        # commit to db
        db.session.commit()
        flash('Your Password Has Been Changed.')
        # return to home screen
        return redirect(url_for('index'))
    # GET
    return render_template('change_password.html', chg_pw_form=chg_pw_form)
