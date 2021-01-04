import numpy as np

image_width = 400
image_height = 400

std_color = np.array([60, 255, 255])
# 路径的颜色范围
lower_color = np.array([50, 50, 50])
upper_color = np.array([70, 255, 255])

# path1的第一个取样点(x, y)
head_point = (30, 213)
# 路线取样距离
sampling_distance = 5

# 计算切线的方框大小(奇数)
tangent_size = 5
# 切线的绘制长度
tangent_length = 100