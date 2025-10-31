# voter_analytics/models.py
# Gracious Ogyiri Asare- gpoa@bu.edu

# define data models for the voter_analytics app
from django.db import models


# Create your models here.
class Voter(models.Model):
    '''Model representing a voter. '''
    
    #define data fields of the Voter model
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    street_number = models.TextField(blank=True)
    street_name = models.TextField(blank=True)
    apartment_number = models.TextField(blank=True)
    zip_code = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.TextField(blank=True)
    precinct = models.TextField(blank=True)

    v20state = models.BooleanField(blank=True)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField()

    def __str__(self):
        '''String for representing the Model object.'''
        return f'Voter: {self.first_name} {self.last_name}, Address: {self.street_number} {self.street_name}, Apt: {self.apartment_number}, Zip: {self.zip_code}'
    
    
def load_data():
        '''Function to load data records from CSV file.'''
        Voter.objects.all().delete() 
        filename = 'newton_voters.csv'
        f = open(filename)
        f.readline() 
 
        for line in f:
            field = line.strip().split(',')
            try:
                result = Voter(
                    last_name = field[1].strip(),
                    first_name = field[2].strip(),
                    street_number = field[3].strip(),
                    street_name = field[4].strip(),
                    apartment_number = field[5].strip(),
                    zip_code = field[6].strip(),
                    dob = field[7].strip(),
                    date_of_registration = field[8].strip(),
                    party_affiliation = field[9].strip(),
                    precinct = field[10].strip(),
                    # for boolean fields, convert strings to boolean values
                    v20state = field[11].strip().upper() == 'TRUE',
                    v21town = field[12].strip().upper() == 'TRUE',
                    v21primary = field[13].strip().upper() == 'TRUE',
                    v22general = field[14].strip().upper() == 'TRUE',
                    v23town = field[15].strip().upper() == 'TRUE',
                    voter_score = int(field[16]) if field[16] else 0,

                )
                result.save() # commit to database
                # print(f'Created result: {result}')
            except:
                print(f'Invalid data at {line}')
                print(f'Created {len(Voter.objects.all())}')