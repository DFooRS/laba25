#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import ind_tests


prodTestSuite = unittest.TestSuite()
prodTestSuite.addTest(unittest.makeSuite(ind_tests.ProdTest))
runner = unittest.TextTestRunner(verbosity=2)
runner.run(prodTestSuite)

