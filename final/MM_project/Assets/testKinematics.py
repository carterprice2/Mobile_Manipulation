#!/usr/bin/env python
"""testKinematics.py
Tests the inverse kinematics and jacobian of the robot

@author Gerry and Carter
"""

import unittest
import numpy as np
import Kinematics

class TestKinematics(unittest.TestCase):
    """Unit tests for robot kinematics"""

    def test_ik_arm(self):
        LINK_LENGTHS = [0, 1, 1, 1]
        Q0 = [0, 0, 0, 0, 0, 0, 0]
        x = [0, 0, 3]
        theta = 0
        phi = 0

        q_expected = [180, 90, 0, 0]
        np.testing.assert_array_almost_equal(Kinematics.ik_arm(x, theta, phi, LINK_LENGTHS, Q0),
                                             q_expected)

        theta = 75
        q_expected = [theta-180, 90, 0, 0]
        np.testing.assert_array_almost_equal(Kinematics.ik_arm(x, theta, phi, LINK_LENGTHS, Q0),
                                             q_expected)

        x = [0, 0, 2]
        q_expected = [theta-180, 30, 120, -60]
        np.testing.assert_array_almost_equal(Kinematics.ik_arm(x, theta, phi, LINK_LENGTHS, Q0),
                                             q_expected)
    
    def test_ik(self):
        LINK_LENGTHS = [0, 1, 1, 1]
        BO = [0, 0, 1]
        Q0 = [0, 0, 0, 0, 0, 0, 0]

        x = [0, 0, 3]
        theta = 0
        phi = 0
        q_expected = [0, 0, 0, 180, 30, 120, -60]
        np.testing.assert_array_almost_equal(Kinematics.ik(x, theta, phi, LINK_LENGTHS, BO, Q0),
                                             q_expected)

        x = [0, 1, 3]
        q_expected = [0, 1, 0, 180, 30, 120, -60]
        np.testing.assert_array_almost_equal(Kinematics.ik(x, theta, phi, LINK_LENGTHS, BO, Q0),
                                             q_expected)

        x = [-1, 0, 3]
        q_expected = [0, 0, 0, 180, 0, 90, 0]
        np.testing.assert_array_almost_equal(Kinematics.ik(x, theta, phi, LINK_LENGTHS, BO, Q0),
                                             q_expected)

        theta = 30
        x = [-0.8660254038, -0.5, 3]
        q_expected = [0, 0, 0, -150, 0, 90, 0]
        np.testing.assert_array_almost_equal(Kinematics.ik(x, theta, phi, LINK_LENGTHS, BO, Q0),
                                             q_expected)

    # def test_jacobian(self):
    #     LINK_LENGTHS = [0, 1, 1, 1]
    #     BO = [0, 0, 1]
    #     Q0 = [0, 0, 0, 0, 0, 0, 0]

    #     q = [0, 0, 0, 0, 0, 0, 0]
    #     J_expected = np.array([[1, 0, 0, 0, 0, 0, 0],
    #                            [1, 0, 0, 0, 0, 0, 0],
    #                            [1, 0, 0, 0, 0, 0, 0],
    #                            [1, 0, 0, 0, 0, 0, 0],
    #                            [1, 0, 0, 0, 0, 0, 0],
    #                            [1, 0, 0, 0, 0, 0, 0]];

if __name__ == '__main__':
    unittest.main()