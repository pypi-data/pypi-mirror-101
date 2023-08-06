'''
Description: 
version: 
Author: TianyuYuan
Date: 2021-04-06 22:43:32
LastEditors: TianyuYuan
LastEditTime: 2021-04-06 22:45:06
'''
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="clearbmk",
  version="0.0.1",
  author="tyyuan",
  author_email="1374736649@qq.com",
  description="清理数据集工具箱",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/paperplane110/clearbmk",
  packages=setuptools.find_packages(),
  install_requires=[],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)