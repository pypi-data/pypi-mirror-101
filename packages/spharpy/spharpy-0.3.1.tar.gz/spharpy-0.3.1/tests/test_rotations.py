""" Tests for sh rotations"""

import pytest
import numpy as np
import spharpy.transforms as transforms
from spharpy.spherical import spherical_harmonic_basis
from spharpy.samplings import Coordinates
import spharpy.spherical as spherical
import spharpy


def test_rotation_matrix_z_axis_complex():
    rot_angle = np.pi/2
    n_max = 2
    reference = np.diag([1, 1j, 1, -1j, -1, 1j, 1, -1j, -1])

    rot_mat = transforms.rotation_z_axis(n_max, rot_angle)
    np.testing.assert_almost_equal(rot_mat, reference)

    rot_angle = np.pi
    reference = np.diag([1, -1, 1, -1, 1, -1, 1, -1, 1])

    rot_mat = transforms.rotation_z_axis(n_max, rot_angle)
    np.testing.assert_almost_equal(rot_mat, reference)

    rot_angle = 3/2*np.pi
    reference = np.diag([1, -1j, 1, 1j, -1, -1j, 1, 1j, -1])

    rot_mat = transforms.rotation_z_axis(n_max, rot_angle)
    np.testing.assert_almost_equal(rot_mat, reference)


def test_rotation_sh_basis_z_axis_complex():
    rot_angle = np.pi/2
    n_max = 2
    theta = np.asarray(np.pi/2)[np.newaxis]
    phi_x = np.asarray(0.0)[np.newaxis]
    phi_y = np.asarray(np.pi/2)[np.newaxis]
    coords_x = Coordinates(1, 0, 0)
    coords_y = Coordinates(0, -1, 0)
    reference = spherical_harmonic_basis(n_max, coords_x).T.conj()

    rot_mat = transforms.rotation_z_axis(n_max, rot_angle)
    sh_vec_x = spherical_harmonic_basis(n_max, coords_y)
    sh_vec_rotated = rot_mat @ sh_vec_x.T.conj()

    np.testing.assert_almost_equal(sh_vec_rotated, reference)


def test_rotation_maxtrix_z_axis_real():
    n_max = 2
    rot_angle = np.pi/4
    reference = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, np.cos(rot_angle), 0, np.sin(rot_angle), 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, -np.sin(rot_angle), 0, np.cos(rot_angle), 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, np.cos(2*rot_angle), 0, 0, 0, np.sin(2*rot_angle)],
                          [0, 0, 0, 0, 0, np.cos(rot_angle), 0, np.sin(rot_angle), 0],
                          [0, 0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, -np.sin(rot_angle), 0, np.cos(rot_angle), 0],
                          [0, 0, 0, 0, -np.sin(2*rot_angle), 0, 0, 0, np.cos(2*rot_angle)]])
    rot_matrix = transforms.rotation_z_axis_real(n_max, rot_angle)
    np.testing.assert_allclose(rot_matrix, reference)


def test_rotation_sh_basis_z_axis_real():
    rot_angle = np.pi/2
    n_max = 2
    coords_x = Coordinates(1, 0, 0)
    coords_y = Coordinates(0, -1, 0)
    reference = np.squeeze(spharpy.spherical.spherical_harmonic_basis_real(n_max, coords_x))

    rot_mat = spharpy.transforms.rotation_z_axis_real(n_max, rot_angle)
    sh_vec_x = spharpy.spherical.spherical_harmonic_basis_real(n_max, coords_y)
    sh_vec_rotated = np.squeeze(rot_mat @ sh_vec_x.T)

    np.testing.assert_almost_equal(sh_vec_rotated, reference)
