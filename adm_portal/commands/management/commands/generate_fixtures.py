import logging
import os
import random
from datetime import datetime
from typing import Dict

from django.core.management.base import BaseCommand

from applications.models import Application, Submission, SubmissionTypes
from payments.models import Document, Payment
from profiles.models import Profile, gender_choices, ticket_types_choices
from users.models import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Command(BaseCommand):
    help = "Generates Fixtures for tests"

    def _user(self, uid: str) -> User:
        logger.info(f"creating user with uid: {uid}")
        return User.objects.create_user(email=f"{uid}@adm.com", password=uid)

    @staticmethod
    def summary() -> Dict[str, int]:
        return {
            "users": User.objects.count(),
            "profiles": Profile.objects.count(),
            "applications": Application.objects.count(),
        }

    def handle(self, *args, **options) -> None:
        # staff user
        User.objects.create_staff_user(email="staff@adm.com", password="staff")

        # user with nothing
        self._user("nothing")

        # user with profiles
        Profile.objects.create(
            user=self._user("profile_student"),
            full_name="User With Student Profile",
            profession="Student",
            gender="f",
            ticket_type="student",
        )
        Profile.objects.create(
            user=self._user("profile_regular"),
            full_name="User With Regular Profile",
            profession="Worker",
            gender="m",
            ticket_type="regular",
        )
        Profile.objects.create(
            user=self._user("profile_company"),
            full_name="User With Company Profile",
            profession="Spotify",
            gender="other",
            ticket_type="company",
        )

        # users with applications
        a0 = Application.objects.create(user=self._user("application_success"), coding_test_started_at=datetime.now())
        Submission.objects.create(
            application=a0,
            submission_type=SubmissionTypes.coding_test.uname,
            score=85,
            feedback_location=_feedback_location,
        )
        Submission.objects.create(
            application=a0, submission_type=SubmissionTypes.slu01.uname, score=91, feedback_location=_feedback_location
        )
        Submission.objects.create(
            application=a0, submission_type=SubmissionTypes.slu02.uname, score=82, feedback_location=_feedback_location
        )
        Submission.objects.create(
            application=a0, submission_type=SubmissionTypes.slu03.uname, score=75, feedback_location=_feedback_location
        )

        a1 = Application.objects.create(user=self._user("application_failed"), coding_test_started_at=datetime.now())
        Submission.objects.create(
            application=a1,
            submission_type=SubmissionTypes.coding_test.uname,
            score=40,
            feedback_location=_feedback_location,
        )

        Application.objects.create(
            user=self._user("application_failed_no_coding_test"), coding_test_started_at=datetime.now()
        )

        # users with payments
        prof0 = Profile.objects.create(
            user=self._user("user_with_docs"), name="User With Pay docs", ticket_type="student", gender="f"
        )
        pay0 = Payment.objects.create(
            user=prof0.user, value=500, currency="£", due_date=datetime.now(), status="pending_verification"
        )
        Document.objects.create(payment=pay0, file_location=_payment_proof_location, doc_type="payment_proof")
        Document.objects.create(payment=pay0, file_location=_student_id_proof_location, doc_type="student_id")

        prof1 = Profile.objects.create(
            user=self._user("user_without_docs"), name="User Without Pay docs", ticket_type="company", gender="m"
        )
        Payment.objects.create(user=prof1.user, value=1500, currency="£", due_date=datetime.now())

        # randoms
        for i in range(0, 50):
            u = self._user(f"random_{i}")
            gender = random.choice(gender_choices)[0]
            ticket_type = random.choice(ticket_types_choices)[0]
            Profile.objects.create(
                user=u,
                full_name=f"Random User {i}",
                profession=f"Random Profession {i}",
                gender=gender,
                ticket_type=ticket_type,
            )

            a = Application.objects.create(user=u, coding_test_started_at=datetime.now())
            for j in range(0, 15):
                s_type = random.choice(
                    [
                        SubmissionTypes.coding_test.uname,
                        SubmissionTypes.slu01.uname,
                        SubmissionTypes.slu02.uname,
                        SubmissionTypes.slu03.uname,
                    ]
                )
                score = random.randrange(60, 100, 2)
                Submission.objects.create(
                    application=a, submission_type=s_type, score=score, feedback_location=_feedback_location
                )

        logger.info(self.summary())


_namespace = "fixtures/"
_feedback_location = os.path.join(_namespace, "submission_feedback.html")
_payment_proof_location = os.path.join(_namespace, "payment_proof.jpg")
_student_id_proof_location = os.path.join(_namespace, "student_id_proof.png")
