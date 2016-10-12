# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djspace.registration.choices import MAJORS, YEAR_CHOICES
from djspace.registration.choices import UNDERGRADUATE_DEGREE, GRADUATE_DEGREE
from djspace.core.models import GenericChoice
from djspace.core.models import Base

from djtools.fields import STATE_CHOICES
from djtools.fields.validators import *


def limit_affiliation():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["WSGC Affiliates","College or University"]
        ).order_by("ranking")
    ]
    return ids

def limit_college_university():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["College or University",]
        ).order_by("ranking")
    ]
    return ids

class BaseStudent(Base):
    class Meta:
        abstract = True

    # core
    major = models.CharField(
        "Primary major",
        max_length=128,
        choices=MAJORS
    )
    major_other = models.CharField(
        "If Other, please state",
        max_length=128,
        null=True, blank=True
    )
    secondary_major_minor = models.CharField(
        "Secondary major or minor",
        max_length=128,
        null=True, blank=True,
        choices=MAJORS
    )
    secondary_major_minor_other = models.CharField(
        "If Other, please state",
        max_length=128,
        null=True, blank=True
    )
    current_cumulative_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_in_major = models.CharField(
        "GPA in major",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_scale = models.CharField(
        "GPA scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    cumulative_college_credits = models.CharField(
        "Cumulative college credits",
        max_length=6,
        validators=[credit_gpa_validator]
    )
    month_year_of_graduation = models.CharField(
        "Expected month and year of graduation",
        max_length=7,
        validators=[month_year_validator]
    )
    studentid = models.CharField(
        "Student Id Number",
        max_length=64
    )


class Undergraduate(BaseStudent):
    highschool_name = models.CharField(
        "High school name",
        max_length=128
    )
    highschool_city = models.CharField(
        "High school city",
        max_length=128
    )
    highschool_state = models.CharField(
        "High school state",
        max_length=2,
        choices=STATE_CHOICES
    )
    class_year = models.CharField(
        "Current Class Status",
        max_length=24,
        choices=YEAR_CHOICES
    )
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        #limit_choices_to={"id__in":limit_college_university},
        verbose_name="College or University",
        related_name="undergraduate_student_wsgc_affiliate",
        help_text="FNL Participants: Choose 'OTHER.'",
        max_length=128,
        on_delete=models.SET_NULL,
        null=True,
    )


class Graduate(BaseStudent):
    college_university = models.CharField(
        "College or university",
        max_length=255
    )
    undergraduate_degree = models.CharField(
        max_length=32,
        choices=UNDERGRADUATE_DEGREE
    )
    degree_program = models.CharField(
        max_length=32,
        choices=GRADUATE_DEGREE
    )
    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        null=True, blank=True,
    )
    concentration_area = models.CharField(
        "Concentration area (eg. physics, astronomy, physiology, etc.)",
        max_length=128
    )
    graduate_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_scale = models.CharField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_graduation_year = models.CharField(
        "Anticipated graduation year",
        max_length=4,
        validators=[four_digit_year_validator]
    )
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        #limit_choices_to={"id__in":limit_college_university},
        verbose_name="College or University",
        related_name="graduate_student_wsgc_affiliate",
        help_text="FNL Participants: Choose 'OTHER.'",
        max_length=128,
        on_delete=models.SET_NULL,
        null=True,
    )

class Faculty(Base):

    # core
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        #limit_choices_to={"id__in":limit_affiliation},
        verbose_name="WSGC Affiliate",
        related_name="faculty_wsgc_affiliate",
        on_delete=models.SET_NULL,
        null=True,
        help_text = """
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """
    )
    department_program = models.CharField(
        "Department / Program",
        max_length=128
    )
    title = models.CharField(
        "Title (eg. Assistant Prof., Associate Prof., Prof.)",
        max_length=128
    )
    web_site = models.CharField(
        "Web site",
        max_length=128,
        help_text = "eg. www.mywebsite.com",
        null=True, blank=True,
    )

    class Meta:
        verbose_name_plural = "Faculty"


class Professional(Base):

    # core
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        #limit_choices_to={"id__in":limit_affiliation},
        verbose_name="WSGC Affiliate",
        related_name="professional_wsgc_affiliate",
        on_delete=models.SET_NULL,
        null=True,
        help_text = """
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """
    )
    sponsoring_organization_name = models.CharField(
        "Name",
        max_length=128,
        null=True, blank=True
    )
    sponsoring_organization_address1 = models.CharField(
        "Address",
        max_length=128,
        null=True, blank=True
    )
    sponsoring_organization_address2 = models.CharField(
        "",
        max_length=128,
        null=True, blank=True
    )
    sponsoring_organization_city = models.CharField(
        "City",
        max_length=128,
        null=True, blank=True
    )
    sponsoring_organization_state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES,
        null=True, blank=True
    )
    sponsoring_organization_postal_code = models.CharField(
        "Zip code",
        max_length=10,
        null=True, blank=True
    )
    sponsoring_organization_contact = models.CharField(
        "Contact",
        max_length=128,
        null=True, blank=True
    )
    sponsoring_organization_description = models.TextField(
        "Description",
        null=True, blank=True
    )

