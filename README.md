# front

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).



# Backen项目组织（flask框架）

```
│  app.py  # 应用主文件
│  config.py  # 配置文件
│  models.py  # ORM模型
│  README.md
│  requirements.txt  # 依赖文件列表
│
├─.idea
│  │  .gitignore
│  │  deployment.xml
│  │  misc.xml
│  │  modules.xml
│  │  workspace.xml
│  │  功能点分析子系统.iml
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│
└─__pycache__
        app.cpython-312.pyc
        models.cpython-312.pyc
```

# 启动项目

首先安装依赖：

```cmd
pip install -r requirements.txt
```

然后启动`app.py`：

```cmd
python app.py
```

# 接口文档

## /projects 接口

- **接口方法：**GET

- **调用方法：**`/projects?user_id={$id}`

- **接收参数：**`user_id: int`

- **返回参数：**

  - 如果用户是**评估师**角色，则返回此用户的**昵称**和**项目列表**。详细字段如下：

    ```json
    {
        "user_name": "Alice",
        "projects": [
            {
                "id": 10,
                "name": "Project A",
                "requirement": "Requirement A",
                "start_time": "2024-11-01 09:00:00",
                "deadline": "2024-12-01 17:00:00",
                "owner_name": "Bob"
            },
            {
                "id": 11,
                "name": "Project B",
                "requirement": "Requirement B",
                "start_time": "2024-11-05 10:00:00",
                "deadline": "2024-12-15 17:00:00",
                "owner_name": "Charlie"
            }
        ]
    }
    
    ```

  - 如果用户不是评估师，则返回错误信息（403 FORBIDDEN）。

    ```json
    {
        "error": "Access denied: User is not an estimator"
    }
    ```

## /get-functionpoint 接口

- **接口方法**：GET

- **调用方法**：`/get-functionpoint?project_id={$id}`

- **接收参数**：

  - `project_id: int` （必填）  
    指定查询的项目 ID。

- **返回参数**：

  - 如果 `project_id` 存在于 `FunctionPoint` 表中，返回此项目的所有功能点信息。详细字段如下：

    ```json
    {
        "project_id": 1,
        "function_points": [
            {
                "id": 101,
                "name": "Input A",
                "type": "EI",
                "complexity": "LOW",
                "base_value": 3,
                "comment": "This is a sample comment", 
                "created_at": "2024-11-01 09:00:00"
            },
            {
                "id": 102,
                "name": "Output B",
                "type": "EO",
                "complexity": "HIGH",
                "base_value": 7,
                "comment": null,
                "created_at": "2024-11-02 10:00:00"
            }
        ]
    }
    ```

  - 如果 `project_id` 不存在或没有功能点记录，返回以下信息（200 OK）：

    ```json
    {
        "message": "No function points found for the given project ID",
        "data": []
    }
    ```

  - 如果未提供 `project_id`，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

## /edit-functionpoint 接口

- **接口方法**：POST

- **调用方法**：`/edit-functionpoint`

- **接收参数**（`application/json` 格式）：

  - `id: int` （必填）  
    功能点的唯一标识符。
  - `name: str` （必填）  
    功能点的名称。
  - `type: str` （必填，取值范围：`ILF`, `EIF`, `EI`, `EO`, `EQ`）  
    功能点的类型。
  - `complexity: str` （必填，取值范围：`LOW`, `MEDIUM`, `HIGH`）  
    功能点的复杂度。
  - `comment: str` （可选）  
    功能点的备注信息。

- **返回参数**：

  - 如果更新成功，返回：

    ```json
    {
        "message": "Function point updated successfully"
    }
    ```

  - 如果参数不完整或格式不正确，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "id, name, type, and complexity are required"
    }
    ```

  - 如果 `id` 不存在，返回错误信息（404 NOT FOUND）：

    ```json
    {
        "error": "Function point with id 101 not found"
    }
    ```

## /add-functionpoint 接口

- **接口方法**：POST

- **调用方法**：`/add-functionpoint`

- **接收参数**（`application/json` 格式）：

  - `project_id: int` （必填）  
    指定功能点所属的项目 ID。
  - `name: str` （必填）  
    功能点的名称。
  - `type: str` （必填，取值范围：`ILF`, `EIF`, `EI`, `EO`, `EQ`）  
    功能点的类型。
  - `complexity: str` （必填，取值范围：`LOW`, `MEDIUM`, `HIGH`）  
    功能点的复杂度。
  - `comment: str` （可选）  
    功能点的备注信息。

- **返回参数**：

  - 如果添加成功，返回：

    ```json
    {
        "message": "Function point added successfully",
        "id": 105
    }
    ```

    - `id` 是新添加功能点的唯一标识符。

  - 如果参数不完整或格式不正确，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "project_id, name, type, and complexity are required"
    }
    ```

## /delete-functionpoint 接口

- **接口方法**：DELETE

- **调用方法**：`/delete-functionpoint`

- **接收参数**（`application/json` 格式）：

  - `id: int` （必填）  
    功能点的唯一标识符。

- **返回参数**：

  - 如果删除成功，返回：

    ```json
    {
        "message": "Function point deleted successfully"
    }
    ```

  - 如果参数不完整，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "id is required"
    }
    ```

  - 如果 `id` 不存在，返回错误信息（404 NOT FOUND）：

    ```json
    {
        "error": "Function point with id 105 not found"
    }
    ```

## /export-functionpoints 接口

- **接口方法**：GET

- **调用方法**：`/export-functionpoints?project_id={$id}`

- **接收参数**：

  - `project_id: int` （必填）  
    指定查询功能点的项目 ID。

- **返回参数**：

  - 如果查询到功能点数据，返回一个包含以下列的 CSV 文件：

    - `Name`：功能点名称。
    - `Type`：功能点类型（如 `ILF`, `EIF`）。
    - `Complexity`：功能点复杂度（如 `LOW`, `MEDIUM`, `HIGH`）。
    - `Base Value`：功能点的基础分值。
    - `Comment`：功能点备注。

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果 `project_id` 不存在或没有功能点记录，返回错误信息（404 NOT FOUND）：

    ```json
    {
        "error": "No function points found for project_id 1"
    }
    ```

- **示例 CSV 文件**（功能点数据）：

```
Name,Type,Complexity,Base Value,Comment
Input A,EI,LOW,3,Sample comment for Input A
Output B,EO,HIGH,7,Output B is highly complex
File C,ILF,MEDIUM,10,Internal file for storing data
```

## /import-functionpoints 接口

>  **警告：此方法覆写项目中所有已有的功能点。**

- **接口方法**：POST

- **调用方法**：`/import-functionpoints`

- **接收参数**：

  1. `project_id: int` （必填）  
     指定功能点所属的项目 ID。
  2. 上传文件：CSV 文件，包含以下列：
     - `Name`：功能点名称（必填）
     - `Type`：功能点类型（必填，取值范围：`ILF`, `EIF`, `EI`, `EO`, `EQ`）
     - `Complexity`：功能点复杂度（必填，取值范围：`LOW`, `MEDIUM`, `HIGH`）
     - `Comment`：功能点备注信息（可选）

- **返回参数**：

  - 如果导入成功，返回：

    ```json
    {
        "message": "Function points imported successfully",
        "count": 3
    }
    ```

    - `count` 是导入的功能点数量。

  - 如果 CSV 文件或数据格式不正确，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Invalid CSV headers. Expected: ['Name', 'Type', 'Complexity', 'Comment']"
    }
    ```

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果 CSV 文件为空或无有效数据，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "CSV file is empty"
    }
    ```

  - 如果项目功能点导入失败，返回错误信息（500 INTERNAL SERVER ERROR）。

  ### 测试示例

  #### **请求**

  ```http
  POST /import-functionpoints
  Content-Type: multipart/form-data
  
  Form Data:
  - project_id: 1
  - file: [上传的CSV文件]
  ```

  #### **示例CSV内容**

  ```csv
  Name,Type,Complexity,Comment
  Input A,EI,LOW,Sample comment for Input A
  Output B,EO,HIGH,Output B is highly complex
  File C,ILF,MEDIUM,Internal file for storing data
  ```

  #### **成功响应**

  ```json
  {
      "message": "Function points imported successfully",
      "count": 3
  }
  ```

  #### **失败响应**

  1. **CSV文件列名错误**：

     ```json
     {
         "error": "Invalid CSV headers. Expected: ['Name', 'Type', 'Complexity', 'Comment']"
     }
     ```

  2. **空CSV文件**：

     ```json
     {
         "error": "CSV file is empty"
     }
     ```

  3. **项目ID未提供**：

     ```json
     {
         "error": "Project ID is required"
     }
     ```

## /total-functionpoint 接口

- **接口方法**：GET

- **调用方法**：`/total-functionpoint?project_id={$id}`

- **接收参数**：

  - `project_id: int` （必填）  
    指定查询功能点的项目 ID。

- **返回参数**：

  - 如果查询成功，返回：

    ```json
    {
        "project_id": 1,
        "total_counts": {
            "ILF": 3,
            "EIF": 2,
            "EI": 5,
            "EO": 4,
            "EQ": 1
        }
    }
    ```

    - `total_counts` 是一个字典，键是功能点的 `type`，值是该类型功能点的数量。

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果项目下没有功能点记录，返回空结果：

    ```json
    {
        "project_id": 1,
        "total_counts": {}
    }
    ```

## /cal-functionpoint 接口

> **此接口每次点击“计算功能点”时调用。每次调用会新建一条记录**

- **接口方法**：POST

- **调用方法**：`/cal-functionpoint`

- **接收参数**（`application/json` 格式）：

  1. `project_id: int` （必填）  
     指定项目 ID。
  2. `total_weight: float` （必填）  
     GSC 的总权重，必须为非负数。
  3. `scf_stage: int` （必填）  
     SCF 阶段参数，表示当前功能点所属的开发阶段，取值范围为：
     - `0`：立项（调整系数 2.0）
     - `1`：招标（调整系数 1.5）
     - `2`：早期（调整系数 1.26）
     - `3`：中期（调整系数 1.26）
     - `4`：完成（调整系数 1.0）

- **返回参数**：

  - 如果计算成功，返回：

    ```json
    {
        "project_id": 1,
        "UFP": 65,
        "SCF_AFP": 81.9,
        "VAF": 1.01,
        "GSC_AFP": 82.719
    }
    ```

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果 `scf_stage` 参数非法，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Invalid SCF stage. Must be one of [0, 1, 2, 3, 4]"
    }
    ```

  - 如果项目没有功能点记录，返回错误信息（404 NOT FOUND）：

    ```json
    {
        "error": "No function points found for project_id 1"
    }
    ```

示例请求：

```json
POST /cal-functionpoint
Content-Type: application/json

{
    "project_id": 1,
    "total_weight": 36,
    "scf_stage": 2
}
```

## /export-results 接口

- **接口方法**：GET

- **调用方法**：`/export-results?project_id={$id}`

- **接收参数**：

  - `project_id: int` （必填）  
    指定需要导出功能点和计算记录的项目 ID。

- **返回参数**：

  - 如果查询成功，返回两个 CSV 文件内容：

    ```json
    {
        "function_points_csv": "CSV 内容的字符串格式",
        "calculation_records_csv": "CSV 内容的字符串格式"
    }
    ```

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果功能点记录或计算记录为空，返回错误信息（404 NOT FOUND）。

---

### **导出的 CSV 文件格式**

**1. function_points.csv**

| **name** | **type** | **complexity** | **base_value** | **created_at**      | **comment**           |
| -------- | -------- | -------------- | -------------- | ------------------- | --------------------- |
| Input A  | EI       | LOW            | 3              | 2024-11-18 10:30:00 | Sample comment        |
| File B   | ILF      | MEDIUM         | 10             | 2024-11-18 11:00:00 | Internal logical file |

**2. calculation_records.csv**

| **created_at**      | **GSC_AFP** | **UFP** | **SCF_AFP** | **VAF** | **total_weight** | **scf_stage** |
| ------------------- | ----------- | ------- | ----------- | ------- | ---------------- | ------------- |
| 2024-11-18 10:30:00 | 82.719      | 65      | 81.9        | 1.01    | 36.0             | 2             |
| 2024-11-18 11:00:00 | 70.5        | 55      | 70.0        | 1.05    | 40.0             | 1             |

## /get-calculations 接口

> **此接口用于可视化比较多次计算的数据变化。**

- **接口方法**：GET

- **调用方法**：`/get-calculations?project_id={$id}`

- **接收参数**：

  - `project_id: int` （必填）  
    指定查询计算记录的项目 ID。

- **返回参数**：

  - 成功时返回一个 JSON 数组，每个元素表示一个计算记录，**按照从新到旧排序**：

    ```json
    [
        {
            "created_at": "2024-11-18 11:00:00",
            "GSC_AFP": 82.719,
            "UFP": 65,
            "SCF_AFP": 81.9,
            "VAF": 1.01,
            "total_weight": 36.0,
            "scf_stage": 2
        },
        {
            "created_at": "2024-11-18 10:30:00",
            "GSC_AFP": 70.5,
            "UFP": 55,
            "SCF_AFP": 70.0,
            "VAF": 1.05,
            "total_weight": 40.0,
            "scf_stage": 1
        }
    ]
    ```

  - 如果 `project_id` 未提供，返回错误信息（400 BAD REQUEST）：

    ```json
    {
        "error": "Project ID is required"
    }
    ```

  - 如果没有计算记录，返回错误信息（404 NOT FOUND）：

    ```json
    {
        "error": "No calculation records found for project_id 1"
    }
    ```
