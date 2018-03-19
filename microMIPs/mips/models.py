from django.db import models

# Create your models here.
class Codes(models.Model):
    address = models.CharField(max_length=10)
    rep = models.CharField(max_length=8)
    label = models.CharField(max_length=30)
    instruction = models.CharField(max_length=40)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.instruction
    class Meta:
        verbose_name_plural = "Codes"

class Opcodetable(models.Model):
    instrc = models.CharField(max_length=10)
    opcode = models.CharField(max_length=6)
    rs = models.CharField(blank=True, max_length=5)
    sa = models.CharField(blank=True, max_length=5)
    func = models.CharField(blank=True, max_length=10)

    def __str__(self):
        return self.instrc

    class Meta:
        verbose_name_plural = "Opcode Table"


class Memory(models.Model):
    address = models.CharField(max_length=4)
    memval = models.CharField(max_length=2,default="00")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "Memory"


class Register(models.Model):
    regval = models.CharField(max_length=16,default="0000000000000000")
    regnum = models.PositiveIntegerField(default=0)
    def __str__(self):
        return "R"+str(self.regnum)
    class Meta:
        verbose_name_plural = "Registers"