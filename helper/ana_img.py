import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib

# 确保使用 'Agg' 后端
matplotlib.use('Agg')


def ana_img(stock: str = ""):
    # 检查文件是否存在
    image_path = f"D:\\stock_img\\{stock}\\{stock}.png"
    if not os.path.exists(image_path):
        print("文件路径不存在")
    else:
        # 读取彩色图像
        image = cv2.imread(image_path)

        # 检查图像是否成功读取
        if image is None:
            print("图像读取失败，请检查文件路径和文件格式。")
        else:
            print("图像读取成功。")

            # 转换为HSV颜色空间
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # 定义红色的范围
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            # 通过颜色范围创建掩膜
            mask1 = cv2.inRange(hsv_image, lower_red, upper_red)
            mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
            mask = mask1 + mask2

            # 应用掩膜到原始图像
            result = cv2.bitwise_and(image, image, mask=mask)

            # 转换为灰度图像并进行二值化
            gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)

            # 形态学操作，去除噪声
            kernel = np.ones((3, 3), np.uint8)
            binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

            # 显示二值化图像
            plt.imshow(binary_image, cmap='gray')
            plt.title('Binary Image')
            plt.savefig(f"D:\\stock_img\\{stock}\\binary_image.png")
            plt.close()

            # 找到轮廓
            contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 检查找到的轮廓数量
            if len(contours) == 0:
                print("未找到任何轮廓，请检查图像的质量和预处理步骤。")
            else:
                # 假设目标轮廓是面积最大的一个
                contour = max(contours, key=cv2.contourArea)

                # 计算折点数
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # 遍历所有折点并标注趋势
                trends = []
                for i in range(len(approx) - 1):
                    point1 = approx[i][0]
                    point2 = approx[i + 1][0]
                    if point2[1] < point1[1]:
                        trends.append("上升")
                    elif point2[1] > point1[1]:
                        trends.append("下降")
                    else:
                        trends.append("平稳")

                # 输出结果
                print("折点数:", len(approx))
                print("所有折点的走势:", trends)

                # 可视化结果
                color_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
                for point in approx:
                    cv2.circle(color_image, tuple(point[0]), 5, (0, 0, 255), -1)

                # 绘制每两个折点之间的线段，并标注趋势
                for i in range(len(approx) - 1):
                    point1 = tuple(approx[i][0])
                    point2 = tuple(approx[i + 1][0])
                    if trends[i] == "上升":
                        color = (0, 255, 0)
                        trend_text = "上升"
                    elif trends[i] == "下降":
                        color = (0, 0, 255)
                        trend_text = "下降"
                    else:
                        color = (255, 255, 0)
                        trend_text = "平稳"
                    cv2.line(color_image, point1, point2, color, 2)
                    cv2.putText(color_image, trend_text, (point1[0], point1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color, 1)

                # 使用 matplotlib 显示处理后的图像
                plt.imshow(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
                plt.title('Contour Analysis')
                plt.savefig(f"D:\\stock_img\\{stock}\\contour_analysis.png")
                plt.close()

                # 保存结果
                cv2.imwrite(f"D:\\stock_img\\{stock}\\contour_analysis_cv2.png", color_image)
                print("结果已保存为 contour_analysis.png 和 contour_analysis_cv2.png")
