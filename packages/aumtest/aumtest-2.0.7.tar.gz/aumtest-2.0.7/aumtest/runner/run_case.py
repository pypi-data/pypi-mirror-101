# coding:utf-8
'''
@File    : run_case.py
@Author  : TM_QA
'''

from aumtest.common import Var
from aumtest.runner.test_case import TestCase
from aumtest.drivers.driver_base_app import DriverBaseApp
from aumtest.drivers.driver_base_web import DriverBaseWeb
from aumtest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if self.skip:
            self.skipTest('skip')
        if Var.re_start:
            if Var.driver != 'selenium':
                DriverBaseApp.launch_app(None)
            else:
                DriverBaseWeb.createSession()

    def testCase(self):
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.re_start:
            try:
                if Var.driver != 'selenium':
                    DriverBaseApp.close_app(None)
                else:
                    DriverBaseWeb.quit()
            except:
                pass