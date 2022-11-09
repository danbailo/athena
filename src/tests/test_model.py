from unittest import TestCase


from database.models.base import AtenaBase


class TestModel(TestCase):

    def test_wrong_model_name(self):
        with self.assertRaises(ValueError):
            class ErrorMaodel(AtenaBase):
                pass

    def test_correct_model_name(self):
        class ErrorModel(AtenaBase):
            pass
