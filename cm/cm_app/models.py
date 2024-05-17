from django.db import models

# Create your models here.
class Requests(models.Model):
    r_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    p_address=models.CharField(max_length=255)

class Users(models.Model):
    u_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    p_address=models.CharField(max_length=255)

class Artists(models.Model):
    u_id=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    p_address=models.CharField(max_length=255)

class Files(models.Model):
    m_id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)

class Musics(models.Model):
    m_id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    date=models.CharField(max_length=255)
    time=models.CharField(max_length=255)
    hash_value=models.CharField(max_length=255)

class Transactionss(models.Model):
    t_id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=255)
    sender_name=models.CharField(max_length=255)
    sender_address=models.CharField(max_length=255)
    receiver_name=models.CharField(max_length=255)
    receiver_address=models.CharField(max_length=255)
    amount=models.CharField(max_length=255)
    transaction_hash=models.CharField(max_length=255)