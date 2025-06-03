from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

def fix_duplicate_emails():
    # Get all email addresses
    email_addresses = EmailAddress.objects.all()
    
    # Group by email
    email_dict = {}
    for email in email_addresses:
        if email.email not in email_dict:
            email_dict[email.email] = []
        email_dict[email.email].append(email)
    
    # Fix duplicates
    for email, addresses in email_dict.items():
        if len(addresses) > 1:
            # Keep the primary email address
            primary = next((addr for addr in addresses if addr.primary), addresses[0])
            
            # Delete other duplicates
            for addr in addresses:
                if addr != primary:
                    addr.delete()
            print(f"Fixed duplicate email: {email}")

if __name__ == "__main__":
    fix_duplicate_emails() 