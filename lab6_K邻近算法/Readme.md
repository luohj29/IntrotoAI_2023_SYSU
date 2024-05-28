**运行**
源文件在Code文件夹中，包含了源代码，和运行中产生的中间csv文件
使用方法：preprocess.py是对训练集的预处理；train_preprocess.py是对测试集的预处理；main.py是主函数，对K_classify.py调用计算分类。注意使用main.py要自行更改编码文件tfidf.csv或者onehot.csv;输出时要记得更改文件的名字。

**结果**
结果文件包含两种编码的输出结果以及准确率随着k的变化。