import os

from django.db import models

from .status import SelectionStatus


class Selection(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, editable=False)

    status = models.CharField(default=SelectionStatus.PASSED_TEST, null=False, max_length=40)

    draw_rank = models.IntegerField(null=True, default=None)

    payment_value = models.FloatField(null=True, default=None)
    ticket_type = models.CharField(null=True, default=None, max_length=40)
    payment_due_date = models.DateTimeField(null=True, default=None)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


doc_type_choices = [("payment_proof", "Payment Proof"), ("student_id", "Student ID")]


class SelectionDocument(models.Model):
    selection = models.ForeignKey("selection.Selection", on_delete=models.CASCADE, related_name="documents")

    file_location = models.TextField(null=False)

    doc_type = models.CharField(blank=False, null=False, max_length=20, choices=doc_type_choices)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    @property
    def filename(self) -> str:
        return os.path.basename(self.file_location)


class SelectionLogs(models.Model):
    selection = models.ForeignKey("selection.Selection", on_delete=models.CASCADE, related_name="logs", editable=False)

    event = models.CharField(null=False, max_length=40, editable=False)
    message = models.TextField(null=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
