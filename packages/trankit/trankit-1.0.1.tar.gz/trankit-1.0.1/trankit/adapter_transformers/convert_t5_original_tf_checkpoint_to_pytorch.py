# coding=utf-8
# Copyright 2018 The T5 authors and HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Convert T5 checkpoint."""


import argparse
import logging

import torch

from transformers import T5Config, T5Model, load_tf_weights_in_t5


logging.basicConfig(level=logging.INFO)


def convert_tf_checkpoint_to_pytorch(tf_checkpoint_path, config_file, pytorch_dump_path):
    # Initialise PyTorch model
    config = T5Config.from_json_file(config_file)
    print("Building PyTorch model from configuration: {}".format(str(config)))
    model = T5Model(config)

    # Load weights from tf checkpoint
    load_tf_weights_in_t5(model, config, tf_checkpoint_path)

    # Save pytorch-model
    print("Save PyTorch model to {}".format(pytorch_dump_path))
    torch.save(model.state_dict(), pytorch_dump_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--tf_checkpoint_path", default=None, type=str, required=True, help="Path to the TensorFlow checkpoint path."
    )
    parser.add_argument(
        "--config_file",
        default=None,
        type=str,
        required=True,
        help="The config json file corresponding to the pre-trained T5 model. \n"
        "This specifies the model architecture.",
    )
    parser.add_argument(
        "--pytorch_dump_path", default=None, type=str, required=True, help="Path to the output PyTorch model."
    )
    args = parser.parse_args()
    convert_tf_checkpoint_to_pytorch(args.tf_checkpoint_path, args.config_file, args.pytorch_dump_path)
