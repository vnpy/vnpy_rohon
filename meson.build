project(
  'vnpy_rohon',
  'cpp',
  version: '6.5.1.20',
  license: 'MIT',
  meson_version: '>=1.7.0',
  default_options: [
    'buildtype=release',
    'cpp_std=c++17',
    'warning_level=2',
  ],
)

# 导入文件系统和Python模块
fs = import('fs')
py = import('python').find_installation(pure: false)
py_dep = py.dependency()

# 获取pybind11路径
python_cmd = host_machine.system() == 'windows' ? 'python' : 'python3'
pybind11_include_dir = run_command(python_cmd, '-c', 'import pybind11; print(pybind11.get_include())', check: true).stdout().strip()
message('使用pybind11路径: ' + pybind11_include_dir)

# 获取编译器信息
cpp = meson.get_compiler('cpp')
compiler_id = cpp.get_id()

# 输出构建目标系统信息
message('构建目标系统: ' + host_machine.system())

# 初始化变量
thostmduserapi_lib = []
thosttraderapi_lib = []
extra_cpp_args = []
extra_link_args = []

# 初始化库变量
thostmduserapi_lib = []
thosttraderapi_lib = []

# 初始化其他编译选项
install_rpath_value = ''

# 设置Windows特定编译选项
if host_machine.system() == 'windows'
  # Windows编译器设置
  add_project_arguments('/MT', language : 'cpp')
  
  # 设置库目录
  lib_dir = meson.current_source_dir() / 'vnpy_rohon/api/libs'
  api_dir = meson.current_source_dir() / 'vnpy_rohon/api'
  
  # 设置include目录
  include_dirs = include_directories(
    'vnpy_rohon/api/include',
    'vnpy_rohon/api/vnrohon',
    pybind11_include_dir,
  )
  
  # 定义CTP库
  thostmduserapi_lib = cpp.find_library('thostmduserapi_se', 
                                       dirs: [lib_dir, api_dir],
                                       required: true)
  thosttraderapi_lib = cpp.find_library('thosttraderapi_se', 
                                       dirs: [lib_dir, api_dir],
                                       required: true)

# 设置Linux特定编译选项
else  # Linux
  # Linux编译器设置
  extra_cpp_args = [
    '-std=c++17',
    '-O3',
    '-Wno-delete-incomplete',
    '-Wno-sign-compare',
  ]
  
  extra_link_args = [
    '-lstdc++',
    '-Wl,-rpath,$ORIGIN',  # 添加rpath设置，使库能在运行时找到同目录下的动态库
  ]
  
  # 设置库目录
  lib_dir = meson.current_source_dir() / 'vnpy_rohon/api'
  
  # 设置include目录
  include_dirs = include_directories(
    'vnpy_rohon/api/include',
    'vnpy_rohon/api/vnrohon',
    pybind11_include_dir,
  )
  
  # 定义CTP库
  thostmduserapi_lib = cpp.find_library('thostmduserapi_se', 
                                       dirs: [lib_dir],
                                       required: true)
  thosttraderapi_lib = cpp.find_library('thosttraderapi_se_6.3.19', 
                                       dirs: [lib_dir],
                                       required: true)
endif

# 创建MD模块扩展
md_module = py.extension_module(
  'vnrohonmd',
  sources: ['vnpy_rohon/api/vnrohon/vnrohonmd/vnrohonmd.cpp'],
  include_directories: include_dirs,
  dependencies: [py_dep, thostmduserapi_lib],
  cpp_args: extra_cpp_args,
  link_args: extra_link_args,
  install: true,
  subdir: 'vnpy_rohon/api'
)

# 创建TD模块扩展
td_module = py.extension_module(
  'vnrohontd',
  sources: ['vnpy_rohon/api/vnrohon/vnrohontd/vnrohontd.cpp'],
  include_directories: include_dirs,
  dependencies: [py_dep, thosttraderapi_lib],
  cpp_args: extra_cpp_args,
  link_args: extra_link_args,
  install: true,
  subdir: 'vnpy_rohon/api'
)

# 安装Python源代码
python_files = [
  ['vnpy_rohon/__init__.py', 'vnpy_rohon'],
  ['vnpy_rohon/api/__init__.py', 'vnpy_rohon/api'],
  ['vnpy_rohon/api/rohon_constant.py', 'vnpy_rohon/api'],
  ['vnpy_rohon/gateway/__init__.py', 'vnpy_rohon/gateway'],
  ['vnpy_rohon/gateway/rohon_gateway.py', 'vnpy_rohon/gateway'],
]

foreach file : python_files
  py.install_sources(
    [file[0]],
    pure: false,
    subdir: file[1]
  )
endforeach

# 安装API动态库文件
if host_machine.system() == 'windows'
  api_libs = [
    'vnpy_rohon/api/thostmduserapi_se.dll',
    'vnpy_rohon/api/thosttraderapi_se.dll',
  ]
  
  install_data(
    api_libs,
    install_dir: py.get_install_dir() / 'vnpy_rohon/api'
  )
else  # Linux
  api_libs = [
    'vnpy_rohon/api/libthostmduserapi_se.so',
    'vnpy_rohon/api/libthosttraderapi_se_6.3.19.so',
    'vnpy_rohon/api/librohonbase.so',
    'vnpy_rohon/api/libLinuxDataCollect.so'
  ]
  
  install_data(
    api_libs,
    install_dir: py.get_install_dir() / 'vnpy_rohon/api'
  )

endif
