# Generated by Django 3.1.2 on 2020-11-17 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotzone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('idNumber', models.CharField(max_length=10)),
                ('dataOfBirth', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='visitedlocationdetail',
            name='caseNumber',
            field=models.ForeignKey(default=1001, on_delete=django.db.models.deletion.CASCADE, to='hotzone.casedetail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casedetail',
            name='caseType',
            field=models.CharField(choices=[('Local', 'Local'), ('Import', 'Import')], max_length=10),
        ),
        migrations.AlterField(
            model_name='casedetail',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotzone.patientdetail'),
        ),
    ]
