from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Password must be at least %d characters long.") % self.min_length,
                code='password_too_short'
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least one numeric character."),
                code='password_no_numeric'
            )

        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least one capital letter."),
                code='password_no_uppercase'
            )

    def get_help_text(self):
        return _(
            "Password must be at least %d characters long and contain at least "
            "one numeric character and one capital letter."
        ) % self.min_length
