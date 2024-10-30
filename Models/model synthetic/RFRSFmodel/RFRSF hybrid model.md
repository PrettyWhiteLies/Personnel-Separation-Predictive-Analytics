## paper: RFRSF
1. 研究背景：
    - 员工离职问题是人力资源管理中的重要议题，因为关键员工的离职可能给公司带来巨大损失。
2. 研究目标：
    - 提出一种新的员工离职预测模型，结合生存分析和机器学习方法。
3. 数据集
    - 数据集是从中国最大的在线职业社交平台之一爬取的。出于隐私考虑，论文没有披露具体平台的名称。
    - 数据集**内容**
        - 员工的个人信息
        - 教育背景
        - 工作经历
        - 平台活动记录
    - 数据集处理：为了使用生存分析模型，研究者对每个样本进行了标记：
        - 生存时间（Survival Time）：如果工作记录有结束时间，生存时间为开始时间到结束时间的持续时间；如果没有结束时间，生存时间为开始时间到用户更新这条工作记录的时间点的持续时间。
        - 离职状态（Turnover Status）：如果工作记录有结束时间，标记为1（表示发生了离职事件）；否则标记为0，并将该记录标记为右删失（right-censored）。
        - 研究者移除了没有开始时间信息的记录。
        - 研究者随机将数据集按7:3的比例分为训练集和测试集。
    - 数据集分布
        - 总样本数：287,229
        - 正样本（离职）：119,728
        - 负样本（未离职）：167,501
    - 数据特点：
        - 一个员工可能有多条离职记录
        - 工作时长（以月为单位）的分布主要集中在1-24个月之间
        - 离职行为在每年的整数年份（12个月的倍数）有明显的峰值
        - 13-24个月（1-2年）区间的相对离职率明显较高
    - 特征提取：从数据集中提取了22个特征，分为六类：
        - 人口统计学特征（如性别）
        - 工作相关特征（如行业类型、公司规模、职位级别）
        - 平台交互特征（如在线互动次数、发帖数、获赞数等）
        - 教育背景特征（如最高学历、学校类型）
        - 工作变动相关特征（如历史离职记录数、当前工作时长）
        - 生存率特征（通过RSF模型生成）
4. 主要方法：
    - 提出了一种名为RFRSF的混合模型，结合了随机生存森林(RSF)和随机森林(RF)。
        - Random Forest with Random Survival Forest
        - 生存分析部分(RSF):
            - 使用21个特征和2个标签(离职状态和生存时间)训练随机生存森林(RSF)模型。
            - RSF模型输出生存率作为新特征。
            - 生存时间
                - 对于已离职的员工：生存时间 = 离职日期 - 入职日期
                - 对于仍在职的员工：生存时间 = 数据收集日期 - 入职日期
        - 分类部分(RF):
            - 使用23个特征(包括原21个特征、RSF生成的生存率、以及原本作为标签的生存时间)和1个标签(离职状态)训练随机森林(RF)分类器。
        - RFRSF算法流程:
            - 训练RSF模型,直到其Out-of-Bag(OOB)评分达到要求。
            - 使用训练好的RSF模型生成生存率特征。
            - 训练RF分类器,直到其OOB评分达到要求。
            - 使用训练好的RF分类器进行最终的离职预测。
    - 从事件中心的角度处理员工离职问题，而不是传统的以员工为中心的方法。
    - 使用生存分析处理包含删失数据的历史离职记录。
    - 采用策略处理多次离职记录的员工数据。
5. 主要结果：
    - RFRSF模型在准确率、精确率、F1分数和AUC等指标上优于基准方法。
    - 生存分析模型显著提高了员工离职预测的性能。
6. 创新点：
    - 将生存分析与机器学习相结合，处理员工离职预测问题。
    - 考虑了时间因素和历史离职行为的影响。
    - 提出了处理多次离职记录的策略。

## RFRSF model used in our porject

### 数据准备和预处理

- 加载CSV文件
- 然后使用LabelEncoder对所有分类变量进行编码。这是为了将文本数据转换为机器学习算法可以处理的数值形式。
```python
data = pd.read_csv('synthetic_data.csv', index_col=0)

le = LabelEncoder()
categorical_columns = data.select_dtypes(include=['object']).columns

for col in categorical_columns:
    data[col] = le.fit_transform(data[col])
```
- 分离了特征（X）和目标变量（y）。
- 特别注意，它创建了一个新的目标变量`y_1year`，表示员工是否在1年内离职。
```python
X = data.drop(['Label', 'Employee code/number'], axis=1)
y = data['Label']
time = data['Years in current role']

y_1year = (time <= 1) & y
```
- 创建了一个用于生存分析的结构化数组。它包含了是否离职的布尔值和截断在1年的时间。
```python
y_surv = np.array([(bool(y_i), min(t_i, 1.0)) for y_i, t_i in zip(y, time)], 
                  dtype=[('Label', bool), ('time', float)])
```

### 数据分割和特征选择
- 将数据分割为训练集和测试集，然后使用随机森林进行特征选择。它选择了重要性高于中位数的特征。
```python
X_train, X_test, y_train, y_test, y_surv_train, y_surv_test = train_test_split(
    X, y_1year, y_surv, test_size=0.2, random_state=42)

selector = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42), threshold='median')
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)
```

### 特征标准化和处理类别不平衡
- 首先标准化特征
- 然后使用SMOTE技术处理类别不平衡问题。SMOTE通过创建合成样本来增加少数类的样本数。
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_selected)
X_test_scaled = scaler.transform(X_test_selected)

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
```

### 随机生存森林（RSF）模型
- 训练了一个随机生存森林模型
- 并定义了一个函数来预测1年的生存概率。这个概率后续被用作一个额外的特征。
```python
rsf = RandomSurvivalForest(n_estimators=50, max_depth=5, min_samples_leaf=10, random_state=42)
rsf.fit(X_train_resampled, y_surv_train_resampled)

def predict_1year_survival(rsf, X):
    surv_funcs = rsf.predict_survival_function(X)
    surv_probs_1year = [sf(1.0) for sf in surv_funcs]
    return np.array(surv_probs_1year)

surv_prob_train_1year = predict_1year_survival(rsf, X_train_resampled)
surv_prob_test_1year = predict_1year_survival(rsf, X_test_scaled)
```

#### Survival rate

> [!Survival rate]
> 
> 生存分析是一种统计方法，用于分析从某个起始时间点到某个事件发生所需的时间。在员工离职预测中，这个"事件"就是员工离职。
> - 生存函数 S(t)：在时间 t 之后仍然"存活"（未发生事件）的概率。
> - 风险函数 h(t)：在时间 t 时刻发生事件的瞬时概率。
> 
> 实现：
> - RSF模型被训练来预测员工的生存函数。生存函数表示员工在给定时间点仍然在公司的概率。
> 	- 生存函数：生存函数通常是一个随时间递减的函数，表示随着时间推移，员工继续留在公司的概率逐渐降低。
> 	  ![[01_Attachment/Pasted image 20241010145517.png|200]]
> 	- RSF 如何构建生存函数：
> 		- 树的构建：
> 		   - RSF 构建多棵决策树，每棵树都使用bootstrap样本。
> 		   - 在每个节点，RSF 选择最能最大化生存差异的特征进行分裂。
> 		- 生存函数的估计：
> 		   - 对于每个叶节点，RSF 使用 Kaplan-Meier 估计器计算生存函数。
> 		      -  Kaplan-Meier 估计器结果通常以生存曲线的形式呈现，曲线显示随着时间推移，生存概率的变化。
> 		   - 最终的生存函数是所有树的平均。
> - 定义一个函数`predict_1year_survival`来预测1年的生存概率
> 	- 使用训练好的RSF模型预测每个员工的生存函数
> 	- 对每个生存函数，计算在时间点1.0（即1年）时的值，1年的生存率

   
### 随机森林分类器（RF）
- 这里训练了随机森林分类器，使用了包含生存概率的增强特征集。
- 还使用了Cross-validation来评估模型性能。
```python
rf = RandomForestClassifier(n_estimators=50, max_depth=5, min_samples_leaf=10, random_state=42)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(rf, X_train_with_surv, y_train_resampled, cv=cv)

rf.fit(X_train_with_surv, y_train_resampled)
```

#### Cross-validation

> [!交叉验证]
> - 5折交叉验证是一种常用的模型评估技术，它可以帮助我们更准确地估计模型的性能和泛化能力。
> - CV score 主要用于评估模型和调优参数，最终模型会在整个训练集上重新训练。
>
> 5折交叉验证的原理：
> 
> 1. 数据分割：
>    - 将整个数据集随机分成5个大小相等的子集（称为"折"）。
>    - ![[01_Attachment/Pasted image 20241010150041.png|400]]
> 
> 2. 迭代过程：
>    - 进行5次迭代，每次迭代中：
>      a. 选择1个子集作为测试集。
>      b. 剩余的4个子集合并作为训练集。
>      c. 使用训练集训练模型。
>      d. 在测试集上评估模型性能。
> 
> 1. 性能计算：
>    - 计算5次迭代的平均性能指标（如准确率、AUC等）。
>    - 交叉验证的结果（cv_scores）给出了模型在5个不同测试集上的性能，而平均分数（cv_scores.mean()）则提供了一个综合的性能估计。
> 
> 4. 最终评估：
>    - 这个平均性能被视为模型的整体性能估计。
> 
> 5折交叉验证的优势：
> 1. **减少过拟合风险**：
>    - 通过在不同的数据子集上训练和测试，降低了模型过度拟合特定数据集的风险。
> 
> 1. 更可靠的性能估计：
>    - 每个数据点都会被用作训练和测试，充分利用了有限的数据。
>    - 相比单次训练-测试分割，观察到模型在不同数据子集上的表现差异，交叉验证提供了**更稳健的性能估计**。
> 
> 5. 超参数调优：
>    - 常用于选择最佳的模型超参数，通过比较不同参数设置下的交叉验证性能。
> 
> cv之后：
> - **交叉验证（Cross-validation）**：在训练集上进行交叉验证，以评估模型的性能和选择最佳的超参数。CV得分的作用是帮助我们了解模型在不同数据划分上的表现，从而避免过拟合或欠拟合。
> 
> - **重新训练最终模型**：基于交叉验证选定的最佳超参数，在整个训练集（即没有分割的全部训练数据）上重新训练最终模型。这一步确保模型能够充分利用所有训练数据，提升其泛化能力。
> 
> - **在测试集上评估**：最终模型训练好后，通常会在一个单独的测试集上进行评估，来衡量模型的真实性能。这一步是为了确保模型能在未见过的数据上表现良好。
> 

### 模型评估
- 在测试集上评估了模型，计算了准确率，AUC分数等指标。
- 计算turnover possibility
```python
y_pred = rf.predict(X_test_with_surv)
y_pred_proba = rf.predict_proba(X_test_with_surv)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC Score:", roc_auc_score(y_test, y_pred_proba))
```


#### turnover possibility

> [! turnover possibility]
> 传统的分类算法通常只预测离散的类别标签。但在这个模型中，我们生成了连续的turnover probability（离职概率）
> 
> -  我们使用RandomForestClassifier来训练模型。虽然它是一个分类器，但它能够输出概率。
> - `rf.fit(X_train_with_surv, y_train_resampled)` 训练随机森林模型。
> -  rf.predict_proba(X_test_with_surv) 返回每个样本属于每个类的概率。
> - `[:, 1]` 选择第二列，也就是属于正类（在这里是离职）的概率。
> 
> 理论基础---随机森林如何生成概率：
> - 决策树投票：
> 	   - 随机森林由多棵决策树组成。它基于这样一个思想：多个相对简单的模型（决策树）的组合可以产生一个更强大、更准确的模型。
> 	   	   - 随机选择样本（Bootstrap Aggregating，简称Bagging）
> 	   	   - 随机选择特征子集
> 	   - 每棵树对样本进行分类。
> 	   - 决策过程： 对于分类问题（如您的离职预测），最终预测是基于所有树的"投票"结果。
> 
> - 概率计算：
> 	   - 不同于简单的多数投票，`predict_proba` 方法计算的是每个类的概率。
> 	   - 概率 = 投票给该类的树的数量 / 总树木数量
> 	   - 例如，如果100棵树中有30棵预测某员工会离职，那么离职概率就是0.3。
> - 优势
> 	- 生成概率而不是简单的二元分类有几个优势
> 	- 提供更细致的信息：
> 		   - 0.51的离职概率和0.99的离职概率在二元分类中可能都被视为"可能离职"，但它们的风险程度显然不同。
> 		   - 便于进行风险评估和分级
> 	- 允许设置自定义阈值：
> 		   - 根据具体情况，可以调整将概率转换为决策的阈值。

#### recall

In your project, recall indicates the proportion of employees who actually left that the model successfully predicted would leave.
#### AUC

> [!AUC]
> AUC（Area Under the Curve）是指ROC曲线（Receiver Operating Characteristic curve）下的面积，是一个用于评估二分类模型性能的重要指标。让我详细解释一下：
> 
> 1. 定义：
>    - AUC值范围在0到1之间。
>    - AUC = 1 表示完美的分类器，AUC = 0.5 相当于随机猜测。
> 
> 2. ROC曲线：
>    - ROC曲线是以不同分类阈值下的真正率（True Positive Rate，TPR）为纵轴，假正率（False Positive Rate，FPR）为横轴绘制的曲线。
>    - TPR = 真正例 / (真正例 + 假负例)
>    - FPR = 假正例 / (假正例 + 真负例)
> 
> 3. AUC的解释：
>    - AUC可以解释为：从所有正样本中随机选择一个样本，从所有负样本中随机选择一个样本，分类器正确区分这两个样本的概率。
>    - 越接近1，模型的区分能力越强。
> 
> 4. AUC的优势：
>    - 不受类别不平衡的影响。
>    - 与具体的分类阈值无关，评估的是模型的整体排序能力。
> 
> 5. AUC值的一般指导：
>    - 0.5-0.6：几乎没有区分能力
>    - 0.6-0.7：有一些区分能力
>    - 0.7-0.8：有良好的区分能力
>    - 0.8-0.9：有很好的区分能力
>    - 0.9-1.0：有极佳的区分能力



### 阈值优化
- 这段代码计算了ROC曲线，并找到了最佳的分类阈值。
```python
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
```

#### optimal threshold
> [!最佳分类阈值]
> 1. 计算ROC曲线和寻找最佳阈值
> 	a) 使用 `roc_curve` 函数计算不同阈值下的假正率(FPR)和真正率(TPR)。
> 		- 真正率(TPR)：正确预测到将要离职的员工占所有实际离职员工的比例。
> 		- 假正率(FPR)：错误预测会离职但实际不会离职的员工占所有实际不会离职员工的比例。
> 	![[01_Attachment/Pasted image 20241010151949.png|200]]
> 	b) `np.argmax(tpr - fpr)` 找到TPR和FPR之差最大的点，这通常被认为是最佳平衡点。
> 	c) 根据找到的索引，从 `thresholds` 中选取对应的阈值作为最佳阈值。
> 
> ```python
> fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
> optimal_idx = np.argmax(tpr - fpr)
> optimal_threshold = thresholds[optimal_idx]
> ```
> 
> 2. 使用新阈值进行预测
> 
> ```python
> y_pred_new = (y_pred_proba >= optimal_threshold).astype(int)
> ```
> 
> 这行代码使用找到的最佳阈值重新进行分类：
> - **如果预测概率大于或等于最佳阈值，分类为1（正类）**
> - **否则分类为0（负类）**
> - 相比默认的0.5阈值，新阈值可能会稍微偏向于提高TPR，"正确预测到将要离职的员工占所有实际离职员工的比例。"
> 
> 3. 评估使用新阈值的模型性能
> 
> 这个过程的意义：
> 
> 1. 优化决策边界：
> 	   - **默认的分类阈值通常是0.5，但这并不总是最优的。**
> 	   - 通过寻找最佳阈值，我们可以优化模型在特定数据集上的表现。
> 1. 平衡不同类型的错误：
> 	   - 在某些应用中，假阳性和假阴性的代价可能不同。
> 	   - 调整阈值可以帮助我们在这两种错误之间找到更好的平衡。
> 1. **处理类别不平衡：**
> 	   - 当数据集中各类别的样本数量差异很大时，调整阈值特别有用。
> 
> 在员工流失预测的情景中，这个过程可能特别有价值：
> 
> - 如果错误地预测一个员工会离职（假阳性）和错误地预测一个员工不会离职（假阴性）的代价不同，调整阈值可以帮助在这两种错误之间找到更好的平衡。
> 	1. 如果假阴性代价更高（错过真正要离职的员工）：
> 		   - 我们可能会选择降低阈值
> 		   - 这会增加TPR，捕获更多实际离职的员工
> 		   - 但同时也会增加FPR，可能会错误地标记一些不会离职的员工
> 	2. 如果假阳性代价更高（错误地认为员工会离职）：
> 		   - 我们可能会选择提高阈值
> 		   - 这会降低FPR，减少错误地标记不会离职的员工
> 		   - 但同时也会降低TPR，可能会错过一些实际要离职的员工
> - 这可能会导致更有针对性的员工保留策略，从而更有效地分配资源。
> 
> 假正率(FPR)、真正率(TPR)之间的关系，以及调整阈值对它们的影响:
> - 真正率(TPR)：正确预测到将要离职的员工占所有实际离职员工的比例。
> - 假正率(FPR)：错误预测会离职但实际不会离职的员工占所有实际不会离职员工的比例。
> 
> 1. 阈值与TPR和FPR的关系：
>    - 降低阈值：TPR增加，但FPR也会增加
>    - 提高阈值：FPR减少，但TPR也会减少
> ![[01_Attachment/Pasted image 20241010152442.png|200]]
> 2. 权衡：
>    - 理想情况下，我们希望高TPR（捕获大多数实际离职的员工）和低FPR（避免错误地标记不会离职的员工）
>    - 但在实际中，这两者往往是此消彼长的关系
> 3. ROC曲线：
>    - ROC曲线正是描述了不同阈值下TPR和FPR的关系
>    - 曲线上的每一点代表一个特定的阈值设置

### 特征重要性和学习曲线

```python
feature_importance = rf.feature_importances_
feature_names = selected_feature_names + ['Survival Probability']
for name, importance in zip(feature_names, feature_importance):
    print(f"{name}: {importance:.4f}")

train_sizes, train_scores, test_scores = learning_curve(
    rf, X_train_with_surv, y_train_resampled, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 5))
```
这部分分析了特征重要性，并绘制了学习曲线来理解模型的学习过程。

### 其他结果生成
- 基于预测概率和优化的阈值为每个员工生成了具体的建议。
```python
results = pd.DataFrame({
    'Predicted_Label': y_pred_new,
    'Turnover_Probability_1Year': y_pred_proba
})

def provide_recommendation(prob, threshold):
    if prob > threshold * 1.5:
        return f"High risk: There is a {prob:.1%} probability that this employee will leave within the next year. It is recommended to take retention measures immediately."
    elif prob >= threshold:
        return f"Medium risk: The employee has a {prob:.1%} probability of leaving within the next year. It is recommended to closely monitor and consider taking preventive measures."
    else:
        return f"Low risk: This employee has a {prob:.1%} probability of leaving within the next year. Currently, the risk is low, but regular monitoring is still necessary."

results['Recommendation'] = results.apply(lambda row: provide_recommendation(row['Turnover_Probability_1Year'], optimal_threshold), axis=1)
```
