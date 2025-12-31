# generate_mock_model_files.py
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --------------------------
# 1. 模拟训练一个适配原代码的模型
# --------------------------
# 模拟特征名（完全匹配原代码的format_data顺序）
feature_names = [
    'bill_length', 'bill_depth', 'flipper_length', 'body_mass',
    'island_dream', 'island_torgerson', 'island_biscoe', 'sex_male', 'sex_female'
]

# 模拟训练数据（仅用于生成模型文件，无需真实数据）
mock_X = np.random.rand(100, len(feature_names))  # 100条模拟特征数据
mock_y = np.random.choice([0, 1, 2], size=100)    # 0=阿德利企鹅,1=巴布亚企鹅,2=帽带企鹅

# 训练简单的随机森林模型（仅为生成文件，不追求准确率）
rfc_model = RandomForestClassifier(random_state=42)
rfc_model.fit(mock_X, mock_y)

# 给模型添加feature_names_in_属性（匹配原代码的关键）
rfc_model.feature_names_in_ = feature_names

# --------------------------
# 2. 保存模型文件（rfc_model.pkl）
# --------------------------
with open('rfc_model.pkl', 'wb') as f:
    pickle.dump(rfc_model, f)

# --------------------------
# 3. 生成并保存类别映射文件（output_uniques.pkl）
# --------------------------
# 中文映射：0→阿德利企鹅，1→巴布亚企鹅，2→帽带企鹅（匹配原代码的图片名）
output_uniques_map = {
    0: "阿德利企鹅",
    1: "巴布亚企鹅",
    2: "帽带企鹅"
}

with open('output_uniques.pkl', 'wb') as f:
    pickle.dump(output_uniques_map, f)

print("✅ 模拟模型文件生成完成！")
print("生成的文件：")
print("- rfc_model.pkl（适配原代码的随机森林模型）")
print("- output_uniques.pkl（中文企鹅物种映射）")
