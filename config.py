import numpy as np

image_width = 400
image_height = 400

std_color = np.array([60, 255, 255])
# 路径的颜色范围
lower_color = np.array([50, 50, 50])
upper_color = np.array([70, 255, 255])


# path1的取样点(x, y)
#start_point = (24, 209)
#end_point = (38, 176)
# path2的取样点(x, y)
start_point = (31, 214)
end_point = (130, 132)
# path3的取样点(x, y)
#start_point = (29, 212)
#end_point = (123, 33)
# 路线取样距离
sampling_distance = 3

# 计算切线的方框大小(奇数)
tangent_size = 5
# 切线的绘制长度
tangent_length = 100