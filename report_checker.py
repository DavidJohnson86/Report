"""
This script help to validate test report file in BMW ACSM5 project.
Checks for missing test cases, duplicated test cases.
"""

from pprint import pprint
from lxml import etree


class Report:
    """
    Class used for store PATH. And hard codes index values for the report.
    Static methods receives lxml parser report objects and returns values."""

    REPORT_PATH = r'.\reports'

    @staticmethod
    def test_name(report_obj):
        """returns test_name"""
        return report_obj[7].attrib['val']

    @staticmethod
    def failed_measurements(report_obj):
        """returns number of failed measurements"""
        return int(report_obj[13].attrib['val'])


class Validator:
    """Includes most essential functions to validate test reports"""

    def __init__(self, *reports):
        """
        Initialize arguments

        Args:
            *reports(str): args for report path

        Variables:
            root(list) : contains lxml etree objects:
                [<Element COMPA-REPORT at 0x28d5e90>], [<Element COMPA-REPORT at 0x28d5d78>]]

            test_names(list): contains strings of test case names:
                 [['Rate_Fault_YAW_Normal_no_Quali_OF_R_OK_Rate_St_1_Class2_Qual']]

            failed_tests(list): contains failed testcases,

            report_names(list):  contains the path of the reports
                [['.\\reports\\8_3_1ISC_Sensor_Emulation_Unknown_XmlReport.xml'],
                ['.\\reports\\SW008_003_002_ISC_Sensor_Emulation_Unknown_XmlReport.xml']]
        """
        self.main_report = etree.parse(reports[0]).getroot()
        self.root = [[] for idx in enumerate(reports)]
        self.test_names = [[] for idx in enumerate(reports)]
        self.failed_tests = [[] for idx in enumerate(reports)]
        self.report_names = [[value] for idx, value in enumerate(reports)]
        for idx, value in enumerate(reports):
            tree = etree.parse(value)
            self.root[idx].append(tree.getroot())
        self.test_names = self.get_test_names()
        self.failed_test = self.get_failed_test()
        self.num_test_cases = [len(elem) for elem in self.test_names]
        self.num_failed = [len(elem) for elem in self.failed_test]
        self.repairable = self.get_repaired()
        self.repaired = self.set_right_values([report for report in self.root[1:]], self.root[0], r'd:\\tests.xml')

    def get_test_names(self):
        """
        Get the test names from the report

        Returns:
            test_names(list) : List of test names.
        """
        for report_idx in range(0, len(self.test_names)):
            for report in self.root[report_idx]:
                for elem in report:
                    self.test_names[report_idx].append(Report.test_name(elem))
        return self.test_names

    def get_failed_test(self):
        """
        Get test names of failed testcases

        Returns:
            failed_tests(list): List of failed test names.

        """
        for report_idx in range(0, len(self.failed_tests)):
            for report in self.root[report_idx]:
                for elem in report:
                    if Report.failed_measurements(elem) > 0:
                        self.failed_tests[report_idx].append(Report.test_name(elem))
        return self.failed_tests

    def get_repaired(self):
        """
        Takes the list of Failed Testcases. Iterating through the Number 2 Xml
        and if in Number 2 is passed what is failed in Number 1 Return a list
        with the names of the repairable testcases.

        Args:
            listofFailed(list): list of Failed Testcases

        Returns(list):
            list of Passed Testcases what is failed before
        """
        self.repairable = []
        for lists in self.failed_test:
            self.repairable = set(lists) - set(self.repairable)
        return list(self.repairable)

    def set_right_values(self, rerunned_tests, source_root, output):
        """
        Replace failed tests with the passed ones.

        Args:
            rerunned_tests(list): Rerunned tests
            source_root(lxml object): Tree object of the main report
            output(string): PATH where to save the merged report

        Returns(list):
            Repaired testcases
        """
        counter = 0
        fixed_tests = []
        root = source_root[0]
        rerunned_tests = [report for lists in rerunned_tests for report in lists]
        source_root = [report for lists in source_root for report in lists]
        for source in source_root:
            if Report.test_name(source) in self.repairable:
                for test in rerunned_tests:
                    for destination in test:
                        if Report.test_name(source) == Report.test_name(destination):
                            root.remove(source)
                            root.append(destination)
                            fixed_tests.append(source)
                            counter += 1
                            break
        root.getroottree().write(str(output), xml_declaration=True)
        return fixed_tests

    @staticmethod
    def check_equal(iterator):
        """
        Check if any duplicated or multiplication of elements in a list.

        Args:
            iterator (list): list of iterator

        Returns(list):
            Same elements found in an iterator

        """
        return [x for x in iterator if iterator.count(x) > 1]

    def __repr__(self):
        """Returns a printable format from the object"""
        summary = ""
        for report_idx in range(0, len(self.failed_tests)):
            summary += "\nReport name: {}"\
                "\nTest names: {}" \
                "\nFailed tests: {}"\
                "\nNumber of test cases: {}"\
                "\nNumber of failed test cases: {}"\
                "\nDuplicated test cases: {}" \
                "\nNumber of duplicated test cases: {}".format(self.report_names[report_idx],
                                                               self.test_names[report_idx],
                                                               self.failed_test[report_idx],
                                                               self.num_test_cases[report_idx],
                                                               self.num_failed[report_idx],
                                                               self.check_equal(self.test_names[report_idx]),
                                                               len(self.check_equal(self.test_names[report_idx])))
        summary += "\nRepairable test cases {}" \
                   "\nNumber of repairable test cases {}"\
                   "\n Testing test elements {}".format(self.repairable, len(self.repairable), self.repaired)

        return summary


if __name__ == "__main__":
    FILE1 = Report.REPORT_PATH + '\\' + r"8_3_1ISC_Sensor_Emulation_Unknown_XmlReport.xml"
    FILE2 = Report.REPORT_PATH + '\\' + r"SW008_003_002_ISC_Sensor_Emulation_Unknown_XmlReport.xml"
    CHECK = Validator(FILE1, FILE2)
    pprint(CHECK)
