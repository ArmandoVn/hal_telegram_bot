# Generated by Django 3.1.7 on 2021-03-17 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageBot',
            fields=[
                ('message_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=220)),
                ('chat_id', models.CharField(max_length=220)),
                ('from_id', models.CharField(max_length=220)),
                ('first_name', models.CharField(max_length=220)),
                ('last_name', models.CharField(max_length=220)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=220)),
                ('context', models.CharField(max_length=220)),
                ('is_text_question', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('next_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='NextQuestion', to='questions.question')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=220)),
                ('context', models.CharField(max_length=220)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('next_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='NextResponseQuestion', to='questions.question')),
                ('parent_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ParentResponseQuestion', to='questions.question')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]