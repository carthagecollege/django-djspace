# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from djspace.application.models import *
from djtools.fields.widgets import MonthYearWidget
from djtools.fields import BINARY_CHOICES

from taggit.models import Tag

class HigherEducationInitiativesForm(forms.ModelForm):

    time_frame = forms.DateField(widget=MonthYearWidget)

    class Meta:
        model = HigherEducationInitiatives
        exclude = ('user','status','funds_authorized','authorized_match')
        fields = [
            'project_title','award_type','funds_requested','proposed_match',
            'source_match','time_frame','location','synopsis','proposal'
        ]

class ResearchInfrastructureForm(forms.ModelForm):

    time_frame = forms.DateField(widget=MonthYearWidget)

    class Meta:
        model = ResearchInfrastructure
        exclude = ('user','status','funds_authorized','authorized_match')
        fields = [
            'project_title','award_type','funds_requested','proposed_match',
            'source_match','time_frame','location','synopsis','proposal'
        ]


class AerospaceOutreachForm(forms.ModelForm):

    project_category = forms.TypedChoiceField(
        choices = PROJECT_CATEGORIES, widget = forms.RadioSelect()
    )
    time_frame = forms.DateField(
        widget=MonthYearWidget
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = AerospaceOutreach
        fields = [
            'project_title','project_category','location','time_frame',
            'funds_requested','proposed_match','source_match',
            'other_funding','other_funding_explain',
            'synopsis', 'proposal',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone'
        ]
        exclude = ('user','status','funds_authorized','authorized_match')


class SpecialInitiativesForm(forms.ModelForm):

    project_category = forms.TypedChoiceField(
        choices = PROJECT_CATEGORIES, widget = forms.RadioSelect()
    )
    time_frame = forms.DateField(widget=MonthYearWidget)
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    proposed_match = forms.IntegerField(
        label = "Proposed match (1:1 mimimum)(in $)",
        help_text = """
            Match must be 50% for ongoing program;
            25% for new innovated programs (or)
            programs with significant legacy value.
        """
    )
    source_match = forms.CharField(
        label = "Source(s) of match",
        help_text = """
            Overhead (or indirect costs) cannot exceed 0.5
            of the required matching funds
        """
    )

    class Meta:
        model = SpecialInitiatives
        fields = [
            'project_title','project_category','location','time_frame',
            'funds_requested','proposed_match','source_match',
            'other_funding','other_funding_explain', 'synopsis', 'proposal',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone'
        ]
        exclude = ('user','status','funds_authorized','authorized_match')


class UndergraduateScholarshipForm(forms.ModelForm):

    academic_institution = forms.TypedChoiceField(
        label = "Application submitted for",
        widget = forms.RadioSelect(),
        choices=ACADEMIC_INSTITUTIONS
    )

    class Meta:
        model = UndergraduateScholarship
        exclude = ('user','status')


class UndergraduateResearchForm(forms.ModelForm):

    class Meta:
        model = UndergraduateResearch
        exclude = ('user','status','funds_authorized')


class GraduateFellowshipForm(forms.ModelForm):

    class Meta:
        model = GraduateFellowship
        exclude = ('user','status','funds_authorized')


class ClarkGraduateFellowshipForm(forms.ModelForm):

    class Meta:
        model = ClarkGraduateFellowship
        exclude = ('user','status','funds_authorized')


class HighAltitudeBalloonPayloadForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonPayload
        exclude = ('user','status')


class HighAltitudeBalloonLaunchForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonLaunch
        exclude = ('user','status')


class RocketLaunchTeamForm(forms.ModelForm):
    """
    Form that handles the create/update for Rocket Launch Teams
    """

    leader = forms.CharField(
        help_text = '''
            Start typing the last name to see results. If you do not find the
            team leader or if the team leader has not yet registered with WSGC,
            you can leave this field blank for now.
        ''',
        required = False
    )
    tags = forms.ModelMultipleChoiceField(
        label="In which WSGC rocket competitions will your team compete?",
        queryset=Tag.objects.filter(name__in=ROCKET_COMPETITIONS).order_by("name"),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = RocketLaunchTeam
        exclude = ('user','members','status',)
        #fields = ['name','academic_institution_name'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RocketLaunchTeamForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Assign a User object to leader
        """
        cd = self.cleaned_data
        lid = cd.get("leader")
        if lid:
            try:
                user = User.objects.get(pk=lid)
                cd["leader"] = user
                self.request.session["leader_id"] = user.id
                self.request.session["leader_name"] = u"{}, {}".format(
                    user.last_name, user.first_name
                )
            except:
                cd["leader"] = None
        else:
            cd["leader"] = None

        return cd


class FirstNationsRocketCompetitionForm(forms.ModelForm):

    class Meta:
        model = FirstNationsRocketCompetition
        exclude = ('user','status')


class MidwestHighPoweredRocketCompetitionForm(forms.ModelForm):

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        exclude = ('user','status')

    def __init__(self, *args, **kwargs):
        super(MidwestHighPoweredRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(tags__name__in=["Midwest High Powered Rocket Competition"]).exclude(
            count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
        ).order_by("name")


class CollegiateRocketCompetitionForm(forms.ModelForm):

    class Meta:
        model = CollegiateRocketCompetition
        exclude = ('user','status')

    def __init__(self, *args, **kwargs):
        super(CollegiateRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(tags__name__in=["Collegiate Rocket Competition"]).exclude(
            count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
        ).order_by("name")


class NasaCompetitionForm(forms.ModelForm):

    program_acceptance = forms.TypedChoiceField(
        label = "Has your team applied and been accepted into the program?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = NasaCompetition
        exclude = (
            'user','status','funds_authorized','authorized_match'
        )


class IndustryInternshipForm(forms.ModelForm):

    class Meta:
        model = IndustryInternship
        exclude = (
            'user','status','work_plan','funds_authorized','authorized_match'
        )

