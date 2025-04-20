#!/bin/bash

# 执行Python安装命令
python3 -m pip install .

# 获取vnpy_rohon的安装路径
SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")
ROHON_API_DIR="${SITE_PACKAGES}/vnpy_rohon/api"

# 设置目标系统库目录
if [ -d "/usr/lib" ]; then
    LIB_DIR="/usr/lib"
elif [ -d "/usr/local/lib" ]; then
    LIB_DIR="/usr/local/lib"
else
    echo "错误: 无法找到系统库目录"
    exit 1
fi

echo "源目录: $ROHON_API_DIR"
echo "目标目录: $LIB_DIR"

# 复制库文件到系统目录
for LIB in "librohonbase.so" "libLinuxDataCollect.so"; do
    if [ -f "${ROHON_API_DIR}/${LIB}" ]; then
        echo "复制 ${LIB} 到 ${LIB_DIR}"
        sudo cp "${ROHON_API_DIR}/${LIB}" "${LIB_DIR}/"
    else
        echo "警告: ${ROHON_API_DIR}/${LIB} 不存在"
    fi
done

# 刷新系统库缓存
sudo ldconfig

echo "完成!" 