import unittest

from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'test': None
    }

    @dynamic_test
    def test_queries(self):

        expected_queries = {
            'create_table': "CREATE TABLE STUDENT( ID INT PRIMARY KEY NOT NULL, NAME CHAR(20) NOT NULL,"
                            " ROLL CHAR(20), ADDRESS CHAR(50), CLASS CHAR(20) )",
            'test': "UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1"
        }

        for query in self.queries:
            if self.queries[query] != expected_queries[query]:
                return wrong(f"'{query}' is wrong! \n Expected:\n {expected_queries[query]}\n"
                             f"Found:\n{self.queries[query]}")
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSQLProject().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
