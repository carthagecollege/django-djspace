# -*- coding: utf-8 -*-

from django import forms

from djspace.application.models import *

class UndergraduateScholarshipForm(forms.ModelForm):
    """
    """

    class Meta:
        model = UndergraduateScholarship
        exclude = ('user','status')


class UndergraduateResearchForm(forms.ModelForm):
    """
    """

    class Meta:
        model = UndergraduateResearch
        exclude = ('user','status','funds_authorized')


class GraduateFellowshipForm(forms.ModelForm):
    """
    """

    class Meta:
        model = GraduateFellowship
        exclude = ('user','status','funds_authorized')


class ClarkFellowshipForm(forms.ModelForm):
    """
    """

    class Meta:
        model = ClarkFellowship
        exclude = ('user','status','funds_authorized')

class HighAltitudeBalloonPayloadForm(forms.ModelForm):
    """
    """

    class Meta:
        model = HighAltitudeBalloonPayload
        exclude = ('user','status')

class HighAltitudeBalloonLaunchForm(forms.ModelForm):
    """
    """

    class Meta:
        model = HighAltitudeBalloonLaunch
        exclude = ('user','status')

