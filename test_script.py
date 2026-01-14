#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本，用于验证Python环境是否正常工作
"""

# 打印基本信息
print("=== Python环境测试 ===")
print("Hello, Python!")

# 测试基本计算
print("\n=== 基本计算测试 ===")
a = 10
b = 5
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")

# 测试列表操作
print("\n=== 列表操作测试 ===")
fruits = ["apple", "banana", "cherry"]
print(f"原始列表: {fruits}")
fruits.append("orange")
print(f"添加元素后: {fruits}")
print(f"列表长度: {len(fruits)}")

# 测试函数定义
print("\n=== 函数测试 ===")
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
print(greet("Python"))

# 测试模块导入
print("\n=== 模块导入测试 ===")
import math
print(f"π的值: {math.pi}")
print(f"平方根(16): {math.sqrt(16)}")

print("\n=== 测试完成 ===")
print("Python环境正常工作！")
