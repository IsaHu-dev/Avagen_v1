from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('account', '0003_auto_20250602_2248'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS account_emailaddress (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES auth_user(id),
                email VARCHAR(254) NOT NULL,
                verified BOOLEAN NOT NULL DEFAULT FALSE,
                primary BOOLEAN NOT NULL DEFAULT FALSE,
                UNIQUE(email)
            );
            CREATE TABLE IF NOT EXISTS account_emailconfirmation (
                id SERIAL PRIMARY KEY,
                email_address_id INTEGER NOT NULL REFERENCES account_emailaddress(id),
                created TIMESTAMP WITH TIME ZONE NOT NULL,
                sent TIMESTAMP WITH TIME ZONE,
                key VARCHAR(64) NOT NULL UNIQUE
            );
            """,
            """
            DROP TABLE IF EXISTS account_emailconfirmation;
            DROP TABLE IF EXISTS account_emailaddress;
            """
        ),
    ] 