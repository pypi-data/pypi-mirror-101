# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
# Imports
#
import base64, binascii


#
# Classes
#

# Wrapper for utility functions
class Utils:
    # Decode data to specified encoding
    @staticmethod
    def Decode(data, encoding = "utf-8"):
        if isinstance(data, str):
            return data
        elif isinstance(data, bytes):
            return data.decode(encoding)
        else:
            raise RuntimeError("Invalid data type")

    # Encode data to specified encoding
    @staticmethod
    def Encode(data, encoding = "utf-8"):
        if isinstance(data, str):
            return data.encode(encoding)
        elif isinstance(data, bytes):
            return data
        else:
            raise RuntimeError("Invalid data type")

    # Base64 decode
    @staticmethod
    def Base64Decode(data):
        return base64.b64decode(data)

    # Base64 encode
    @staticmethod
    def Base64Encode(data):
        return Utils.Decode(base64.b64encode(Utils.Encode(data)))

    # Check if base64
    @staticmethod
    def IsBase64(data):
        try:
            base64.b64decode(data, validate=True)
            res = True
        except binascii.Error:
            res = False

        return res
