# dadjokes/serializers.py
# Serializers convert the django data models to a text represtion suitable to transmit over HTTP. 

from rest_framework import serializers # has base classes
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''A serializer for the Joke model
    Specify which model/fields to send in the API
    '''

    class Meta:
        model = Joke
        fields = ['id', 'joke_text', 'contributor', 'timestamp']  
    
    # add methods to cusomize the create/read/update/delete operaitions
    def create(self, validated_data):
        #validated_data- data coming from the POST request
        '''overide the superclass method that handles object creation.'''
        print(f'JokeSerializer.create, validated_data={validated_data}.') 

        
        # create an Joke object
        joke = Joke(**validated_data)

        # save the object to the database
        joke.save()

        # return an object instance
        return joke
     

class PictureSerializer(serializers.ModelSerializer):
    '''A serializer for the Joke model
    Specify which model/fields to send in the API
    '''

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']  
    
    # add methods to cusomize the create/read/update/delete operaitions
    def create(self, validated_data):
        #validated_data- data coming from the POST request
        '''overide the superclass method that handles object creation.'''
        print(f'PictureSerializer.create, validated_data={validated_data}.') 

        
        # create an Joke object
        picture = Picture(**validated_data)

        # save the object to the database
        picture.save()

        # return an object instance
        return picture
     

      