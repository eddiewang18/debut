from django.db import models

# Create your models here.
class Machine(models.Model):
    machine_id = models.AutoField(primary_key=True,db_column="machine_id")
    machine_name = models.CharField(max_length = 30, db_column='machine_name',unique=True)
    connecting_plate = models.IntegerField(db_column='connecting_plate',null=False,blank=False)
    machine_amt = models.IntegerField(db_column='machine_amt',null=False,blank=False)
    cdatetime = models.DateTimeField(db_column='cdatetime', auto_now=False, auto_now_add=True)
    mdatetime = models.DateTimeField(db_column='mdatetime', auto_now=True, auto_now_add=False)
    
    class Meta :
        db_table = "machine"

class Machine_line(models.Model):
    machine_line_id = models.AutoField(primary_key=True,db_column="machine_line_id")
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE,to_field='machine_id',db_column='machine_id',related_name='lines')
    machine_line_name = models.CharField(max_length = 30, db_column='machine_line_name')
    emp_default_amt = models.IntegerField(db_column='emp_default_amt',null=False,blank=False)
    cdatetime = models.DateTimeField(db_column='cdatetime', auto_now=False, auto_now_add=True)
    mdatetime = models.DateTimeField(db_column='mdatetime', auto_now=True, auto_now_add=False)

    class Meta :
        db_table = "machine_line"

class Machine_line_record(models.Model):
    record_id = models.AutoField(primary_key=True,db_column="record_id")
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE,to_field='machine_id',db_column='machine_id')
    machine_line_id = models.ForeignKey(Machine_line, on_delete=models.CASCADE,to_field='machine_line_id',db_column='machine_line_id')
    production_day = models.DateField(db_column='production_day',null=True,blank=True)
    machine_line_amt = models.IntegerField(db_column='machine_line_amt',null=True,blank=True)
    emp_amt = models.IntegerField(db_column='emp_amt',null=True,blank=True)
    work_hours = models.IntegerField(db_column='work_hours',null=True,blank=True)
    overhead_wire = models.CharField(db_column='overhead_wire', max_length=2,null=True,blank=True)
    ng = models.CharField(db_column='ng', max_length=200,null=True,blank=True)
    cdatetime = models.DateTimeField(db_column='cdatetime', auto_now=False, auto_now_add=True)
    mdatetime = models.DateTimeField(db_column='mdatetime', auto_now=True, auto_now_add=False)

    class Meta :
        db_table = "machine_line_record"