# yqn_project_cli

####console runner:
yqn-project -c absolute_json_file_path
****
yqn-autoview - c new_json_file_path which named project_name.json in config dir for generating module or view automatically
****

####json-file format:
```json
{
  "app_id": 22010,
  "app_name": "project_name",
  "app_path": "absolute_project_dir_path",
  "path_list": [
    {
      "path": "/index/", 
      "module": "main",
      "view_cls": "Index",
      "view_mth": "get_index",
      "http_methods": ["GET", "POST"],
      "doc": "默认"
    },
    {
      "path": "/tool/",
      "module": "tool",
      "view_cls": "Index",
      "view_mth": "get_tool",
      "http_methods": ["GET", "POST"],
      "doc": "工具"
    }
  ]
}
```

####参数解释：
****
#####app_id：项目唯一数字标识
#####项目(app_name)位于路径(app_path)下
#####path_list：所有需路由对象信息数组
****
#####path: http请求路径
#####module: api下的对应模块，便于分块，如 main、tool
#####view_cls: api对应模块下views.py文件内的视图类, 如 Index
#####view_mth: 对应视图类下实例方法, 如 get_index、get_tool，http请求时产生调用
#####http_methods: 支持http请求方式
#####doc: 方法doc描述




