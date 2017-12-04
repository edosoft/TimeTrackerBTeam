import unittest
from datetime import datetime, date
from models import Workday
from tasks import automatic_checkout_helper


class TasksTestCase(unittest.TestCase):

    def test_auto_checkout(self):
        fake_date = datetime.now()
        fake_work = Workday(employeeid="prueba", date=fake_date,
                            checkin=fake_date, checkout=None, total=0)
        fake_work.put()
        automatic_checkout_helper()

        queryWorkday = Workday.query(Workday.date == date.today(),
                                     Workday.employeeid == "prueba").get()

        self.assertFalse(queryWorkday.checkout, None, "checkout not closed")


if __name__ == '__main__':
    unittest.main()
