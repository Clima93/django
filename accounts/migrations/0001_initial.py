# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=300, null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='HardSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, unique=True, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=500)),
                ('responsibility', models.TextField(blank=True)),
                ('job_type', models.CharField(max_length=100, blank=True)),
                ('min_salary', models.CharField(max_length=500, blank=True)),
                ('max_salary', models.CharField(max_length=500, blank=True)),
                ('job_level', models.CharField(max_length=100, blank=True)),
                ('start_date', models.DateField(max_length=100, null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('industry', models.CharField(max_length=500, null=True, blank=True)),
                ('department', models.CharField(max_length=500, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('currency', models.CharField(max_length=100, null=True, blank=True)),
                ('work_location', models.CharField(max_length=500, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('education_level', models.CharField(max_length=100, null=True, blank=True)),
                ('institution_not_needed', models.BooleanField(default=False)),
                ('training', models.CharField(max_length=500, null=True, blank=True)),
                ('work_experience', models.TextField(null=True, blank=True)),
                ('skill_not_needed', models.BooleanField(default=False)),
                ('language_not_needed', models.BooleanField(default=False)),
                ('personality', models.TextField(null=True, blank=True)),
                ('contacts', models.CharField(max_length=500, null=True, blank=True)),
                ('sex', models.CharField(max_length=20, null=True, blank=True)),
                ('age', models.CharField(max_length=20, null=True, blank=True)),
                ('company_name', models.CharField(max_length=500, null=True, blank=True)),
                ('company_size', models.CharField(max_length=500, null=True, blank=True)),
                ('hard_skills', models.ManyToManyField(to='accounts.HardSkill', blank=True)),
                ('institutions', models.ManyToManyField(to='accounts.Institute', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('reading_level', models.CharField(max_length=100, blank=True)),
                ('writing_level', models.CharField(max_length=100, blank=True)),
                ('verbal_level', models.CharField(max_length=100, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=1000)),
                ('link_info', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(max_length=500, upload_to='profile_upload', blank=True)),
                ('company_logo', models.ImageField(max_length=500, upload_to='company_logo', blank=True)),
                ('email_verification_code', models.CharField(max_length=250, blank=True)),
                ('email_validation_expire', models.DateTimeField(default=datetime.datetime(2018, 2, 26, 17, 45, 10, 416000))),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('d_o_b', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True, choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('category', models.CharField(blank=True, max_length=50, null=True, choices=[('Job Seeker', 'Job Seeker'), ('Employer', 'Employer'), ('Service Seeker', 'Service Seeker'), ('Service Provider', 'Service Provider')])),
                ('work_industry', models.CharField(max_length=250, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('profile_complete', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
                ('heard_from', models.CharField(max_length=500, null=True, blank=True)),
                ('phone', models.CharField(max_length=25, null=True, blank=True)),
                ('phone_code', models.CharField(max_length=5, null=True, blank=True)),
                ('personal_statement', models.TextField(null=True, blank=True)),
                ('company_size', models.CharField(max_length=300, null=True, blank=True)),
                ('company_name', models.CharField(max_length=500, null=True, blank=True)),
                ('work_location', models.CharField(max_length=300, null=True, blank=True)),
                ('job_level', models.CharField(max_length=100, null=True, blank=True)),
                ('availability', models.CharField(max_length=100, null=True, blank=True)),
                ('min_salary', models.CharField(max_length=100, null=True, blank=True)),
                ('max_salary', models.CharField(max_length=100, null=True, blank=True)),
                ('salary_currency', models.CharField(max_length=100, null=True, blank=True)),
                ('employer_industry', models.CharField(max_length=500, null=True, blank=True)),
                ('department', models.CharField(max_length=500, null=True, blank=True)),
                ('application_details', models.BooleanField(default=False)),
                ('document', models.FileField(max_length=500, null=True, upload_to='documents', blank=True)),
                ('job_seeker_auto_welcome', models.BooleanField(default=False)),
                ('employer_auto_welcome', models.BooleanField(default=False)),
                ('service_provider_auto_welcome', models.BooleanField(default=False)),
                ('service_seeker_auto_welcome', models.BooleanField(default=False)),
                ('newsletter_register', models.BooleanField(default=False)),
                ('hard_skills', models.ManyToManyField(to='accounts.HardSkill', blank=True)),
                ('industry', models.ManyToManyField(to='accounts.Industry', blank=True)),
                ('skills', models.ManyToManyField(to='accounts.Skill', blank=True)),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
                ('verbal_level', models.CharField(max_length=100, blank=True)),
                ('writing_level', models.CharField(max_length=100, blank=True)),
                ('reading_level', models.CharField(max_length=100, blank=True)),
                ('profile', models.ForeignKey(related_name='languages', to='accounts.UserAccount', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('negotiable', models.BooleanField()),
                ('company_name', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('company_website', models.CharField(max_length=500, blank=True)),
                ('location', models.CharField(max_length=200)),
                ('testimonial', models.CharField(max_length=1000, blank=True)),
                ('price', models.CharField(max_length=500)),
                ('business_details', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('links', models.ManyToManyField(to='accounts.Link', blank=True)),
                ('prices', models.ManyToManyField(to='accounts.Price', blank=True)),
                ('profile', models.ForeignKey(related_name='services', blank=True, to='accounts.UserAccount', null=True)),
                ('service', models.ForeignKey(related_name='users', to='accounts.Service')),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=300, null=True, blank=True)),
                ('employer_name', models.CharField(max_length=300, null=True, blank=True)),
                ('job_title', models.CharField(max_length=300, null=True, blank=True)),
                ('responsibility', models.TextField(null=True, blank=True)),
                ('achievements', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(related_name='experience', blank=True, to='accounts.UserAccount', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkIndustry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('verification_code', models.CharField(max_length=250, blank=True)),
                ('start_time', models.DateTimeField(default=datetime.datetime(2018, 2, 21, 16, 45, 10, 405000, tzinfo=utc))),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='profile',
            field=models.ForeignKey(related_name='links', to='accounts.UserAccount'),
        ),
        migrations.AddField(
            model_name='job',
            name='languages',
            field=models.ManyToManyField(to='accounts.JobLanguage', blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='profile',
            field=models.ForeignKey(related_name='jobs', to='accounts.UserAccount'),
        ),
        migrations.AddField(
            model_name='job',
            name='skills',
            field=models.ManyToManyField(to='accounts.Skill', blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='viewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='education',
            name='institute',
            field=models.ForeignKey(blank=True, to='accounts.Institute', null=True),
        ),
        migrations.AddField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(related_name='education', blank=True, to='accounts.UserAccount', null=True),
        ),
    ]
