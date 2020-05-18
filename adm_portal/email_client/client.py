from abc import ABC, abstractmethod
from typing import Optional


class EmailClient(ABC):
    # account
    @abstractmethod
    def send_signup_email(self, to: str, *, email_confirmation_url: str) -> None:
        pass

    @abstractmethod
    def send_reset_password_email(self, to: str, *, reset_password_url: str) -> None:
        pass

    # payments
    @abstractmethod
    def send_payment_accepted_proof_email(self, to: str, *, message: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def send_payment_need_additional_proof_email(self, to: str, *, message: str) -> None:
        pass

    @abstractmethod
    def send_payment_refused_proof_email(self, to: str, *, message: str) -> None:
        pass

    # bulk emails
    # application is over
    def send_application_is_over_passed(self, to: str) -> None:
        pass

    def send_application_is_over_failed(self, to: str) -> None:
        pass

    # admissions are over
    def send_admissions_are_over_not_selected(self, to: str) -> None:
        pass
