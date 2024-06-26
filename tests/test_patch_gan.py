# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import unittest

import torch
from monai.networks import eval_mode
from parameterized import parameterized

from generative.networks.nets.patchgan_discriminator import MultiScalePatchDiscriminator
from tests.utils import test_script_save

TEST_2D = [
    {
        "num_d": 2,
        "num_layers_d": 3,
        "spatial_dims": 2,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    },
    torch.rand([1, 3, 256, 512]),
    [(1, 1, 32, 64), (1, 1, 4, 8)],
    [4, 7],
]
TEST_3D = [
    {
        "num_d": 2,
        "num_layers_d": 3,
        "spatial_dims": 3,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    },
    torch.rand([1, 3, 256, 512, 256]),
    [(1, 1, 32, 64, 32), (1, 1, 4, 8, 4)],
    [4, 7],
]
TEST_3D_POOL = [
{
        "num_d": 2,
        "num_layers_d": 3,
        "spatial_dims": 3,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "pooling_method": "max",
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    },
    torch.rand([1, 3, 256, 512, 256]),
    [(1, 1, 32, 64, 32), (1, 1, 16, 32, 16)],
    [4, 4],
]
TEST_2D_POOL = [
    {
        "num_d": 4,
        "num_layers_d": 3,
        "spatial_dims": 2,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "pooling_method": "avg",
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    },
    torch.rand([1, 3, 256, 512]),
    [(1, 1, 32, 64), (1, 1, 16, 32), (1, 1, 8, 16), (1, 1, 4, 8)],
    [4, 4, 4, 4],
]
TEST_LAYER_LIST = [
    {
        "num_d": 3,
        "num_layers_d": [3,4,5],
        "spatial_dims": 2,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    },
    torch.rand([1, 3, 256, 512]),
    [(1, 1, 32, 64), (1, 1, 16, 32), (1, 1, 8, 16)],
    [4, 5, 6],
]
TEST_TOO_SMALL_SIZE = [
    {
        "num_d": 2,
        "num_layers_d": 6,
        "spatial_dims": 2,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    }
]
TEST_MISMATCHED_NUM_LAYERS = [
    {
        "num_d": 5,
        "num_layers_d": [3,4,5],
        "spatial_dims": 2,
        "num_channels": 8,
        "in_channels": 3,
        "out_channels": 1,
        "kernel_size": 3,
        "activation": "LEAKYRELU",
        "norm": "instance",
        "bias": False,
        "dropout": 0.1,
        "minimum_size_im": 256,
    }
]

CASES = [TEST_2D, TEST_3D, TEST_3D_POOL, TEST_2D_POOL, TEST_LAYER_LIST]

class TestPatchGAN(unittest.TestCase):
    @parameterized.expand(CASES)
    def test_shape(self, input_param, input_data, expected_shape, features_lengths=None):
        net = MultiScalePatchDiscriminator(**input_param)
        with eval_mode(net):
            result, features = net.forward(input_data)
            for r_ind, r in enumerate(result):
                self.assertEqual(tuple(r.shape), expected_shape[r_ind])
            for o_d_ind, o_d in enumerate(features):
                self.assertEqual(len(o_d), features_lengths[o_d_ind])

    def test_too_small_shape(self):
        with self.assertRaises(AssertionError):
            MultiScalePatchDiscriminator(**TEST_TOO_SMALL_SIZE[0])

    def test_mismatched_num_layers(self):
        with self.assertRaises(AssertionError):
            MultiScalePatchDiscriminator(**TEST_MISMATCHED_NUM_LAYERS[0])

    def test_script(self):
        net = MultiScalePatchDiscriminator(
            num_d=2,
            num_layers_d=3,
            spatial_dims=2,
            num_channels=8,
            in_channels=3,
            out_channels=1,
            kernel_size=3,
            activation="LEAKYRELU",
            norm="instance",
            bias=False,
            dropout=0.1,
            minimum_size_im=256,
        )
        i = torch.rand([1, 3, 256, 512])
        test_script_save(net, i)


if __name__ == "__main__":
    unittest.main()
