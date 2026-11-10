from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0011_golferseason_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='TournamentGolfer',
            name='position',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='overall_score',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='r1_strokes',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='r2_strokes',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='r3_strokes',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='r4_strokes',
            field=models.CharField(max_length=16, null=True)
        ),
        migrations.AddField(
            model_name='TournamentGolfer',
            name='total_strokes',
            field=models.CharField(max_length=16, null=True)
        )
    ]
