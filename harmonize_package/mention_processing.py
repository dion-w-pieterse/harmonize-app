from harmonize_package import db, queries, current_user
from flask import render_template, flash, redirect, url_for
from harmonize_package.models import BlogEntry
from harmonize_package.image_processing import ImageProcessor
from harmonize_package.sentiment_analysis import SentimentAnalyzer
import re


class MentionProcessor:

    def __init__(self, form):
        self.entry_body = form.body.data
        # create list for verified mentions
        self.user_mentions = []
        self.validated_mentions = []
        self.form = form


    def find_user_mentions(self):
        user_mention_list = []
        possible_user_mention = ''
        # tokenize the entry body into list of space delimited words
        # token_list = entry_body.split(' ')
        token_list = re.split(' |\r\n|\n', self.entry_body)
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


    def set_blog_user_mentions(self):
        if len(self.validated_mentions) != 0:
            # now add validated mentions to user_blogs_mentions table (process list into set)
            unique_validated_aliases = set(self.validated_mentions)
            # read the id of the latest blog entry from the database
            blog_entry_id = queries.get_latest_blog_entry_id()
            for alias in unique_validated_aliases:
                # look up user by unique alias
                user_id = queries.get_user_id_by_alias(user_alias=alias)['id']
                print(f'Check type: {user_id}')
                if queries.chk_if_blog_mention_row_exists(blog_entry_id=blog_entry_id, user_id=user_id):
                    continue
                else:
                    queries.set_user_blogs_mention(blog_entry_id=blog_entry_id, user_id=user_id)
        return

    def process_collected_mentions(self):
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
                    entry_body = self.form.body.data
                    # Now find recommendations for invalid mentions
                    for invalid_alias in invalid_mentions:
                        best_replace_aliases = ', '.join(d_obj['user_alias'] for d_obj in list(queries.get_recommended_user_aliases(user_alias=invalid_alias)))
                        # replace misspelled mention with first result from from get_recommended_user_aliases
                        corrected_entry_body = entry_body.replace(invalid_alias, f'<< @{ invalid_alias } Did you mean: {best_replace_aliases} >>')

                    print(f'Corrected body of text: {corrected_entry_body}')
                    # set invalid alias flag (for front-end styling)
                    incorrect_alias_detected = True
                    print(incorrect_alias_detected)
                    if self.form.entry_img.data:
                        print('CASE: INVALID MENTION AND IMAGE')
                        # process image name
                        img_processor = ImageProcessor(self.form.entry_img.data)
                        picture_name = img_processor.format_img_for_blog()
                        # update sentiment analysis values
                        # instantiate analyzer
                        sent_analyzer = SentimentAnalyzer(corrected_entry_body)
                        # get polarity scores
                        polarity_scores = sent_analyzer.get_polarity_scores()

                        # create a new entry with the suggestions for the incorrect user alias(s) not spelled right.
                        entry = BlogEntry(title=self.form.title.data, body=corrected_entry_body, entry_img=picture_name, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                        # add post to db session
                        db.session.add(entry)
                        # commit db session
                        db.session.commit()
                        # if any valid mentions made it into the validated_mentions list, record them in the db.
                        # if len(self.validated_mentions) != 0:
                        #     self.set_blogs_user_mentions(self.validated_mentions)
                        flash('CASE: INVALID MENTION AND IMAGE')
                        return redirect(url_for('blog', user_id=current_user.id))
                    else:
                        print('CASE: INVALID MENTION AND NO IMAGE')
                        # update sentiment analysis values
                        # instantiate analyzer
                        sent_analyzer = SentimentAnalyzer(corrected_entry_body)
                        # get polarity scores
                        polarity_scores = sent_analyzer.get_polarity_scores()
                        # create a new entry with the suggestions for the incorrect user alias(s) not spelled right.
                        entry = BlogEntry(title=self.form.title.data, body=corrected_entry_body, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                        # add post to db session
                        db.session.add(entry)
                        # commit db session
                        db.session.commit()
                        # if any valid mentions made it into the validated_mentions list, record them in the db.
                        # if len(self.validated_mentions) != 0:
                        #     self.set_blogs_user_mentions(self.validated_mentions)
                        flash('CASE: INVALID MENTION AND NO IMAGE')
                        return redirect(url_for('blog', user_id=current_user.id))
            # Here is if there is a mention and it is a valid user_alias (need 2 cases: img and no image)
            if self.form.entry_img.data:
                print('CASE: VALID MENTION AND IMAGE')
                img_processor = ImageProcessor(self.form.entry_img.data)
                picture_name = img_processor.format_img_for_blog()
                ##################################################
                # update sentiment analysis values
                # instantiate analyzer
                sent_analyzer = SentimentAnalyzer(self.form.body.data)
                # get polarity scores
                polarity_scores = sent_analyzer.get_polarity_scores()
                blog_entry = BlogEntry(title=self.form.title.data, entry_img=picture_name, body=self.form.body.data, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                # add entry to session
                db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: VALID MENTION AND IMAGE')
                return redirect(url_for('blog', user_id=current_user.id))
            else:
                print('CASE: VALID MENTION AND NO IMAGE')
                # update sentiment analysis values
                # instantiate analyzer
                sent_analyzer = SentimentAnalyzer(self.form.body.data)
                # get polarity scores
                polarity_scores = sent_analyzer.get_polarity_scores()
                blog_entry = BlogEntry(title=self.form.title.data, body=self.form.body.data, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                # add entry to session
                db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: VALID MENTION AND NO IMAGE')
                return redirect(url_for('blog', user_id=current_user.id))
        else:
            # No mentions were made, so now create img and no-img cases inside the else block
            if self.form.entry_img.data:
                print('CASE: NO MENTION AND IMAGE')
                # create a new entry (no user mentions were written)
                # process image name
                img_processor = ImageProcessor(self.form.entry_img.data)
                picture_name = img_processor.format_img_for_blog()
                ##################################################
                # update sentiment analysis values
                # instantiate analyzer
                sent_analyzer = SentimentAnalyzer(self.form.body.data)
                # get polarity scores
                polarity_scores = sent_analyzer.get_polarity_scores()
                blog_entry = BlogEntry(title=self.form.title.data, entry_img=picture_name, body=self.form.body.data, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                # add entry to session
                db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: NO MENTION AND IMAGE')
                return redirect(url_for('blog', user_id=current_user.id))
            else:
                print('CASE: NO MENTION AND NO IMAGE')
                # update sentiment analysis values
                # instantiate analyzer
                sent_analyzer = SentimentAnalyzer(self.form.body.data)
                # get polarity scores
                polarity_scores = sent_analyzer.get_polarity_scores()
                blog_entry = BlogEntry(title=self.form.title.data, body=self.form.body.data, private_entry=self.form.private_entry.data, analysis_neg_score=polarity_scores['neg'], analysis_neu_score=polarity_scores['neu'], analysis_pos_score=polarity_scores['pos'], analysis_compound_score=polarity_scores['compound'], user_id=current_user.id)
                # add entry to session
                db.session.add(blog_entry)
                # commit to db
                db.session.commit()
                flash('CASE: NO MENTION AND NO IMAGE')
                return redirect(url_for('blog', user_id=current_user.id))
