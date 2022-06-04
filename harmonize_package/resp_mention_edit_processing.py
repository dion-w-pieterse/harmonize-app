from harmonize_package import db, queries, current_user
from flask import render_template, flash, redirect, url_for
from harmonize_package.models import BlogEntry, ConvoResponse
from harmonize_package.image_processing import ImageProcessor
import re


class RespMentionEditProcessor:

    def __init__(self, form, room_id, convo_id, resp_id):
        self.resp_body = form.body.data
        # create list for verified mentions
        self.user_mentions = []
        self.validated_mentions = []
        self.form = form
        self.room_id = room_id
        self.conversation_id = convo_id
        self.resp_id = resp_id # blog_entry_id
        #self.user_id = user_id


    def find_user_mentions_for_edit(self):
        user_mention_list = []
        possible_user_mention = ''
        # tokenize the entry body into list of space delimited words
        # token_list = resp_body.split(' ')
        token_list = re.split(' |\r\n|\n', self.resp_body)
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
        # populate user_mentions class list
        self.user_mentions = user_alias_recommendations
        return


    def set_forum_user_mentions_for_edit(self):
        if len(self.validated_mentions) != 0:
            # now add validated mentions to user_blogs_mentions table (process list into set)
            unique_validated_aliases = set(self.validated_mentions)
            # read the id of the latest blog entry from the database
            #blog_entry_id = queries.get_latest_blog_entry_id()
            # remove all rows from previous write or edit (takes care of historical mentions that are no longer present
            num_del_rows = queries.remove_all_mentions_of_alias_for_resp(convo_response_id=self.resp_id)
            print(f"Num of deleted rows: {num_del_rows}")
            for alias in unique_validated_aliases:
                # look up user by unique alias
                user_id = queries.get_user_id_by_alias(user_alias=alias)['id']
                print(f'Check type: {user_id}')

                if queries.chk_if_forum_mention_row_exists(convo_response_id=self.resp_id, user_id=user_id):
                    continue
                else:
                    queries.set_user_forum_mention(convo_response_id=self.resp_id, user_id=user_id)
        return

    def process_collected_mentions_for_edit(self):
        # if any user_mentions were typed in the entry body
        if len(self.user_mentions) != 0:
            print(f'Length of user_mentions is: {len(self.user_mentions)}')
            invalid_mentions = []
            # check each mention in the list of potential mentions
            for user_alias in self.user_mentions:
                print(f'Checking potential mention: {user_alias}')
                if queries.get_user_alias(user_alias=user_alias):
                    # found user_alias, add to validated mentions list and continue to next iteration
                    self.validated_mentions.append(user_alias)
                    continue
                else:
                    print(f'inside else: adding to invalid_mention list')
                    invalid_mentions.append(user_alias)
                    # get original entry text
                    resp_body = self.form.body.data
                    # Now find recommendations for invalid mentions
                    for invalid_alias in invalid_mentions:
                        best_replace_aliases = ', '.join(d_obj['user_alias'] for d_obj in list(queries.get_recommended_user_aliases(user_alias=invalid_alias)))
                        # replace misspelled mention with first result from from get_recommended_user_aliases
                        corrected_resp_body = resp_body.replace(invalid_alias, f'<< @{ invalid_alias } Did you mean: {best_replace_aliases} >>')

                    print(f'Corrected body of text: {corrected_resp_body}')
                    # set invalid alias flag (for front-end styling)
                    incorrect_alias_detected = True
                    print(incorrect_alias_detected)
                    if self.form.resp_img.data:
                        print('CASE: INVALID MENTION AND IMAGE')
                        # process image name
                        img_processor = ImageProcessor(self.form.resp_img.data)
                        picture_name = img_processor.format_img_for_forum()
                        # create a new entry with the suggestions for the incorrect user alias(s) not spelled right.
                        #entry = BlogEntry(title=self.form.title.data, body=corrected_resp_body, resp_img=picture_name, private_entry=self.form.private_entry.data, user_id=current_user.id)
                        # look up existing blog entry
                        forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                        forum_response.body = corrected_resp_body
                        forum_response.resp_img = picture_name
                        #db.session.add(entry)
                        # commit db session
                        db.session.commit()
                        # if any valid mentions made it into the validated_mentions list, record them in the db.
                        # if len(self.validated_mentions) != 0:
                        #     self.set_blogs_user_mentions(self.validated_mentions)
                        flash('CASE: INVALID MENTION AND IMAGE')
                        return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
                    else:
                        print('CASE: INVALID MENTION AND NO IMAGE')
                        # create a new entry with the suggestions for the incorrect user alias(s) not spelled right.
                        #entry = BlogEntry(title=self.form.title.data, body=corrected_resp_body, private_entry=self.form.private_entry.data, user_id=current_user.id)
                        # add post to db session
                        forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                        forum_response.body = corrected_resp_body
                        #db.session.add(entry)
                        # commit db session
                        db.session.commit()
                        # if any valid mentions made it into the validated_mentions list, record them in the db.
                        # if len(self.validated_mentions) != 0:
                        #     self.set_blogs_user_mentions(self.validated_mentions)
                        flash('CASE: INVALID MENTION AND NO IMAGE')
                        return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
            # Here is if there is a mention and it is a valid user_alias (need 2 cases: img and no image)
            if self.form.resp_img.data:
                print('CASE: VALID MENTION AND IMAGE')
                img_processor = ImageProcessor(self.form.resp_img.data)
                picture_name = img_processor.format_img_for_forum()
                ##################################################
                #blog_entry = BlogEntry(title=self.form.title.data, resp_img=picture_name, body=self.form.body.data, private_entry=self.form.private_entry.data, user_id=current_user.id)
                # add entry to session
                forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                forum_response.body = self.form.body.data
                forum_response.resp_img = picture_name
                #db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: VALID MENTION AND IMAGE')
                return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
            else:
                print('CASE: VALID MENTION AND NO IMAGE')
                #blog_entry = BlogEntry(title=self.form.title.data, body=self.form.body.data, private_entry=self.form.private_entry.data, user_id=current_user.id)
                # add entry to session
                forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                forum_response.body = self.form.body.data
                #db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: VALID MENTION AND NO IMAGE')
                return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
        else:
            # No mentions were made, so now create img and no-img cases inside the else block
            if self.form.resp_img.data:
                print('CASE: NO MENTION AND IMAGE')
                # remove all rows from previous write or edit (takes care of historical mentions that are no longer present
                num_del_rows = queries.remove_all_mentions_of_alias_for_resp(convo_response_id=self.resp_id)

                # create a new entry (no user mentions were written)
                # process image name
                img_processor = ImageProcessor(self.form.resp_img.data)
                picture_name = img_processor.format_img_for_forum()
                ##################################################
                #blog_entry = BlogEntry(title=self.form.title.data, resp_img=picture_name, body=self.form.body.data, private_entry=self.form.private_entry.data, user_id=current_user.id)
                # add entry to session
                forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                forum_response.body = self.form.body.data
                forum_response.resp_img = picture_name
                #db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: NO MENTION AND IMAGE')
                return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
            else:
                print('CASE: NO MENTION AND NO IMAGE')
                #blog_entry = BlogEntry(title=self.form.title.data, body=self.form.body.data, private_entry=self.form.private_entry.data, user_id=current_user.id)
                # add entry to session
                # remove all rows from previous write or edit (takes care of historical mentions that are no longer present
                num_del_rows = queries.remove_all_mentions_of_alias_for_resp(convo_response_id=self.resp_id)
                forum_response = ConvoResponse.query.filter_by(id=self.resp_id).first()
                forum_response.body = self.form.body.data
                #db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: NO MENTION AND NO IMAGE')
                return redirect(url_for('convo_view', room_id=self.room_id, convo_id=self.conversation_id))
