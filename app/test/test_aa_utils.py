from app.code.aa_xml_flatten_utils import *
import unittest


class TestUtils(unittest.TestCase):
    def test_xml_flattens(self):
        my_xml = '<?xml version="1.0" encoding="ASCII"?> \n \
            <FIXML> \n \
            <PosRpt RptID="541386431" Rslt="0" \n  \
            BizDt="2003-09-10T00:00:00" Acct="1" AcctTyp="1" > \n  \
            <Pty ID="OCC" R="212"/> \n  \
            <Pty ID="99999" R="4"/> \
            <Qty Typ="SOD2" Long="35" Short="0"/> \n  \
            <Qty Typ="FIN" Long="202" Short="10"/> \n  \
            <Qty Typ="IAS" Long="10"/> \n  \
            </PosRpt> \n  \
            </FIXML> \n '

        actual_result = get_flat_list_from_xml_string(my_xml)

        expected_result = [('FIXML_PosRpt_@RptID', '541386431'),
                           ('FIXML_PosRpt_@Rslt', '0'),
                           ('FIXML_PosRpt_@BizDt', '2003-09-10T00:00:00'),
                           ('FIXML_PosRpt_@Acct', '1'),
                           ('FIXML_PosRpt_@AcctTyp', '1'),
                           ('FIXML_PosRpt_Pty_<0>_@ID', 'OCC'),
                           ('FIXML_PosRpt_Pty_<0>_@R', '212'),
                           ('FIXML_PosRpt_Pty_<1>_@ID', '99999'),
                           ('FIXML_PosRpt_Pty_<1>_@R', '4'),
                           ('FIXML_PosRpt_Qty_<0>_@Typ', 'SOD2'),
                           ('FIXML_PosRpt_Qty_<0>_@Long', '35'),
                           ('FIXML_PosRpt_Qty_<0>_@Short', '0'),
                           ('FIXML_PosRpt_Qty_<1>_@Typ', 'FIN'),
                           ('FIXML_PosRpt_Qty_<1>_@Long', '202'),
                           ('FIXML_PosRpt_Qty_<1>_@Short', '10'),
                           ('FIXML_PosRpt_Qty_<2>_@Typ', 'IAS'),
                           ('FIXML_PosRpt_Qty_<2>_@Long', '10')]
        print("actual result = ")
        print(actual_result)

        self.assertEqual(expected_result, actual_result)

if __name__ == '__main__':
    unittest.main()
