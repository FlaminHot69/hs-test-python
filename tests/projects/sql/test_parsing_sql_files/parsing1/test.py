from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'test': None
    }

    @dynamic_test()
    def test_queries_exist(self):
        for query in self.queries:
            if self.queries[query] is None:
                return wrong(f"Can't find '{query}' query from SQL files!")
        return correct()

    @dynamic_test()
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
