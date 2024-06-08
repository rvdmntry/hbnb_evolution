import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    def setUp(self):
        self.review = Review(
            user_id="user123", place_id="place123", rating=5, comment="Great place!")

    def test_instance(self):
        self.assertIsInstance(self.review, Review)

    def test_attributes(self):
        self.assertEqual(self.review.user_id, "user123")
        self.assertEqual(self.review.place_id, "place123")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Great place!")

    def test_to_dict(self):
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict["user_id"], "user123")
        self.assertEqual(review_dict["place_id"], "place123")
        self.assertEqual(review_dict["__class__"], "Review")


if __name__ == '__main__':
    unittest.main()
