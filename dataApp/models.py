from django.db import models
import re
    
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['name']) < 2:
            errors["name"] = "Name is too short"
        if len(reqPOST['email']) < 6:
            errors["email"] = "Email is too short"
        if len(reqPOST['password']) < 8:
            errors["password"] ="Password is too short"
        if reqPOST["password"] != reqPOST["password_conf"]:
            errors["match"] ="Password and password confirmation do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email address!"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email already taken."
        return errors



class User(models.Model):
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()




class TherapistManager(models.Manager):
    def therapist_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['name']) < 2:
            errors["name"] = "Name is too short"
        if len(reqPOST['hours']) < 1:
            errors["hours"] = "Please enter number of hours worked"
        if len(reqPOST['wages']) < 1:
            errors["wages"] = "Please enter wages"
        return errors
    

class Therapist(models.Model):
    name = models.TextField()
    hours = models.IntegerField()
    wages = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TherapistManager()

    
class ClientManager(models.Manager):
    def client_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['name']) < 2:
            errors["name"] = "Name is too short."
        if len(reqPOST['sessions']) < 1:
            errors["sessions"] = "Please enter number of sessions."
        if len(reqPOST['evaluation']) < 1:
            errors["evaluation"] = "Please enter number of evaluations."
        if len(reqPOST['no_show']) < 1:
            errors["no_show"] = "Please enter number of no_shows."
        
        return errors


class Client(models.Model):
    name = models.CharField(max_length=255)
    sessions = models.IntegerField()
    evaluation = models.IntegerField()
    noshow = models.IntegerField()
    therapists = models.ManyToManyField(Therapist, related_name = "clients")
    copay = models.DecimalField(decimal_places=2, max_digits=8)
    insurance_amt = models.DecimalField(decimal_places=2, max_digits=8)
    total_charges = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ClientManager()
