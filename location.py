import time
import sys

# ========= 参数 =========
m = 1.0           # 质量
g = 10           # 重力加速度
f = 50.0          # 瞬时力大小
s = 0.05          # 力作用时间（很短）
dt = 0.03         # 30 ms ≈ 30 FPS

# ========= 状态 =========
y = 0.0           # 位置
v = 0.0           # 速度
running = True

# ========= 输入检测 =========
def space_pressed():
    try:
        import msvcrt  # Windows
        if msvcrt.kbhit():
            key = msvcrt.getch()
            return key == b' '
    except ImportError:
        pass
    return False

print("开始模拟，按【空格】施加向上瞬时力，Ctrl+C 退出")

# ========= 主循环 =========
while running:
    # --- 输入 ---
    if space_pressed():
        dv = (f * s) / m
        v += dv
        print(">>> 施加瞬时力")

    # --- 物理更新 ---
    v -= g * dt
    y += v * dt

    # --- 地面碰撞 ---
    if y <= 0:
        y = 0
        v = 0

    # --- 输出 ---
    print(f"y = {y:.4f} m, v = {v:.4f} m/s")

    time.sleep(dt)
