import os
import secrets
from PIL import Image, ImageEnhance
from harmonize_package import app


class ImageProcessor:

    def __init__(self, user_image):
        self.user_image = user_image
        self.original_filename, self.file_extension = os.path.splitext(self.user_image.filename)
        self.PATH_USER_ACCOUNT_IMGS = 'static/user_account_imgs'
        self.PATH_USER_BLOG_IMGS = 'static/user_blog_imgs'
        self.PATH_USER_FORUM_IMGS = 'static/user_forum_imgs'
        self.USER_ACCT_IMG_DIM = (500, 500)
        self.BLOG_ENTRY_IMG_DIM = (1200, 400)
        self.FORUM_ENTRY_IMG_DIM = (1200, 400)


    def format_img_for_account(self):
        # generate new filename
        img_filename = secrets.token_urlsafe(32)
        print(f'img_filename generated: {img_filename}')
        # build new unique filename
        unique_filename = img_filename + self.file_extension
        print(f'unique_filename generated: {unique_filename}')
        # build image path
        full_img_path = os.path.join(app.root_path, self.PATH_USER_ACCOUNT_IMGS, unique_filename)
        print(f'full_img_path generated: {full_img_path}')
        # Load the image for Pillow
        account_img = Image.open(self.user_image)
        print(f'account_img generated: {account_img}')
        # keep aspect ratio and resize
        account_img.thumbnail(self.USER_ACCT_IMG_DIM)
        # save the uploaded image to the pertaining app directory
        account_img.save(full_img_path)
        # return the reformatted filename to be saved in the database
        print(f'unique_filename returned: {unique_filename}')
        return unique_filename


    def format_img_for_blog(self):
        # generate new filename
        img_filename = secrets.token_urlsafe(32)
        print(f'img_filename generated: {img_filename}')
        # build new unique filename
        unique_filename = img_filename + self.file_extension
        print(f'unique_filename generated: {unique_filename}')
        # build image path
        full_img_path = os.path.join(app.root_path, self.PATH_USER_BLOG_IMGS, unique_filename)
        print(f'full_img_path generated: {full_img_path}')
        # Load the image for Pillow
        blog_entry_img = Image.open(self.user_image)
        print(f'blog_entry_img generated: {blog_entry_img}')
        # keep aspect ratio and resize
        blog_entry_img.thumbnail(self.BLOG_ENTRY_IMG_DIM)
        # save the uploaded image to the pertaining app directory
        blog_entry_img.save(full_img_path)
        # return the reformatted filename to be saved in the database
        print(f'unique_filename returned: {unique_filename}')
        return unique_filename


    def format_img_for_forum(self):
        # generate new filename
        img_filename = secrets.token_urlsafe(32)
        print(f'img_filename generated: {img_filename}')
        # build new unique filename
        unique_filename = img_filename + self.file_extension
        print(f'unique_filename generated: {unique_filename}')
        # build image path
        full_img_path = os.path.join(app.root_path, self.PATH_USER_FORUM_IMGS, unique_filename)
        print(f'full_img_path generated: {full_img_path}')
        # Load the image for Pillow
        blog_entry_img = Image.open(self.user_image)
        print(f'blog_entry_img generated: {blog_entry_img}')
        # keep aspect ratio and resize
        blog_entry_img.thumbnail(self.FORUM_ENTRY_IMG_DIM)
        # save the uploaded image to the pertaining app directory
        blog_entry_img.save(full_img_path)
        # return the reformatted filename to be saved in the database
        print(f'unique_filename returned: {unique_filename}')
        return unique_filename


