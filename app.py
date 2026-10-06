from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# 當使用者連線到首頁，自動去 templates 資料夾抓 index.html
@app.route('/')
def home():
    return render_template('index.html')

# 當網頁按下按鈕，傳送身高體重到這裡計算
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    height = data.get('height') / 100  # 公分轉公尺
    weight = data.get('weight')
    
    # 計算 BMI
    bmi = round(weight / (height ** 2), 2)
    
    # 判斷身材狀態
    if bmi < 18.5:
        status = "體重過輕"
    elif bmi < 24:
        status = "健康體重"
    else:
        status = "體重過重"
        
    return jsonify({'bmi': bmi, 'status': status})

if __name__ == '__main__':
    # 配合 Render 偵聽環境變數的 PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
