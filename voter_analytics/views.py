# voter_analytics/views.py 
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models.query import QuerySet

import plotly
import plotly.graph_objs as go


# Create your views here.
class VoterListView(ListView):
    '''Display all voters.'''
    model = Voter
    template_name = 'voter_analytics/results.html'
    context_object_name = 'voters' 
    paginate_by = 100  

    def get_queryset(self):
        '''return queryset of voters'''
        results = super().get_queryset().order_by('last_name')

        # filter results by these fields:

        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                results = results.filter(dob__year__lte=int(max_year))

        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                results = results.filter(dob__year__gte=int(min_year))
        
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                results = results.filter(party_affiliation=party)
        
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                results = results.filter(voter_score=int(score))

        if 'v20state' in self.request.GET:
            results = results.filter(v20state=True)
        if 'v21town' in self.request.GET:
            results = results.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            results = results.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            results = results.filter(v22general=True)
        if 'v23town' in self.request.GET:
            results = results.filter(v23town=True)

        return results
    
class ResultDetailView(DetailView):
    '''Display results for single voter.'''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    '''display graphs for voter data.'''
    
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
    
    def get_queryset(self):
        '''Return the queryset of voters, with filtering applied.'''
        
        results = super().get_queryset()
        
        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                results = results.filter(dob__year__lte=int(max_year))

        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                results = results.filter(dob__year__gte=int(min_year))
        
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                results = results.filter(party_affiliation=party)
        
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                results = results.filter(voter_score=int(score))

        if 'v20state' in self.request.GET:
            results = results.filter(v20state=True)
        if 'v21town' in self.request.GET:
            results = results.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            results = results.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            results = results.filter(v22general=True)
        if 'v23town' in self.request.GET:
            results = results.filter(v23town=True)

        return results
    
    def get_context_data(self, **kwargs):
        '''add graphs to the context data.'''
        
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        
        # histogram the distribution of voters by their year of birth.
        birth_year_counts = {}
        for voter in voters:
            if voter.dob:
                year = voter.dob.year
                birth_year_counts[year] = birth_year_counts.get(year, 0) + 1
        
        years = sorted(birth_year_counts.keys())
        counts = [birth_year_counts[year] for year in years]
        
        fig_birth_year = go.Bar(x=years, y=counts)
        graph_birth_year_div = plotly.offline.plot(
            {"data": [fig_birth_year],
             "layout_title_text": "Voter Distribution by Year of Birth",
            },
            auto_open=False,
            output_type='div'
        )
        context['graph_birth_year'] = graph_birth_year_div
        
        # pie chart 
        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation if voter.party_affiliation else 'not found'
            party_counts[party] = party_counts.get(party, 0) + 1
        
        fig_party = go.Pie(labels=list(party_counts.keys()), 
                           values=list(party_counts.values()))
        graph_party_div = plotly.offline.plot(
            {"data": [fig_party],
             "layout_title_text": "Voter Distribution by Party Affiliation",
            },
            auto_open=False,
            output_type='div'
        )
        context['graph_party'] = graph_party_div
        
        #histogram- party affiliation
        elections = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0,
        }
        
        for voter in voters:
            if voter.v20state:
                elections['v20state'] += 1
            if voter.v21town:
                elections['v21town'] += 1
            if voter.v21primary:
                elections['v21primary'] += 1
            if voter.v22general:
                elections['v22general'] += 1
            if voter.v23town:
                elections['v23town'] += 1
        
        fig_elections = go.Bar(
            x=['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'],
            y=[elections['v20state'], elections['v21town'], elections['v21primary'], 
               elections['v22general'], elections['v23town']]
        )
        graph_elections_div = plotly.offline.plot(
            {"data": [fig_elections],
             "layout_title_text": "Vote Count by Election",
            },
            auto_open=False,
            output_type='div'
        )
        context['graph_elections'] = graph_elections_div
        
        return context