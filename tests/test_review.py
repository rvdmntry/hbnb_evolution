import unittest
from models.review import Review
from models.user import User
from models.place import Place


class TestReview(unittest.TestCase):
    def test_create_review(self):
        user = User(email="reviewer@example.com",
                    password="password", first_name="John", last_name="Doe")
        place = Place(name="Nice Apartment", description="A beautiful apartment", address="456 Elm St", city=None,
                      latitude=34.0522, longitude=-118.2437, host=None, number_of_rooms=2, bathrooms=1, price_per_night=100, max_guests=3)
        review = Review(user=user, place=place, rating=5,
                        comment="Amazing place!")
        self.assertIsNotNone(review.id)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Amazing place!")


if __name__ == '__main__':
    unittest.main()
