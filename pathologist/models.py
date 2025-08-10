from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient  # Import the existing Patient model


# ----------------------------------------
# Pathologist Model
# ----------------------------------------
class Pathologist(models.Model):
    """
    Stores details for a Pathologist profile.
    Linked one-to-one with Django's built-in User model.
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to user account
    profile_pic = models.ImageField(
        upload_to='profile_pic/PathologistProfilePic/',
        null=True,
        blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=True)  # Active/Inactive status

    @property
    def get_name(self):
        """Return the full name of the pathologist."""
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        """Return the associated user's ID."""
        return self.user.id

    def __str__(self):
        """Readable name in admin & shell."""
        return f"{self.user.first_name} ({self.user.last_name})"


# ----------------------------------------
# Report Model
# ----------------------------------------
class Report(models.Model):
    """
    Stores uploaded reports for patients.
    - Linked to a Patient (one patient can have multiple reports).
    - Includes the report name, file, and upload timestamp.
    """
    report_id = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to patient
    report_name = models.CharField(max_length=100)  # Example: "Blood Test Report"
    file = models.FileField(upload_to='reports/')  # File upload path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation

    def __str__(self):
        """Readable name in admin & shell."""
        return f"{self.report_name} - {self.report_id}"  # Shows report name + patient
