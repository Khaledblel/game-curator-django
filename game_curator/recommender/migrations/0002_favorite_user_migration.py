from django.db import migrations, models
import django.db.models.deletion

def set_default_user(apps, schema_editor):
    # Get the User model from apps to ensure we're using the historical version
    User = apps.get_model('auth', 'User')
    Favorite = apps.get_model('recommender', 'Favorite')
    
    # Get or create a default admin user if it exists
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Set all existing favorites to the admin user
    Favorite.objects.filter(user__isnull=True).update(user=admin_user)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.RunPython(set_default_user),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'game_id')},
        ),
    ]