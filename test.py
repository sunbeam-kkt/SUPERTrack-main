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
