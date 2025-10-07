# # with open("/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt", "rb") as f:
# #     content = f.read(1000)  # 读取前1000字节
# #     print(content)



# # file_path = '/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt'

# # with open(file_path, 'rb') as file:  # 以二进制模式读取文件
# #     for _ in range(5):  # 打印前 5 行数据的字节内容
# #         print(file.readline())



# # import laspy
# # import numpy as np
# # import re

# # # 文件路径
# # input_txt_path = '/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt'
# # output_las_path = '/home/xcl/Cloud Points/converted_file.las'

# # # 读取文件以二进制模式打开
# # points = []
# # with open(input_txt_path, 'rb') as file:  # 二进制模式读取文件
# #     while True:
# #         line = file.readline()
# #         if not line:
# #             break
# #         try:
# #             # 尝试解码为字符串并拆分
# #             decoded_line = line.decode('utf-8')  # 使用utf-8解码
# #             print(f"Decoded line: {decoded_line}")  # 调试输出：查看每一行的内容
            
# #             parts = decoded_line.strip().split()

# #             # 确保该行包含3个数字，并且这些数字能转换为浮点数
# #             if len(parts) == 3:
# #                 # 使用正则表达式检查每部分是否为数字
# #                 if re.match(r'^-?\d+(\.\d+)?$', parts[0]) and re.match(r'^-?\d+(\.\d+)?$', parts[1]) and re.match(r'^-?\d+(\.\d+)?$', parts[2]):
# #                     points.append([float(parts[0]), float(parts[1]), float(parts[2])])
# #                 else:
# #                     print(f"Invalid data in line: {decoded_line}")  # 打印无效的数据行
# #         except UnicodeDecodeError:
# #             # 忽略无法解码的字节，继续读取
# #             pass

# # # 将数据转化为 NumPy 数组
# # if points:
# #     points = np.array(points)

# #     # 使用 laspy 创建 .las 文件
# #     las = laspy.create(point_format=3, file_version="1.2")  # 设置点格式和版本
# #     las.x = points[:, 0]
# #     las.y = points[:, 1]
# #     las.z = points[:, 2]

# #     # 保存为 .las 文件
# #     las.write(output_las_path)

# #     print(f"File has been converted to LAS format and saved to {output_las_path}")
# # else:
# #     print("No valid points found in the file.")


# # import open3d as o3d
# # import numpy as np

# # # 读取TXT文件
# # points = np.loadtxt("/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt")

# # # 创建Open3D点云对象
# # pcd = o3d.geometry.PointCloud()
# # pcd.points = o3d.utility.Vector3dVector(points)

# # # 保存为PLY文件
# # o3d.io.write_point_cloud("bunny_from_txt.ply", pcd)
# # print("bunny_from_txt.ply created successfully.")


# # import struct
# # import laspy
# # import numpy as np

# # # === 根据您的分析结果修改以下参数 ===
# # filename = "/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt"
# # HEADER_SIZE = 120  # 假设头文件大小为120字节
# # POINT_RECORD_SIZE = 32  # 假设每个点占32字节，您需要计算并修改它！
# # POINT_FORMAT = '<'  # 字节序：'<' 为小端 (Windows, Intel常用)；'>' 为大端
# # # 定义数据解包格式字符串：
# # # 例如：'3fI' 表示 3个float (4*3=12字节) + 1个unsigned int (4字节) -> 总共16字节
# # # 例如：'3dH' 表示 3个double (8*3=24字节) + 1个unsigned short (2字节) -> 总共26字节，需要补齐或还有其他字段
# # # 您需要根据 POINT_RECORD_SIZE 和数据分析来确定这个字符串！
# # UNPACK_STR = POINT_FORMAT + '3f I'  # 这是一个示例：小端，3个float（坐标），1个unsigned int（强度）

# # # ===================================

# # # 读取文件
# # with open(filename, 'rb') as f:
# #     data = f.read()

# # # 跳过文件头，获取纯点数据
# # point_data = data[HEADER_SIZE:]

# # # 计算实际点数
# # num_points = len(point_data) // POINT_RECORD_SIZE
# # print(f"文件总大小: {len(data)} 字节")
# # print(f"跳过 {HEADER_SIZE} 字节头文件后，点数据部分为 {len(point_data)} 字节")
# # print(f"假设每个点占 {POINT_RECORD_SIZE} 字节，计算得到点数: {num_points}")

# # # 创建数组来存储点数据
# # all_points = []
# # all_intensities = []

# # # 解析每一个点
# # for i in range(num_points):
# #     start = i * POINT_RECORD_SIZE
# #     end = start + POINT_RECORD_SIZE
# #     point_bytes = point_data[start:end]
    
# #     try:
# #         # 解包核心操作
# #         unpacked_data = struct.unpack(UNPACK_STR, point_bytes[:struct.calcsize(UNPACK_STR)])
# #         # 假设前三个值是X,Y,Z
# #         x, y, z = unpacked_data[0:3]
# #         # 假设第四个值是强度
# #         intensity = unpacked_data[3]
        
# #         all_points.append([x, y, z])
# #         all_intensities.append(intensity)
# #     except struct.error as e:
# #         print(f"Error unpacking point {i} at offset {start}: {e}")
# #         print(f"Bytes: {point_bytes.hex()}")
# #         break

# # # 转换为numpy数组
# # points_array = np.array(all_points)
# # intensities_array = np.array(all_intensities)

# # # 创建并写入LAS文件
# # las = laspy.create(point_format=2)  # 选择点格式，2支持强度值
# # # 设置偏移和缩放因子（非常重要，否则坐标值可能溢出）
# # las.header.offsets = np.min(points_array, axis=0)
# # las.header.scales = [0.001, 0.001, 0.001]  # 精细度到毫米

# # las.x = points_array[:, 0]
# # las.y = points_array[:, 1]
# # las.z = points_array[:, 2]
# # las.intensity = intensities_array

# # output_filename = filename.split('.')[0] + ".las"
# # las.write(output_filename)
# # print(f"转换成功！共转换 {len(all_points)} 个点。文件已保存为: {output_filename}")





# # import struct
# # import laspy
# # import numpy as np

# # # 参数设置
# # filename = "/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt"
# # HEADER_SIZE = 120
# # POINT_RECORD_SIZE = 32
# # POINT_FORMAT = '<'
# # UNPACK_STR = POINT_FORMAT + '3f I'  # 3个float + 1个unsigned int

# # # 读取文件
# # with open(filename, 'rb') as f:
# #     data = f.read()

# # # 跳过文件头，获取纯点数据
# # point_data = data[HEADER_SIZE:]

# # # 计算实际点数
# # num_points = len(point_data) // POINT_RECORD_SIZE
# # print(f"文件总大小: {len(data)} 字节")
# # print(f"跳过 {HEADER_SIZE} 字节头文件后，点数据部分为 {len(point_data)} 字节")
# # print(f"假设每个点占 {POINT_RECORD_SIZE} 字节，计算得到点数: {num_points}")

# # # 创建数组来存储点数据
# # all_points = []
# # all_intensities = []

# # # 解析每一个点
# # for i in range(num_points):
# #     start = i * POINT_RECORD_SIZE
# #     end = start + POINT_RECORD_SIZE
# #     point_bytes = point_data[start:end]
    
# #     try:
# #         # 解包核心操作
# #         unpacked_data = struct.unpack(UNPACK_STR, point_bytes[:struct.calcsize(UNPACK_STR)])
# #         # 假设前三个值是X,Y,Z
# #         x, y, z = unpacked_data[0:3]
# #         # 假设第四个值是强度
# #         intensity = unpacked_data[3]
        
# #         all_points.append([x, y, z])
# #         all_intensities.append(intensity)
# #     except struct.error as e:
# #         print(f"Error unpacking point {i} at offset {start}: {e}")
# #         print(f"Bytes: {point_bytes.hex()}")
# #         break

# # # 转换为numpy数组
# # points_array = np.array(all_points)
# # intensities_array = np.array(all_intensities)

# # # 数据清理
# # print(f"原始点数: {len(points_array)}")
# # valid_mask = np.all(np.isfinite(points_array), axis=1)
# # points_array = points_array[valid_mask]
# # intensities_array = intensities_array[valid_mask]
# # print(f"移除无效值后点数: {len(points_array)}")

# # # 限制强度值在合理范围内
# # intensities_array = np.clip(intensities_array, 0, 65535).astype(np.uint16)

# # # 创建并写入LAS文件
# # las = laspy.create(point_format=2)  # 选择点格式，2支持强度值

# # # 设置偏移和缩放因子
# # las.header.offsets = np.min(points_array, axis=0)
# # las.header.scales = [0.0001, 0.0001, 0.0001]  # 更精细的精度

# # las.x = points_array[:, 0]
# # las.y = points_array[:, 1]
# # las.z = points_array[:, 2]
# # las.intensity = intensities_array

# # output_filename = filename.split('.')[0] + "_optimized.las"
# # las.write(output_filename)
# # print(f"转换成功！共转换 {len(points_array)} 个点。文件已保存为: {output_filename}")



# # 可行
# # import struct
# # import laspy
# # import numpy as np

# # # 参数设置
# # filename = "/home/xcl/Cloud Points/_2025_08_07_17_31_42_841 originalData.txt"
# # HEADER_SIZE = 120
# # POINT_RECORD_SIZE = 32
# # POINT_FORMAT = '<'
# # UNPACK_STR = POINT_FORMAT + '3f I'  # 3个float + 1个unsigned int

# # # 读取文件
# # with open(filename, 'rb') as f:
# #     data = f.read()

# # # 跳过文件头，获取纯点数据
# # point_data = data[HEADER_SIZE:]

# # # 计算实际点数
# # num_points = len(point_data) // POINT_RECORD_SIZE
# # print(f"文件总大小: {len(data)} 字节")
# # print(f"跳过 {HEADER_SIZE} 字节头文件后，点数据部分为 {len(point_data)} 字节")
# # print(f"假设每个点占 {POINT_RECORD_SIZE} 字节，计算得到点数: {num_points}")

# # # 创建数组来存储点数据
# # all_points = []
# # all_intensities = []

# # # 解析每一个点
# # for i in range(num_points):
# #     start = i * POINT_RECORD_SIZE
# #     end = start + POINT_RECORD_SIZE
# #     point_bytes = point_data[start:end]
    
# #     try:
# #         # 解包核心操作
# #         unpacked_data = struct.unpack(UNPACK_STR, point_bytes[:struct.calcsize(UNPACK_STR)])
# #         # 假设前三个值是X,Y,Z
# #         x, y, z = unpacked_data[0:3]
# #         # 假设第四个值是强度
# #         intensity = unpacked_data[3]
        
# #         all_points.append([x, y, z])
# #         all_intensities.append(intensity)
# #     except struct.error as e:
# #         print(f"Error unpacking point {i} at offset {start}: {e}")
# #         print(f"Bytes: {point_bytes.hex()}")
# #         break

# # # 转换为numpy数组
# # points_array = np.array(all_points)
# # intensities_array = np.array(all_intensities)

# # # 数据清理
# # print(f"原始点数: {len(points_array)}")
# # valid_mask = np.all(np.isfinite(points_array), axis=1)
# # points_array = points_array[valid_mask]
# # intensities_array = intensities_array[valid_mask]
# # print(f"移除无效值后点数: {len(points_array)}")

# # # 限制强度值在合理范围内
# # intensities_array = np.clip(intensities_array, 0, 65535).astype(np.uint16)

# # # 创建并写入LAS文件
# # las = laspy.create(point_format=2)  # 选择点格式，2支持强度值

# # # 智能计算偏移和缩放因子
# # # 计算坐标范围
# # coord_ranges = np.ptp(points_array, axis=0)
# # print(f"坐标范围: X={coord_ranges[0]}, Y={coord_ranges[1]}, Z={coord_ranges[2]}")

# # # 设置偏移量为最小值
# # las.header.offsets = np.min(points_array, axis=0)
# # print(f"偏移量设置为: {las.header.offsets}")

# # # 根据坐标范围动态设置缩放因子
# # # LAS使用整数存储坐标，我们需要确保 (坐标 - 偏移量) / 缩放因子 在32位整数范围内
# # max_possible_value = 2147483647  # 32位有符号整数的最大值

# # # 计算每个维度所需的最小缩放因子
# # required_scales = coord_ranges / max_possible_value
# # # 取三个维度中最大的缩放需求，并向上取整到最近的10的幂次
# # max_required_scale = np.max(required_scales)
# # if max_required_scale > 0:
# #     # 计算10的幂次
# #     scale_exp = np.ceil(np.log10(max_required_scale))
# #     scale = 10 ** scale_exp
# # else:
# #     scale = 0.001  # 默认值

# # print(f"计算出的缩放因子: {scale}")

# # # 设置缩放因子
# # las.header.scales = [scale, scale, scale]

# # # 验证坐标值是否在合理范围内
# # scaled_coords = (points_array - las.header.offsets) / scale
# # if np.any(scaled_coords > max_possible_value) or np.any(scaled_coords < -max_possible_value):
# #     print("警告: 有些坐标值仍然超出范围，尝试增加缩放因子")
# #     # 找出超出范围的值
# #     out_of_range = np.any((scaled_coords > max_possible_value) | (scaled_coords < -max_possible_value), axis=1)
# #     print(f"有 {np.sum(out_of_range)} 个点超出范围")
# #     # 移除这些点
# #     points_array = points_array[~out_of_range]
# #     intensities_array = intensities_array[~out_of_range]
# #     print(f"移除超出范围的点后，剩余点数: {len(points_array)}")

# # # 设置坐标和强度
# # las.x = points_array[:, 0]
# # las.y = points_array[:, 1]
# # las.z = points_array[:, 2]
# # las.intensity = intensities_array

# # output_filename = filename.split('.')[0] + "_optimized.las"
# # las.write(output_filename)
# # print(f"转换成功！共转换 {len(points_array)} 个点。文件已保存为: {output_filename}")



# import numpy as np
# import matplotlib.pyplot as plt
# import laspy

# # ---------------- 用户参数 ----------------
# file_path = "/home/xcl/Cloud Points/REC_SCAN_0_360_T20250807164447_2025.9.13.txt"  # 输入二进制文件路径
# output_las = "output_2025_9_13_frame.las"          # 输出 LAS 文件名
# max_header_scan = 128               # 最大扫描文件头字节数
# dtypes = [('<f4','float32'), ('>f4','float32'), ('<i4','int32'), ('>i4','int32')]
# point_dims_list = [3, 4, 6]        # 尝试每点字段数
# coord_min, coord_max = -1e5, 1e5   # 坐标合理范围
# min_points_threshold = 10           # 至少点数
# num_plot_points = 1000              # 绘图前 num_plot_points 个点
# # -----------------------------------------

# # 读取文件
# with open(file_path, "rb") as f:
#     data = f.read()

# best_score = 0
# best_points = None
# best_params = None

# for header_size in range(0, min(max_header_scan, len(data)//10), 16):
#     for dtype_str, dtype_label in dtypes:
#         for point_dims in point_dims_list:
#             point_byte_len = np.dtype(dtype_str).itemsize * point_dims
#             num_points = (len(data) - header_size) // point_byte_len
#             if num_points < min_points_threshold:
#                 continue

#             data_points = data[header_size:header_size + num_points * point_byte_len]
#             try:
#                 points = np.frombuffer(data_points, dtype=dtype_str).reshape(-1, point_dims).copy()
#             except:
#                 continue

#             xyz = points[:, :3]
#             # 有限值判断，去掉 NaN/Inf
#             finite_mask = np.isfinite(xyz).all(axis=1)
#             xyz_valid = xyz[finite_mask]

#             if len(xyz_valid) == 0:
#                 continue

#             # 判断坐标是否在合理范围
#             valid_mask = np.all((xyz_valid > coord_min) & (xyz_valid < coord_max), axis=1)
#             valid_ratio = np.mean(valid_mask)

#             if valid_ratio < 0.1:
#                 continue

#             # 保存最合理方案
#             if valid_ratio > best_score:
#                 best_score = valid_ratio
#                 best_points = xyz_valid.astype(np.float64)  # 转为 float64 避免溢出
#                 best_params = (header_size, dtype_label, dtype_str, point_dims)

# # 输出结果
# if best_points is not None:
#     print(f"最佳方案: header={best_params[0]}, dtype={best_params[1]} ({best_params[2]}), dims={best_params[3]}, 有效比例={best_score:.2f}")

#     # 安全缩放：中心偏移 + 统一缩放到 0~1000
#     center = np.mean(best_points, axis=0)
#     scale_needed = np.max(np.ptp(best_points, axis=0))  # 最大坐标范围
#     if scale_needed == 0:
#         scale_needed = 1.0
#     xyz_scaled = (best_points - center) / scale_needed * 1000.0

#     # 绘制最优方案散点图
#     plt.figure(figsize=(6,6))
#     plt.scatter(xyz_scaled[:num_plot_points,0], xyz_scaled[:num_plot_points,1], s=1)
#     plt.title(f"最佳方案散点图（已安全缩放）: header={best_params[0]}, dtype={best_params[1]}, dims={best_params[3]}")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.show()

#     # 写 LAS 文件
#     las = laspy.create(file_version="1.4", point_format=3)
#     las.x = xyz_scaled[:,0]
#     las.y = xyz_scaled[:,1]
#     las.z = xyz_scaled[:,2]
#     las.write(output_las)
#     print(f"LAS 文件已生成: {output_las}（已安全缩放并清理 NaN/Inf）")

# else:
#     print("未找到合理解析方案，请尝试调整扫描范围或数据类型列表。")













# # import numpy as np
# # import matplotlib.pyplot as plt
# # import laspy
# # import os
# # from pathlib import Path

# # # ---------------- 用户参数 ----------------
# # folder_path = "/home/xcl/Cloud Points/frame100"  # 目标文件夹路径
# # output_folder = "/home/xcl/Cloud Points/output-100_frame"            # 输出文件夹
# # max_header_scan = 128                   # 最大扫描文件头字节数
# # dtypes = [('<f4','float32'), ('>f4','float32'), ('<i4','int32'), ('>i4','int32')]
# # point_dims_list = [3, 4, 6]             # 尝试每点字段数
# # coord_min, coord_max = -1e5, 1e5        # 坐标合理范围
# # min_points_threshold = 10               # 至少点数
# # num_plot_points = 1000                  # 绘图前 num_plot_points 个点
# # show_plot = False                       # 是否显示每个文件的散点图（大量文件时建议 False）
# # # -----------------------------------------

# # folder = Path(folder_path)
# # out_dir = folder / output_folder
# # out_dir.mkdir(exist_ok=True)

# # txt_files = sorted(folder.glob("*.txt"))
# # if not txt_files:
# #     print(f"文件夹 {folder} 下没有找到 txt 文件！")
# #     exit()

# # for file_path in txt_files:
# #     print(f"\n===== 正在处理: {file_path.name} =====")
# #     with open(file_path, "rb") as f:
# #         data = f.read()

# #     best_score = 0
# #     best_points = None
# #     best_params = None

# #     for header_size in range(0, min(max_header_scan, len(data)//10), 16):
# #         for dtype_str, dtype_label in dtypes:
# #             for point_dims in point_dims_list:
# #                 point_byte_len = np.dtype(dtype_str).itemsize * point_dims
# #                 num_points = (len(data) - header_size) // point_byte_len
# #                 if num_points < min_points_threshold:
# #                     continue

# #                 data_points = data[header_size:header_size + num_points * point_byte_len]
# #                 try:
# #                     points = np.frombuffer(data_points, dtype=dtype_str).reshape(-1, point_dims).copy()
# #                 except Exception:
# #                     continue

# #                 xyz = points[:, :3]
# #                 finite_mask = np.isfinite(xyz).all(axis=1)
# #                 xyz_valid = xyz[finite_mask]

# #                 if len(xyz_valid) == 0:
# #                     continue

# #                 valid_mask = np.all((xyz_valid > coord_min) & (xyz_valid < coord_max), axis=1)
# #                 valid_ratio = np.mean(valid_mask)

# #                 if valid_ratio < 0.1:
# #                     continue

# #                 if valid_ratio > best_score:
# #                     best_score = valid_ratio
# #                     best_points = xyz_valid.astype(np.float64)
# #                     best_params = (header_size, dtype_label, dtype_str, point_dims)

# #     if best_points is not None:
# #         print(f"最佳方案: header={best_params[0]}, dtype={best_params[1]} ({best_params[2]}), dims={best_params[3]}, 有效比例={best_score:.2f}")

# #         center = np.mean(best_points, axis=0)
# #         scale_needed = np.max(np.ptp(best_points, axis=0))
# #         if scale_needed == 0:
# #             scale_needed = 1.0
# #         xyz_scaled = (best_points - center) / scale_needed * 1000.0

# #         # 绘制散点图
# #         if show_plot:
# #             plt.figure(figsize=(6,6))
# #             plt.scatter(xyz_scaled[:num_plot_points,0], xyz_scaled[:num_plot_points,1], s=1)
# #             plt.title(f"{file_path.name} 散点图")
# #             plt.xlabel("X")
# #             plt.ylabel("Y")
# #             plt.show()

# #         # 写 LAS 文件
# #         output_las = out_dir / f"{file_path.stem}.las"
# #         las = laspy.create(file_version="1.4", point_format=3)
# #         las.x = xyz_scaled[:,0]
# #         las.y = xyz_scaled[:,1]
# #         las.z = xyz_scaled[:,2]
# #         las.write(output_las)
# #         print(f"✅ LAS 文件已生成: {output_las}")
# #     else:
# #         print(f"❌ 未找到合理解析方案: {file_path.name}")

# # print("\n全部文件处理完成！")
















import struct
import numpy as np
import laspy
import sys

FRAME_HEADER = 0x55AAAA55  # 帧头
FRAME_HEADER_SIZE = 4      # 帧头长度
TARGET_STRUCT = "<fffff"   # 方位角 仰角 距离 速度 幅度，每个float32
TARGET_SIZE = struct.calcsize(TARGET_STRUCT)

def parse_binary_file(filename):
    points = []
    amplitudes = []
    speeds = []

    with open(filename, "rb") as f:
        data = f.read()

    offset = 0
    total_frames = 0
    total_points = 0

    while offset + FRAME_HEADER_SIZE < len(data):
        frame_header = struct.unpack_from("<I", data, offset)[0]
        if frame_header != FRAME_HEADER:
            offset += 1
            continue

        # 读取目标数
        if offset + 8 > len(data):
            print("[WARN] 剩余数据不足，无法读取目标数，停止解析")
            break
        num_targets = struct.unpack_from("<I", data, offset + 4)[0]
        offset += 8

        frame_points = []
        frame_amplitudes = []
        frame_speeds = []

        for i in range(num_targets):
            if offset + TARGET_SIZE > len(data):
                print(f"[WARN] 帧{total_frames}声明目标数{num_targets}，但数据不足，仅解析{i}个")
                break

            az, el, rng, vel, amp = struct.unpack_from(TARGET_STRUCT, data, offset)
            offset += TARGET_SIZE

            # 转换为笛卡尔坐标
            x = rng * np.cos(np.deg2rad(el)) * np.cos(np.deg2rad(az))
            y = rng * np.cos(np.deg2rad(el)) * np.sin(np.deg2rad(az))
            z = rng * np.sin(np.deg2rad(el))

            frame_points.append([x, y, z])
            frame_amplitudes.append(amp)
            frame_speeds.append(vel)

        if frame_points:
            points.extend(frame_points)
            amplitudes.extend(frame_amplitudes)
            speeds.extend(frame_speeds)
            total_points += len(frame_points)

        total_frames += 1

    print(f"[INFO] 共解析 {total_frames} 帧, 总点数 {total_points}")
    return np.array(points), np.array(amplitudes), np.array(speeds)


def write_las(output_file, points, amplitudes, speeds):
    if points.shape[0] == 0:
        raise ValueError("没有解析到任何点，无法写入LAS文件")

    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    ranges = maxs - mins

    print(f"[INFO] 点云范围：X[{mins[0]:.3f},{maxs[0]:.3f}], Y[{mins[1]:.3f},{maxs[1]:.3f}], Z[{mins[2]:.3f},{maxs[2]:.3f}]")

    max_int32 = np.iinfo(np.int32).max
    scale = ranges / max_int32
    scale = np.where(scale < 1e-6, 1e-6, scale)  # 避免scale为0
    scale = np.minimum(scale, 0.001)  # 保留毫米精度上限

    print(f"[INFO] 自动选择 scale: {scale}, offset: {mins}")

    header = laspy.LasHeader(version="1.2", point_format=3)
    header.scales = scale
    header.offsets = mins

    las = laspy.LasData(header)
    try:
        las.x = points[:, 0]
        las.y = points[:, 1]
        las.z = points[:, 2]
    except OverflowError:
        raise RuntimeError(f"[ERROR] 仍然溢出，请检查scale/offset选择！scale={scale}, offset={mins}, ranges={ranges}")

    las.intensity = np.clip(amplitudes, 0, 65535).astype(np.uint16)
    las.gps_time = speeds.astype(np.float64)

    las.write(output_file)
    print(f"[INFO] LAS文件已保存: {output_file} (共 {points.shape[0]} 点)")


def main():
    if len(sys.argv) != 3:
        print("用法: python convert_bin_to_las.py input.txt output.las")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    points, amplitudes, speeds = parse_binary_file(input_file)
    write_las(output_file, points, amplitudes, speeds)


if __name__ == "__main__":
    main()
