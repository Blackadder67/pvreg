from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=50)
    def get_people(self):
        return self.person_set.all()
    def __str__(self):
        return '{}) {}'.format(self.pk, self.name)

class Person(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    fname_rus = models.CharField(max_length=20, null=True, blank=True)
    lname_rus = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        unique_together = [('fname', 'lname')]
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    ext = models.CharField(max_length=4, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return '{}) {}'.format(self.pk, self.email)

class PhTherGroup(models.Model):
    name = models.CharField(max_length=300, unique=True)
    def __str__(self):
        return '{}) {}'.format(self.pk, self.name)

class INN(models.Model):
    old_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    ibd = models.DateField(null=True, blank=True)
    def __str__(self):
        return '{}) {}'.format(self.pk, self.name)

class DosageForm(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return '{}'.format(self.name)

class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True)

class Product(models.Model):
    old_id = models.IntegerField(null=True, blank=True)
    eng_name = models.CharField(max_length=50, null=True, blank=True)
    rus_name = models.CharField(max_length=50, null=True, blank=True)
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE, null=True, blank=True)
    strength = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        unique_together = [('eng_name', 'dosage_form')]
    ph_ther_group = models.ForeignKey(PhTherGroup, null=True, blank=True, on_delete=models.CASCADE)
    inns = models.ManyToManyField(INN, null=True, blank=True)
    first_registration_date = models.DateField(null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    rc_number = models.CharField(max_length=30, null=True, blank=True)
    ma_holder = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    rx = 'Rx'
    otc = 'OTC'
    PRESCRIPTION_STATUS_CHOICES = (
        (rx, 'Rx'),
        (otc, 'OTC'),
    )
    prescription_status = models.CharField(max_length=3, choices=PRESCRIPTION_STATUS_CHOICES, null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return '{} {} {}'.format(self.eng_name, self.dosage_form, self.strength)

class ADR(models.Model):
    old_id = models.IntegerField(null=True, blank=True)
    local_number = models.CharField(max_length=20, null=True, blank=True)
    cioms_number = models.CharField(max_length=20, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    received_by_company = models.DateField(null=True, blank=True)
    sent_to_regional_office = models.DateField(null=True, blank=True)
    cioms_received = models.DateField(null=True, blank=True)
    submitted = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    batch_number = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    serious = models.BooleanField(null=True, blank=True)
    expected = models.BooleanField(null=True, blank=True)
    therapy_start_date = models.DateField(null=True, blank=True)
    therapy_stop_date = models.DateField(null=True, blank=True)
    indication = models.CharField(max_length=20, null=True, blank=True)
    daily_dose = models.CharField(max_length=20, null=True, blank=True)
    adr_onset_date = models.DateField(null=True, blank=True)
    adr_outcome_date = models.DateField(null=True, blank=True)
    source_is_patient = models.BooleanField(null=True, blank=True)
    source_is_hcp = models.BooleanField(null=True, blank=True)
    initial_reporter = models.CharField(max_length=200, null=True, blank=True)
    secondary_reporter = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

class PSUR(models.Model):
    old_id = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    submitted = models.DateField(null=True, blank=True)
    recommendations_rus = models.TextField()
    recommendations_eng = models.TextField()
    path_to_folder = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
