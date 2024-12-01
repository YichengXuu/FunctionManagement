from flask import Flask, request, jsonify, Response
from models import db, User, Project, ProjectUserLink, FunctionPoint, CalculationResult, Tenant
import csv
import io
from io import StringIO
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有域名访问，默认支持所有路由

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shixun:TEzzsLddDRdDwXdE@localhost:3306/shixun'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 初始化数据库
db.init_app(app)

# 数据库初始化（在应用启动时执行）
with app.app_context():
    db.create_all()



@app.route('/projects', methods=['GET'])
def get_projects():
    # 获取用户ID
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # 查询用户信息
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 检查用户角色
    if user.role != 2:  # 仅分析师可以访问
        return jsonify({'error': 'Access denied: User is not an estimator'}), 403

    # 查询与分析师相关的项目
    project_links = ProjectUserLink.query.filter_by(user_id=user_id).all()
    project_ids = [pl.project_id for pl in project_links]

    # 获取项目及拥有者信息
    projects = []
    for project_id in project_ids:
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            continue
        # 从 Tenant 表中查找 owner_name
        tenant = Tenant.query.filter_by(id=project.owner_id).first()
        owner_name = tenant.name if tenant else 'Unknown'
        projects.append({
            'id': project.id,
            'name': project.name,
            'requirement': project.requirement,
            'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'deadline': project.deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'owner_name': owner_name
        })

    # 返回结果
    return jsonify({
        'user_name': user.username,
        'projects': projects
    }), 200



@app.route('/get-functionpoint', methods=['GET'])
def get_function_point():
    # 获取 project_id 参数
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 查询 FunctionPoint 表
    function_points = FunctionPoint.query.filter_by(project_id=project_id).all()

    # 如果没有数据，返回空列表
    if not function_points:
        return jsonify({'message': 'No function points found for the given project ID', 'data': []}), 200

    # 构造返回数据
    result = []
    for fp in function_points:
        result.append({
            'id': fp.id,
            'name': fp.name,
            'type': fp.type,
            'complexity': fp.complexity,
            'base_value': fp.base_value,
            'comment': fp.comment,  # 新增字段
            'created_at': fp.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'project_id': project_id, 'function_points': result}), 200

@app.route('/edit-functionpoint', methods=['POST'])
def edit_function_point():
    # 获取请求数据
    data = request.json
    point_id = data.get('id')
    name = data.get('name')
    type_ = data.get('type')  # 避免与 Python 的内置关键字冲突
    complexity = data.get('complexity')
    comment = data.get('comment')

    # 验证必填字段
    if not all([point_id, name, type_, complexity]):
        return jsonify({'error': 'id, name, type, and complexity are required'}), 400

    # 验证 type 和 complexity 是否合法
    valid_types = ['ILF', 'EIF', 'EI', 'EO', 'EQ']
    valid_complexities = ['LOW', 'MEDIUM', 'HIGH']
    if type_ not in valid_types or complexity not in valid_complexities:
        return jsonify({'error': f'Invalid type or complexity. Valid types: {valid_types}, complexities: {valid_complexities}'}), 400

    # 查询功能点
    function_point = FunctionPoint.query.filter_by(id=point_id).first()
    if not function_point:
        return jsonify({'error': f'Function point with id {point_id} not found'}), 404

    # 根据规则计算 base_value
    base_value_lookup = {
        'ILF': {'LOW': 7, 'MEDIUM': 10, 'HIGH': 15},
        'EIF': {'LOW': 5, 'MEDIUM': 7, 'HIGH': 10},
        'EI': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
        'EO': {'LOW': 4, 'MEDIUM': 5, 'HIGH': 7},
        'EQ': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
    }
    base_value = base_value_lookup[type_][complexity]

    # 更新功能点数据
    function_point.name = name
    function_point.type = type_
    function_point.complexity = complexity
    function_point.comment = comment
    function_point.base_value = base_value

    # 保存到数据库
    db.session.commit()

    return jsonify({'message': 'Function point updated successfully'}), 200

@app.route('/add-functionpoint', methods=['POST'])
def add_function_point():
    # 获取请求数据
    data = request.json
    project_id = data.get('project_id')
    name = data.get('name')
    type_ = data.get('type')  # 避免与 Python 的内置关键字冲突
    complexity = data.get('complexity')
    comment = data.get('comment')

    # 验证必填字段
    if not all([project_id, name, type_, complexity]):
        return jsonify({'error': 'project_id, name, type, and complexity are required'}), 400

    # 验证 type 和 complexity 是否合法
    valid_types = ['ILF', 'EIF', 'EI', 'EO', 'EQ']
    valid_complexities = ['LOW', 'MEDIUM', 'HIGH']
    if type_ not in valid_types or complexity not in valid_complexities:
        return jsonify({'error': f'Invalid type or complexity. Valid types: {valid_types}, complexities: {valid_complexities}'}), 400

    # 根据规则计算 base_value
    base_value_lookup = {
        'ILF': {'LOW': 7, 'MEDIUM': 10, 'HIGH': 15},
        'EIF': {'LOW': 5, 'MEDIUM': 7, 'HIGH': 10},
        'EI': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
        'EO': {'LOW': 4, 'MEDIUM': 5, 'HIGH': 7},
        'EQ': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
    }
    base_value = base_value_lookup[type_][complexity]

    # 插入新功能点
    new_function_point = FunctionPoint(
        project_id=project_id,
        name=name,
        type=type_,
        complexity=complexity,
        comment=comment,
        base_value=base_value
    )
    db.session.add(new_function_point)
    db.session.commit()

    return jsonify({'message': 'Function point added successfully', 'id': new_function_point.id}), 201

@app.route('/delete-functionpoint', methods=['DELETE'])
def delete_function_point():
    # 获取请求数据
    data = request.json
    point_id = data.get('id')

    # 验证必填字段
    if not point_id:
        return jsonify({'error': 'id is required'}), 400

    # 查询功能点
    function_point = FunctionPoint.query.filter_by(id=point_id).first()
    if not function_point:
        return jsonify({'error': f'Function point with id {point_id} not found'}), 404

    # 删除功能点
    db.session.delete(function_point)
    db.session.commit()

    return jsonify({'message': 'Function point deleted successfully'}), 200

@app.route('/export-functionpoints', methods=['GET'])
def export_function_points():
    # 获取 project_id 参数
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 查询指定项目的功能点
    function_points = FunctionPoint.query.filter_by(project_id=project_id).all()
    if not function_points:
        return jsonify({'error': f'No function points found for project_id {project_id}'}), 404

    # 创建 CSV 数据
    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    writer.writerow(['Name', 'Type', 'Complexity', 'Base Value', 'Comment'])

    # 写入功能点数据
    for fp in function_points:
        writer.writerow([
            fp.name,
            fp.type,
            fp.complexity,
            fp.base_value,
            fp.comment if fp.comment else ''
        ])

    # 准备响应
    output.seek(0)
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=functionpoints_project_{project_id}.csv'
    return response

@app.route('/import-functionpoints', methods=['POST'])
def import_function_points():
    # 获取 project_id 参数
    project_id = request.form.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 获取上传的 CSV 文件
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'CSV file is required'}), 400

    # 解析 CSV 文件
    try:
        stream = StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)

        # 验证 CSV 的列名是否正确
        expected_headers = ['Name', 'Type', 'Complexity', 'Comment']
        if reader.fieldnames != expected_headers:
            return jsonify({'error': f'Invalid CSV headers. Expected: {expected_headers}'}), 400

        # 读取 CSV 内容并验证数据
        new_function_points = []
        valid_types = ['ILF', 'EIF', 'EI', 'EO', 'EQ']
        valid_complexities = ['LOW', 'MEDIUM', 'HIGH']

        for row in reader:
            # 验证必填字段和合法性
            if not all(row.get(col) for col in ['Name', 'Type', 'Complexity']):
                return jsonify({'error': 'CSV contains empty required fields'}), 400
            if row['Type'] not in valid_types or row['Complexity'] not in valid_complexities:
                return jsonify({'error': f"Invalid Type or Complexity in row: {row}"}), 400

            # 根据规则计算 base_value
            base_value_lookup = {
                'ILF': {'LOW': 7, 'MEDIUM': 10, 'HIGH': 15},
                'EIF': {'LOW': 5, 'MEDIUM': 7, 'HIGH': 10},
                'EI': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
                'EO': {'LOW': 4, 'MEDIUM': 5, 'HIGH': 7},
                'EQ': {'LOW': 3, 'MEDIUM': 4, 'HIGH': 6},
            }
            base_value = base_value_lookup[row['Type']][row['Complexity']]

            # 构造功能点对象
            new_function_points.append(FunctionPoint(
                project_id=project_id,
                name=row['Name'],
                type=row['Type'],
                complexity=row['Complexity'],
                comment=row['Comment'] if row['Comment'] else '',
                base_value=base_value
            ))

        # 如果 CSV 为空，不进行覆写
        if not new_function_points:
            return jsonify({'error': 'CSV file is empty'}), 400

        # 开始覆写操作
        db.session.query(FunctionPoint).filter_by(project_id=project_id).delete()
        db.session.bulk_save_objects(new_function_points)
        db.session.commit()

        return jsonify({'message': 'Function points imported successfully', 'count': len(new_function_points)}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to process CSV file: {str(e)}'}), 500

@app.route('/total-functionpoint', methods=['GET'])
def total_function_point():
    # 获取 project_id 参数
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 查询每种 type 的功能点数量
    result = (
        db.session.query(FunctionPoint.type, db.func.count(FunctionPoint.id))
        .filter(FunctionPoint.project_id == project_id)
        .group_by(FunctionPoint.type)
        .all()
    )

    # 构造返回结果
    total_counts = {type_: count for type_, count in result}

    return jsonify({'project_id': project_id, 'total_counts': total_counts}), 200

@app.route('/cal-functionpoint', methods=['POST'])
def calculate_function_points():
    # 获取请求数据
    data = request.json
    project_id = data.get('project_id')
    total_weight = data.get('total_weight', 0)  # VAF 总权重
    scf_stage = data.get('scf_stage')  # SCF_AFP 阶段参数

    # 参数验证
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400
    if not isinstance(total_weight, (int, float)) or total_weight < 0:
        return jsonify({'error': 'Total weight must be a non-negative number'}), 400
    if scf_stage not in [0, 1, 2, 3, 4]:
        return jsonify({'error': 'Invalid SCF_AFP stage. Must be one of [0, 1, 2, 3, 4]'}), 400

    # SCF_AFP 调整系数映射
    scf_stage_mapping = {
        0: 2.0,    # 立项
        1: 1.5,    # 招标
        2: 1.26,   # 早期
        3: 1.26,   # 中期
        4: 1.0     # 完成
    }
    scf_adjustment = scf_stage_mapping[scf_stage]

    # 查询 FunctionPoint 表
    function_points = FunctionPoint.query.filter_by(project_id=project_id).all()
    if not function_points:
        return jsonify({'error': f'No function points found for project_id {project_id}'}), 404

    # 计算 UFP
    ufp = 0
    for fp in function_points:
        ufp += fp.base_value  # 累加每个功能点的 base_value

    # 计算 SCF_AFP
    scf_afp = ufp * scf_adjustment

    # 计算 VAF
    vaf = 0.65 + 0.01 * total_weight

    # 计算 GSC_AFP
    gsc_afp = ufp * vaf

    # 插入新记录到 CalculationResult 表
    calculation = CalculationResult(
        project_id=project_id,
        GSC_AFP=gsc_afp,
        UFP=ufp,
        SCF_AFP=scf_afp,
        VAF=vaf,
        total_weight=total_weight,  # 存储 total_weight 参数
        scf_stage=scf_stage,        # 存储 scf_stage 参数
        created_at=datetime.utcnow()
    )
    db.session.add(calculation)

    # 提交到数据库
    db.session.commit()

    # 返回计算结果
    return jsonify({
        'project_id': project_id,
        'UFP': ufp,
        'SCF_AFP': scf_afp,
        'VAF': vaf,
        'GSC_AFP': gsc_afp
    }), 200

@app.route('/export-results', methods=['GET'])
def export_results():
    # 获取 project_id 参数
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 查询功能点数据
    function_points = FunctionPoint.query.filter_by(project_id=project_id).all()
    if not function_points:
        return jsonify({'error': f'No function points found for project_id {project_id}'}), 404

    # 查询计算记录数据
    calculation_records = CalculationResult.query.filter_by(project_id=project_id).order_by(CalculationResult.created_at.desc()).all()
    if not calculation_records:
        return jsonify({'error': f'No calculation records found for project_id {project_id}'}), 404

    # 生成 function_points.csv
    function_points_output = StringIO()
    function_points_writer = csv.writer(function_points_output)
    function_points_writer.writerow(['name', 'type', 'complexity', 'base_value', 'created_at', 'comment'])
    for fp in function_points:
        function_points_writer.writerow([
            fp.name, fp.type, fp.complexity, fp.base_value, fp.created_at, fp.comment
        ])

    # 生成 calculation_records.csv
    calculation_records_output = StringIO()
    calculation_records_writer = csv.writer(calculation_records_output)
    calculation_records_writer.writerow(['created_at', 'GSC_AFP', 'UFP', 'SCF_AFP', 'VAF', 'total_weight', 'scf_stage'])
    for record in calculation_records:
        calculation_records_writer.writerow([
            record.created_at, record.GSC_AFP, record.UFP, record.SCF_AFP, record.VAF, record.total_weight, record.scf_stage
        ])

    # 打包两个 CSV 文件返回
    return jsonify({
        "function_points_csv": function_points_output.getvalue(),
        "calculation_records_csv": calculation_records_output.getvalue()
    })

@app.route('/get-calculations', methods=['GET'])
def get_calculations():
    # 获取 project_id 参数
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # 查询计算记录
    calculations = CalculationResult.query.filter_by(project_id=project_id).order_by(CalculationResult.created_at.desc()).all()
    if not calculations:
        return jsonify({'error': f'No calculation records found for project_id {project_id}'}), 404

    # 构造返回结果
    result = []
    for record in calculations:
        result.append({
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'GSC_AFP': record.GSC_AFP,  # 替代原 AFP
            'UFP': record.UFP,
            'SCF_AFP': record.SCF_AFP,  # 替代原 SCF
            'VAF': record.VAF,          # 替代原 GSC
            'total_weight': record.total_weight,
            'scf_stage': record.scf_stage
        })

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=6757)
