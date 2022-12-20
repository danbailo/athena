from unittest import TestCase


from api.database.models.base import AthenaBase


class TestModel(TestCase):

    def test_wrong_model_name(self):
        with self.assertRaises(ValueError):
            class ErrorMaodel(AthenaBase):
                pass

    def test_correct_model_name(self):
        class ErrorModel(AthenaBase):
            pass
