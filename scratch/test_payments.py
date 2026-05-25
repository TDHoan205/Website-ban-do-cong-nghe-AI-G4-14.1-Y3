import sys
sys.path.append('.')

import unittest
from sqlalchemy.orm import Session
from Data.database import SessionLocal
from Services.PaymentService import PaymentService, BANK_CONFIG
from Controllers.PaymentController import _create_order_from_payment

class TestPayments(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.payment_service = PaymentService(self.db)

    def tearDown(self):
        self.db.close()

    def test_build_qr_url(self):
        url = self.payment_service._build_qr_url(150000, "DH0525TEST")
        print("Generated QR URL:", url)
        self.assertIn("img.vietqr.io/image/mb-0386267692-compact2.png", url)
        self.assertIn("amount=150000", url)
        self.assertIn("addInfo=DH0525TEST", url)
        self.assertIn("accountName=TRAN%20ANH%20QUAN", url)

if __name__ == "__main__":
    unittest.main()
