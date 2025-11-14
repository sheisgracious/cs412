# blog/serializers.py
# Serializers convert our django data models to a text represtion suitable to transmit over HTTP. 

from rest_framework import serializers # has base classes
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    '''A serializer for the Article model
    Specify which model/fields to send in the API
    '''

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text', 'published', 'image_file']  
    
    # add methods to cusomize the create/read/update/delete operaitions
    def create(self, validated_data):
        #validated_data- data coming from the POST request
        '''overide the superclass method that handles object creation.'''
        print(f'ArticleSerializer.create, validated_data={validated_data}.') 

        '''
        # create an Article object
        article = Article(**validated_data)

        # attach a FK for the User 
        article.user = User.objects.first() 

        # save the object to the database
        article.save()

        # return an object instance
        return article
        '''

        # a simplified way:
        # attach a FK for the User
        validated_data['user'] = User.objects.first()
        # doing the create and save all at once
        return Article.objects.create(**validated_data)
