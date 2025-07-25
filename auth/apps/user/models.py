from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinLengthValidator
from slugify import slugify
from django.db.models.signals import post_save
import requests
from django.conf import settings
# activecampaign_url = 'https://us21.api.mailchimp.com/3.0/lists/1b8f2c7d6a/members'
import uuid, json
import stripe
import re

pattern_special_characters = r'\badmin\b|[!@#$%^~&*()_+=[]{}|;:",.<>/?]|\s'

# Create your models here.
class User(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        def create_slug(username):
            if re.search(pattern_special_characters, username):
                raise ValueError("Username contains invalid characters.")
            username = re.sub(pattern_special_characters, '', username)
            return slugify(username)
        extra_fields['slug'] = create_slug(extra_fields['username'])

        user = self.model(email = email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        # item = {}
        # item['id'] = str(user.id)
        # item['email'] = user.email
        # item['username'] = user.username
        # producer.produce(
        #     'user_created',
        #     key='create_user',
        #     value=json.dumps(item).encode('utf-8')
        # )
        # producer.flush()

        if user.agreed:
            url = activecampaign_url + '/api/3/contact/async'
            data = {
                'contact': {
                    'email': user.email,
                }
            }
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Api-Token': activecampaign_key
            }
            response = requests.post(url, json=data, headers=headers)

            contact = response.json()

            contac_id = str(contact['contact']['id'])

            url = activecampaign_url + '/api/3/contactTags'
            data = {
                'contactTag': {
                    'contact': contac_id,
                    'tag': '5'
                }
            }

            response = requests.post(url, json=data, headers=headers)

            url = activecampaign_url + '/api/3/contactLists'
            data = {
                'contactList': {
                    'list': '2',
                    'contact': contac_id,
                    'status': 1
                }
            }

            response = requests.post(url, json=data, headers=headers)

        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'Admin'
        user.verified = True
        user.become_seller = True
        user.save(using=self._db)

        return user